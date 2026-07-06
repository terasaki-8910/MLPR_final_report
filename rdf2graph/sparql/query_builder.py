"""SPARQLクエリ文字列を安全に組み立てるためのプレースホルダヘルパー。

CLAUDE.md アーキテクチャ原則#3「SPARQLは安全側に倒す」に基づき、値を生文字列連結で
クエリテンプレートに埋め込むことを禁止する。呼び出し側はここで検証・エスケープ済みの
文字列表現を得てから埋め込む。Phase 2 の profiler.py でも同じヘルパーを再利用する。
"""
import re

_IRI_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^\s<>]+$")


class QueryBuilderError(ValueError):
    """iri() / int_literal() / string_literal() に不正な値が渡された場合の例外。"""


def iri(value: str) -> str:
    """IRI文字列を検証し、SPARQLの``<...>``形式に変換する。"""
    if not isinstance(value, str) or not _IRI_RE.match(value):
        raise QueryBuilderError(f"invalid IRI: {value!r}")
    return f"<{value}>"


def int_literal(value: int) -> str:
    """int型への変換を強制することで、文字列連結によるインジェクションを構造的に防ぐ。"""
    return str(int(value))


def string_literal(value: str) -> str:
    """SPARQLの文字列リテラルとして安全な形にエスケープする。"""
    if not isinstance(value, str):
        raise QueryBuilderError(f"expected str, got {type(value)!r}")
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'
