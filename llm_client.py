import requests
from config import Config

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """调用 LLM API 生成文本"""
    if Config.LLM_PROVIDER == "deepseek":
        headers = {
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": Config.LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": Config.TEMPERATURE,
            "max_tokens": Config.MAX_TOKENS
        }
        resp = requests.post(Config.DEEPSEEK_API_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data['choices'][0]['message']['content'].strip()
    else:
        raise ValueError(f"不支持的 LLM 提供商: {Config.LLM_PROVIDER}")