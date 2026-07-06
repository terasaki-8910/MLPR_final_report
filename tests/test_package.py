def test_import():
    """pytestが0件収集で終了コード5を返すのを防ぐ最小スモークテスト。"""
    import rdf2graph  # noqa: F401
