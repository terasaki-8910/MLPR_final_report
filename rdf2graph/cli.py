"""rdf2graphのコマンドラインエントリポイント。各フェーズの機能はPhase進行に応じて追加する。"""
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="rdf2graph")
    parser.parse_args()


if __name__ == "__main__":
    main()
