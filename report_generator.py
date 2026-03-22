#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from tqdm import tqdm

from config import Config
from sections import ALL_SECTIONS
from utils import (
    extract_text_from_file,
    load_progress,
    save_progress,
    append_to_markdown,
    convert_markdown_to_docx,
    unescape_markdown
)
from llm_client import call_llm

def generate_chapter(section: dict, context: str) -> str:
    """调用 LLM 生成单个章节内容"""
    system_prompt = "你是一位专业的可行性研究报告撰写专家。"
    user_prompt = f"""
请根据以下项目信息，撰写【{section['id']} {section['title']}】部分。

【项目信息】
{context}

【写作要求】
{section['requirements']}

请直接输出章节内容，不要添加额外解释。
"""
    content = call_llm(system_prompt, user_prompt)
    return unescape_markdown(content)

def main():
    parser = argparse.ArgumentParser(description="可行性研究报告自动生成器")
    parser.add_argument("--project_name", required=True, help="项目名称")
    parser.add_argument("--file", required=True, help="项目资料文件路径（txt/md/pdf/docx）")
    parser.add_argument("--report_id", required=True, help="报告唯一标识")
    parser.add_argument("--resume", action="store_true", help="是否断点续传")
    parser.add_argument("--format", default="md", choices=["md", "docx"], help="输出格式，默认 md")
    args = parser.parse_args()

    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        sys.exit(1)

    # 提取文档内容
    print("正在提取文档内容...")
    try:
        context = extract_text_from_file(args.file)
    except Exception as e:
        print(f"文档提取失败: {e}")
        sys.exit(1)

    # 加载进度
    progress = load_progress(args.report_id, args.resume)
    completed = set(progress["completed_chapters"])
    base_output = progress["output_file"]
    if args.format == "docx":
        base_output = base_output.replace(".md", ".docx")
    output_file = base_output

    # 如果 resume=False，清空已有报告文件
    if not args.resume and os.path.exists(output_file):
        os.remove(output_file)
        progress["completed_chapters"] = []
        save_progress(progress)

    # 待生成章节
    remaining = [s for s in ALL_SECTIONS if s["id"] not in completed]
    if not remaining:
        print("所有章节已生成完毕！")
        return

    print(f"共有 {len(remaining)} 个章节待生成。")

    # 收集所有生成的 Markdown 内容（用于最后转为 docx）
    all_chapters_md = []

    for section in tqdm(remaining, desc="生成章节"):
        try:
            content = generate_chapter(section, context)
        except Exception as e:
            print(f"\n生成 {section['id']} {section['title']} 时出错: {e}")
            content = f"**生成失败：** {e}\n"

        # 添加到 Markdown 文件（如果输出格式是 md，则实时追加；如果是 docx，则先收集）
        if args.format == "md":
            append_to_markdown(output_file, section, content)
        else:
            # 收集 Markdown 内容，稍后统一转换
            chapter_md = f"## {section['id']} {section['title']}\n\n{content}\n\n"
            all_chapters_md.append(chapter_md)

        # 更新进度
        progress["completed_chapters"].append(section["id"])
        save_progress(progress)

    # 如果输出格式是 docx，将收集的所有 Markdown 转为 Word
    if args.format == "docx":
        full_markdown = "\n".join(all_chapters_md)
        print("正在将 Markdown 转换为 Word 文档...")
        convert_markdown_to_docx(full_markdown, output_file)

    print(f"\n报告生成完成！文件保存在: {output_file}")

if __name__ == "__main__":
    main()