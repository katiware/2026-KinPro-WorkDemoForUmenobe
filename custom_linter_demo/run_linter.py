#!/usr/bin/env python3
"""CLI Entry point for KinPro Custom Linter."""

import argparse
import io
import sys
from pathlib import Path
from typing import Dict, List

# Ensure safe UTF-8 output on Windows consoles
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from linter import Diagnostic, LintAnalyzer, LintReporter


def collect_python_files(target_paths: List[str]) -> List[Path]:
    """Collects all .py files from specified paths or directories."""
    files: List[Path] = []
    for p_str in target_paths:
        path = Path(p_str)
        if not path.exists():
            print(f"エラー: 指定されたパスが存在しません: {path}", file=sys.stderr)
            continue
        if path.is_file():
            if path.suffix.lower() == ".py":
                files.append(path)
            else:
                print(f"スキップ: Pythonファイル (.py) ではありません: {path}", file=sys.stderr)
        elif path.is_dir():
            # Recursively find .py files excluding hidden or venv directories
            for sub_file in path.rglob("*.py"):
                if not any(part.startswith((".", "__", "venv", ".venv")) for part in sub_file.parts):
                    files.append(sub_file)
    return sorted(list(set(files)))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="初心者向け作品制作カスタムリンター (KinPro 2026)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python run_linter.py samples/bad_sample.py
  python run_linter.py samples/good_sample.py
  python run_linter.py samples/
        """
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["samples/"],
        help="検査対象のファイルまたはディレクトリのパス (デフォルト: samples/)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="ターミナル出力をカラー化しない"
    )

    args = parser.parse_args()

    files = collect_python_files(args.paths)
    if not files:
        print("検査対象のPythonファイルが見つかりませんでした。")
        return 0

    analyzer = LintAnalyzer()
    reporter = LintReporter(use_color=not args.no_color)

    print("=" * 70)
    print("🔍 KinPro 初心者向けカスタムリンター を実行中...")
    print("=" * 70)

    all_diagnostics: Dict[str, List[Diagnostic]] = {}

    for f in files:
        rel_path = str(f)
        diagnostics = analyzer.analyze_file(f)
        all_diagnostics[rel_path] = diagnostics
        reporter.report_file_results(rel_path, diagnostics)

    exit_code = reporter.report_summary(len(files), all_diagnostics)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
