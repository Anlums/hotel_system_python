"""文档加载器：将知识库转为 LangChain Documents，支持 YAML/PDF/Word/TXT/Markdown"""

import yaml
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    Docx2txtLoader,
)

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge_base"


async def load_yaml() -> list[Document]:
    """加载 YAML 知识库文件"""
    docs = []
    for yaml_file in sorted(KNOWLEDGE_DIR.glob("*.yaml")):
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for item in data.get("knowledge", []):
            doc = Document(
                page_content=item["content"],
                metadata={
                    "source": yaml_file.name,
                    "id": item["id"],
                    "category": item.get("category", "general"),
                    "keywords": item.get("keywords", []),
                },
            )
            docs.append(doc)
    return docs


async def load_pdf() -> list[Document]:
    """加载 PDF 文件"""
    docs = []
    for pdf_file in sorted(KNOWLEDGE_DIR.glob("*.pdf")):
        loader = PyPDFLoader(str(pdf_file))
        pages = await loader.aload()
        for page in pages:
            page.metadata["source"] = pdf_file.name
            page.metadata["category"] = "pdf"
        docs.extend(pages)
        print(f"  ［PDF］已加载: {pdf_file.name}（{len(pages)} 页）")
    return docs


async def load_docx() -> list[Document]:
    """加载 Word 文件（.docx）"""
    docs = []
    for docx_file in sorted(KNOWLEDGE_DIR.glob("*.docx")):
        loader = Docx2txtLoader(str(docx_file))
        loaded = loader.load()
        for d in loaded:
            d.metadata["source"] = docx_file.name
            d.metadata["category"] = "word"
        docs.extend(loaded)
        print(f"  ［Word］已加载: {docx_file.name}")
    return docs


async def load_txt() -> list[Document]:
    """加载纯文本文件（.txt）"""
    docs = []
    for txt_file in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        loader = TextLoader(str(txt_file), encoding="utf-8")
        loaded = loader.load()
        for d in loaded:
            d.metadata["source"] = txt_file.name
            d.metadata["category"] = "txt"
        docs.extend(loaded)
        print(f"  ［TXT］已加载: {txt_file.name}")
    return docs


async def load_markdown() -> list[Document]:
    """加载 Markdown 文件（.md），保留标题层级结构"""
    docs = []
    from langchain.text_splitter import MarkdownHeaderTextSplitter

    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
            ]
        )
        chunks = splitter.split_text(content)
        for chunk in chunks:
            chunk.metadata["source"] = md_file.name
            chunk.metadata["category"] = "markdown"
        docs.extend(chunks)
        print(f"  ［MD］已加载: {md_file.name}（{len(chunks)} 个段落）")
    return docs


async def load_all() -> list[Document]:
    """加载 knowledge_base 目录下所有支持的文档"""
    docs = []

    print("RAG 正在加载知识库...")
    docs += await load_yaml()
    docs += await load_pdf()
    docs += await load_docx()
    docs += await load_txt()
    docs += await load_markdown()

    print(f"RAG 知识库加载完成: 共 {len(docs)} 篇文档")
    return docs
