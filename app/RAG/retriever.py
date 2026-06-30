"""检索器：TF-IDF 向量检索知识库，返回最相关的文档片段"""

from typing import Optional
from .embedding import TfidfVectorizer, cosine_similarity


class KnowledgeRetriever:
    """基于 TF-IDF 的知识检索器（不依赖外部 API，纯 Python 实现）"""

    def __init__(self):
        self.docs: list[dict] = []          # [{id, category, content, keywords}]
        self.vectors: list[list[float]] = []  # 对应的 TF-IDF 向量
        self.vectorizer = TfidfVectorizer()
        self._ready = False

    @property
    def is_ready(self) -> bool:
        return self._ready

    async def build_index(self, docs: list[dict]):
        """构建 TF-IDF 向量索引（启动时调用一次）"""
        self.docs = docs
        # 把 keywords 也拼到 content 里一起索引，提高关键词匹配率
        texts = []
        for d in docs:
            enriched = d["content"] + " " + " ".join(d.get("keywords", []))
            texts.append(enriched)
        self.vectorizer.fit(texts)
        self.vectors = [self.vectorizer.transform(t) for t in texts]
        self._ready = True

    async def retrieve(
        self,
        query: str,
        top_k: int = 3,
        category: Optional[str] = None,
        min_score: float = 0.1,
    ) -> list[dict]:
        """检索最相关的知识片段

        Args:
            query: 用户问题
            top_k: 返回条数
            category: 按类型过滤（policy/service/faq/pricing 等）
            min_score: 最低相似度阈值

        Returns:
            [{content, score, category}] 按相似度降序
        """
        if not self._ready:
            return [{"content": "知识库正在加载中，请稍后再试。", "score": 0, "category": "system"}]

        query_vec = self.vectorizer.transform(query)

        results = []
        for idx, doc_vec in enumerate(self.vectors):
            score = cosine_similarity(query_vec, doc_vec)
            doc = self.docs[idx]

            if category and doc["category"] != category:
                continue

            results.append({
                "content": doc["content"],
                "score": round(score, 4),
                "category": doc["category"],
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        results = [r for r in results if r["score"] >= min_score]

        return results[:top_k]


# 全局单例
retriever = KnowledgeRetriever()
