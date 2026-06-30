"""知识库文档加载器：从 YAML 文件加载知识库内容"""

import yaml
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge_base"


async def load_knowledge_base() -> list[dict]:
    """加载所有知识库 YAML 文件，返回 [{id, category, content, keywords}] 列表"""
    docs = []

    for yaml_file in sorted(KNOWLEDGE_DIR.glob("*.yaml")):
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for item in data.get("knowledge", []):
            docs.append({
                "id": item["id"],
                "category": item.get("category", "general"),
                "content": item["content"],
                "keywords": item.get("keywords", []),
            })

    return docs
