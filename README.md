# 可行性研究报告自动生成器

本项目是一个纯 Python 脚本，用于根据项目资料自动生成规范的可行性研究报告（可研报告）。支持断点续传、多种文件格式输入，并可输出为 Markdown 或 Word 文档（docx）。

功能特性
📄 多格式输入：支持 .txt、.md、.pdf、.docx 文件，自动提取项目信息

✍️ 智能生成：基于 LLM（大语言模型）逐章生成专业内容，覆盖 11 章 50+ 小节

🔁 断点续传：生成中断后，再次运行可跳过已生成章节，继续完成剩余部分

🎨 双格式输出：可直接生成 Markdown（.md）或格式精美的 Word 文档（.docx）

⚙️ 灵活配置：通过环境变量设置 API 密钥、模型、温度等参数

🖥️ 轻量运行：无需 Web 服务，命令行一键启动

安装
1. 克隆项目
git clone https://github.com/your-username/feasibility-report-generator.git
cd feasibility-report-generator

2. 安装依赖
pip install -r requirements.txt
建议使用虚拟环境（如 python -m venv venv）隔离项目依赖。

3. 配置 API 密钥
复制示例配置文件并编辑：
cp .env.example .env
编辑 .env 文件，填入你的 DeepSeek API Key（或其他支持的 LLM）：
DEEPSEEK_API_KEY=sk-your-api-key-here

使用方法
基本命令
python report_generator.py --project_name "项目名称" --file 资料文件路径 --report_id 报告标识 [--format md|docx] [--resume]
参数说明
参数	必填	说明
--project_name	✅	项目名称，用于报告中显示
--file	✅	项目资料文件路径，支持 .txt、.md、.pdf、.docx
--report_id	✅	报告唯一标识（如 001），用于生成文件名和进度管理
--format	❌	输出格式，md（Markdown）或 docx（Word），默认 md
--resume	❌	断点续传标志，若存在已完成进度，则继续生成未完成的章节

示例
1. 生成 Markdown 报告
python report_generator.py \
    --project_name "霍邱县周集淮畔大酒店" \
    --file sample_data/sample_project_info.txt \
    --report_id "001"
2. 生成 Word 报告
python report_generator.py \
    --project_name "霍邱县周集淮畔大酒店" \
    --file sample_data/sample_project_info.txt \
    --report_id "001" \
    --format docx
3. 断点续传（中断后继续）
假设之前运行到一半中断了，再次执行并加上 --resume：
python report_generator.py \
    --project_name "霍邱县周集淮畔大酒店" \
    --file sample_data/sample_project_info.txt \
    --report_id "001" \
    --format docx \
    --resume
程序会自动读取进度文件 progress_001.json，跳过已生成的章节，继续生成剩余部分。

输出文件
Markdown 格式：report_{report_id}.md

Word 格式：report_{report_id}.docx

进度文件：progress_{report_id}.json（用于断点续传）

自定义章节
如需调整报告章节结构或写作要求，请编辑 sections.py 中的 ALL_SECTIONS 列表。每个章节包含 id、title 和 requirements（写作要求），你可以增删改章节，或修改每个章节的生成提示词。

支持的 LLM 提供商
当前支持 DeepSeek 官方 API。如需使用其他兼容 OpenAI 接口的模型，可在 llm_client.py 中扩展，或在 config.py 中修改 LLM_PROVIDER 和对应 URL。

常见问题
Q: 运行报错“请设置 DEEPSEEK_API_KEY 环境变量”
A: 检查 .env 文件是否正确配置，并确保文件名是 .env（注意前面的点）。如果使用其他方式设置环境变量，也可直接 export。

Q: 生成的 Word 文档中表格或样式不对
A: 程序内置了简单的 Markdown 表格解析，并应用了 Word 的“Light Grid Accent 1”样式。如需更复杂的样式，可自行修改 utils.py 中的 _parse_table 和 set_chinese_font 函数。

Q: 生成过程中断，如何继续？
A: 使用 --resume 参数重新运行即可。进度文件会记录已完成章节，不会重复生成。

Q: 支持 PDF 或 DOCX 输入文件吗？
A: 支持，但需要安装对应库（已在 requirements.txt 中）。PDF 依赖 PyPDF2，DOCX 依赖 python-docx。

Q: 如何调整生成的内容长度或风格？
A: 可以在 sections.py 中修改每个章节的 requirements 字段，例如增加“字数控制”、“突出数据”、“语言风格”等要求。

许可证
本项目采用 MIT 许可证，允许自由使用和修改。

致谢
DeepSeek 提供强大的 LLM 服务

python-docx、PyPDF2 等优秀开源库