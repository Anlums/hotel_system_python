"""向量检索器：使用 ChromaDB + HuggingFace Embeddings"""

from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 持久化目录
CHROMA_DIR = Path(__file__).parent / "chroma_db"

# Embedding 模型：BAAI/bge-small-zh-v1.5（免费中文模型，512维）
EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"

_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
_vectorstore = None
_ready = False


def get_vectorstore() -> Chroma:
    global _vectorstore, _ready
    if _vectorstore is None:
        _vectorstore = Chroma(
            embedding_function=_embeddings,
            persist_directory=str(CHROMA_DIR),
        )
        _ready = True
    return _vectorstore


async def build_index(docs: list):
    """构建/重建索引"""
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "，", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    global _vectorstore, _ready
    _vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=_embeddings,
        persist_directory=str(CHROMA_DIR),
    )
    _ready = True
    return len(chunks)


async def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """检索最相关的知识片段"""
    if not _ready:
        return [{"content": "知识库加载中，请稍后再试。", "score": 0, "category": "system"}]

    vs = get_vectorstore()
    results = vs.similarity_search_with_relevance_scores(query, k=top_k)

    output = []
    for doc, score in results:
        output.append({
            "content": doc.page_content,
            "score": round(float(score), 4),
            "category": doc.metadata.get("category", "general"),
            "source": doc.metadata.get("source", "?"),
        })
    return output
