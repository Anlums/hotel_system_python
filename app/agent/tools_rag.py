"""RAG 检索工具：注册到 Agent，让 LLM 能检索知识库"""

from langchain_core.tools import tool
from app.RAG.retriever import retriever


def create_rag_tools() -> list:
    """创建 RAG 相关工具"""

    @tool
    async def retrieve_knowledge(query: str, top_k: int = 3) -> str:
        """当客人询问酒店政策（入住/退房/宠物/早餐等）、服务说明（接送/洗衣/停车等）、调价经验、常见问题时，使用此工具检索相关知识库。

        Args:
            query: 客人关心的问题关键词
            top_k: 返回的相关知识条数（默认 3）
        """
        results = await retriever.retrieve(query, top_k=top_k)

        if not results:
            return "未在知识库中找到相关信息。"

        lines = [f"找到 {len(results)} 条相关知识："]
        for r in results:
            tag = f"[{r['category']}]"
            lines.append(f"  {tag} {r['content']}")
        return "\n".join(lines)

    return [retrieve_knowledge]
