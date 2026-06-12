# encoding: utf-8
"""
中文分词分析器 — 用于 Whoosh 全文搜索引擎
使用 jieba 分词器对中文文本进行分词，替代英文的 StemmingAnalyzer
"""
from whoosh.analysis import Tokenizer, Token, StopFilter
from jieba import cut_for_search as jieba_cut
import re


class ChineseTokenizer(Tokenizer):
    """使用 jieba 搜索引擎模式进行中文分词"""

    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        # 清理 HTML 标签
        value = re.sub(r'<[^>]+>', ' ', value)
        # 清理 HTML 实体
        value = value.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        # jieba 搜索引擎模式分词（会切分出更多词）
        words = jieba_cut(value)
        token_list = []
        pos = start_pos
        for w in words:
            w = w.strip()
            if w:
                t = Token(
                    positions=True,
                    chars=chars,
                    pos=pos,
                    startchar=start_char,
                    endchar=start_char + len(w),
                )
                t.text = w
                token_list.append(t)
                pos += 1
                start_char += len(w)
        return token_list


def ChineseAnalyzer():
    """返回一个适用于中文的分词分析器"""
    return ChineseTokenizer() | StopFilter()
