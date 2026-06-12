# encoding: utf-8
"""
最小化中文搜索后端 — 继承标准 haystack whoosh 后端，仅替换中文分词分析器
避免复制整个后端文件，减少维护成本和 Django 版本兼容性问题
"""
from haystack.backends.whoosh_backend import (
    WhooshSearchBackend,
    WhooshSearchQuery,
    WhooshEngine as BaseWhooshEngine,
)
from whoosh.fields import TEXT
from .ChineseAnalyzer import ChineseAnalyzer


class ChineseWhooshSearchBackend(WhooshSearchBackend):
    """
    与标准 WhooshSearchBackend 相同，仅将文本字段的 analyzer 替换为
    基于 jieba 的 ChineseAnalyzer，以支持中文分词搜索
    """

    def build_schema(self, fields):
        content_field_name, schema = super().build_schema(fields)

        # 将文本字段的 analyzer 替换为中文分词器
        # 标准后端使用 StemmingAnalyzer（仅支持英文），替换为 jieba 分词
        for field_name, field in schema.items():
            if isinstance(field, TEXT):
                field.analyzer = ChineseAnalyzer()

        return content_field_name, schema


class ChineseWhooshSearchQuery(WhooshSearchQuery):
    """与标准 WhooshSearchQuery 相同，无需额外修改"""
    pass


class WhooshEngine(BaseWhooshEngine):
    """中文搜索引擎入口"""
    backend = ChineseWhooshSearchBackend
    query = ChineseWhooshSearchQuery
