"""文本向量化与检索：基于 TF-IDF + 余弦相似度（纯 numpy 实现，不依赖外部 API）"""

import math
import re
from collections import Counter
from typing import Optional


# 中文分词（简单正向最大匹配 + 单字切分兜底）
_STOP_WORDS = {"的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
               "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
               "会", "着", "没有", "看", "好", "自己", "这", "他", "她", "它",
               "们", "那", "些", "什么", "怎么", "如何", "请问", "吗", "呢",
               "吧", "啊", "哦", "嗯", "呀", "啦"}


def _simple_cut(text: str) -> list[str]:
    """简单分词：按空格/标点切分 + 提取中文字符为单字"""
    # 按非字母数字下划线切分
    tokens = re.findall(r'[一-鿿]+|[a-zA-Z0-9]+', text.lower())
    result = []
    for token in tokens:
        if re.match(r'^[一-鿿]+$', token):
            # 中文词：切成单字
            for char in token:
                if char not in _STOP_WORDS:
                    result.append(char)
        else:
            # 英文/数字：保留原样
            if token not in _STOP_WORDS:
                result.append(token)
    return result


def _compute_tf(text: str) -> dict[str, float]:
    """计算 TF（词频）"""
    words = _simple_cut(text)
    total = len(words)
    if total == 0:
        return {}
    counter = Counter(words)
    return {word: count / total for word, count in counter.items()}


def _compute_idf(corpus: list[str]) -> dict[str, float]:
    """计算 IDF（逆文档频率）"""
    n_docs = len(corpus)
    df: Counter = Counter()
    for doc in corpus:
        words = set(_simple_cut(doc))
        for word in words:
            df[word] += 1
    return {word: math.log((n_docs + 1) / (freq + 1)) + 1
            for word, freq in df.items()}


class TfidfVectorizer:
    """TF-IDF 向量化器"""

    def __init__(self):
        self.idf: dict[str, float] = {}
        self.vocab: list[str] = []

    def fit(self, corpus: list[str]):
        """拟合语料库"""
        self.idf = _compute_idf(corpus)
        self.vocab = sorted(self.idf.keys())

    def transform(self, text: str) -> list[float]:
        """将文本转为 TF-IDF 向量"""
        tf = _compute_tf(text)
        vec = []
        for word in self.vocab:
            vec.append(tf.get(word, 0.0) * self.idf.get(word, 0.0))
        return vec


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
