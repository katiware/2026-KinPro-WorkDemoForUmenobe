"""ANSI color terminal reporter for beginner-friendly diagnostics."""

import os
import sys
from typing import Dict, List
from .models import Diagnostic, Severity


class Colors:
    """ANSI color escape sequences."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    GRAY = "\033[90m"


class LintReporter:
    """Formats and prints lint diagnostics to the console."""

    def __init__(self, use_color: bool = True):
        # Enable ANSI colors on Windows 10+
        if os.name == "nt":
            os.system("")
        self.use_color = use_color

    def _c(self, color_code: str, text: str) -> str:
        if not self.use_color:
            return text
        return f"{color_code}{text}{Colors.RESET}"

    def report_file_results(self, file_path: str, diagnostics: List[Diagnostic]) -> None:
        """Prints diagnostics for a single file."""
        if not diagnostics:
            print(f"{self._c(Colors.GREEN + Colors.BOLD, '  PASS ')} {self._c(Colors.BOLD, file_path)}")
            return

        print(f"\n{self._c(Colors.BOLD + Colors.MAGENTA, '▶ ファイル:')} {self._c(Colors.BOLD, file_path)}")
        print(self._c(Colors.GRAY, "─" * 70))

        for d in diagnostics:
            # Color by severity
            if d.severity == Severity.ERROR:
                badge = self._c(Colors.RED + Colors.BOLD, f" [ {d.severity.display_name} ] ")
                rule_tag = self._c(Colors.RED, f"({d.rule_id})")
            elif d.severity == Severity.WARNING:
                badge = self._c(Colors.YELLOW + Colors.BOLD, f" [ {d.severity.display_name} ] ")
                rule_tag = self._c(Colors.YELLOW, f"({d.rule_id})")
            else:
                badge = self._c(Colors.CYAN + Colors.BOLD, f" [ {d.severity.display_name} ] ")
                rule_tag = self._c(Colors.CYAN, f"({d.rule_id})")

            pos_info = self._c(Colors.GRAY, f"Line {d.line}:{d.col}")
            print(f"{badge} {pos_info} {rule_tag}")
            print(f"   {self._c(Colors.BOLD, d.message)}")

            # Print code excerpt if available
            if d.line_content is not None:
                stripped_line = d.line_content.rstrip()
                print(f"   {self._c(Colors.GRAY, f'{d.line:4d} | ')}{stripped_line}")
                # Point to column
                pointer_indent = " " * (7 + max(0, d.col))
                print(f"{pointer_indent}{self._c(Colors.YELLOW + Colors.BOLD, '^')}")

            # Print suggestion
            print(f"   {self._c(Colors.GREEN + Colors.BOLD, '💡 修正のアドバイス:')} {d.suggestion}")
            print()

    def report_summary(self, total_files: int, all_diagnostics: Dict[str, List[Diagnostic]]) -> int:
        """Prints overall summary across all analyzed files."""
        total_errors = sum(1 for diags in all_diagnostics.values() for d in diags if d.severity == Severity.ERROR)
        total_warnings = sum(1 for diags in all_diagnostics.values() for d in diags if d.severity == Severity.WARNING)
        total_infos = sum(1 for diags in all_diagnostics.values() for d in diags if d.severity == Severity.INFO)
        clean_files = sum(1 for diags in all_diagnostics.values() if len(diags) == 0)

        print(self._c(Colors.GRAY, "=" * 70))
        print(f"{self._c(Colors.BOLD, '📊 静的解析サマリー:')}")
        print(f"   検査対象ファイル数 : {total_files} 件")
        print(f"   問題なし (合格)    : {self._c(Colors.GREEN + Colors.BOLD, str(clean_files))} ファイル")
        print(f"   重大エラー (ERROR)  : {self._c(Colors.RED + Colors.BOLD, str(total_errors))} 件")
        print(f"   警告 (WARNING)     : {self._c(Colors.YELLOW + Colors.BOLD, str(total_warnings))} 件")
        print(f"   改善ヒント (INFO)   : {self._c(Colors.CYAN + Colors.BOLD, str(total_infos))} 件")
        print(self._c(Colors.GRAY, "=" * 70))

        if total_errors == 0 and total_warnings == 0:
            print(self._c(Colors.GREEN + Colors.BOLD, "🎉 すべてのチェックをクリアしました！素晴らしいコードです！\n"))
            return 0
        elif total_errors == 0:
            print(self._c(Colors.YELLOW + Colors.BOLD, "✨ 重大なエラーはありません。警告やヒントを参考にブラッシュアップしてみましょう！\n"))
            return 0
        else:
            print(self._c(Colors.RED + Colors.BOLD, "⚠️ 重大なエラーが見つかりました。アドバイスを参考に修正してみてください。\n"))
            return 1
