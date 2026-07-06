"""logging設定の一元化（CLAUDE.md 品質基準: print禁止、loggingを使う）。"""
import logging

_CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    """呼び出し元の`__name__`を渡して設定済みのloggerを取得する。"""
    global _CONFIGURED
    if not _CONFIGURED:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )
        _CONFIGURED = True
    return logging.getLogger(name)
