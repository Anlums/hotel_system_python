"""文档加载器：将知识库转为 LangChain Documents，支持多种格式"""

import yaml
from pathlib import Path
from langchain_core.documents import Document

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge_base"


async def load_yaml_knowledge() -> list[Document]:
    """加载 YAML 知识库文件为 LangChain Documents"""
    docs = []
    for yaml_file in sorted(KNOWLEDGE_DIR.glob("*.yaml")):
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for item in data.get("knowledge", []):
            doc = Document(
                page_content=item["content"],
                metadata={
                    "id": item["id"],
                    "category": item.get("category", "general"),
                    "keywords": item.get("keywords", []),
                    "source": yaml_file.name,
                },
            )
            docs.append(doc)
    return docs


async def load_all() -> list[Document]:
    """加载所有文档（YAML + 后续可扩展 PDF/网页等）"""
    docs = await load_yaml_knowledge()
    # 后续扩展：加载 PDF、网页等
    # from langchain_community.document_loaders import PyPDFLoader
    # docs += await PyPDFLoader("policies.pdf").aload()
    return docs
