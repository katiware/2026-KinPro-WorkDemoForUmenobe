"""Core AST analyzer engine that executes rules on Python source files."""

import ast
import sys
from pathlib import Path
from typing import List, Optional
from .models import Diagnostic, Severity
from .rules import DEFAULT_RULES, BaseRule


class LintAnalyzer:
    """Orchestrates parsing and rule execution for Python files."""

    def __init__(self, rules: Optional[List[BaseRule]] = None):
        self.rules = rules if rules is not None else DEFAULT_RULES

    def analyze_source(self, code: str, file_path: str = "<input>") -> List[Diagnostic]:
        """Analyzes a source string and returns list of Diagnostics."""
        source_lines = code.splitlines()

        # Syntax error checking via AST parsing
        try:
            tree = ast.parse(code, filename=file_path)
        except SyntaxError as e:
            line_no = e.lineno or 1
            line_text = source_lines[line_no - 1] if 0 < line_no <= len(source_lines) else ""
            return [
                Diagnostic(
                    rule_id="SYNTAX-001",
                    severity=Severity.ERROR,
                    message=f"構文エラー (SyntaxError): {e.msg}",
                    suggestion="コロン `:` や閉じ括弧 `)` の付け忘れ、インデントのズレがないか確認してください。",
                    file_path=file_path,
                    line=line_no,
                    col=e.offset or 0,
                    line_content=line_text
                )
            ]
        except Exception as e:
            return [
                Diagnostic(
                    rule_id="PARSER-ERR",
                    severity=Severity.ERROR,
                    message=f"ファイル解析エラー: {str(e)}",
                    suggestion="ファイルの文字コード（UTF-8推奨）や内容を確認してください。",
                    file_path=file_path,
                    line=1,
                    col=0,
                    line_content=""
                )
            ]

        # Execute registered rules
        diagnostics: List[Diagnostic] = []
        for rule in self.rules:
            try:
                rule_findings = rule.check(tree, source_lines, file_path)
                diagnostics.extend(rule_findings)
            except Exception as ex:
                print(f"[警告] ルール {rule.rule_id} の実行中にエラーが発生しました: {ex}", file=sys.stderr)

        # Sort diagnostics by line number and column
        diagnostics.sort(key=lambda d: (d.line, d.col))
        return diagnostics

    def analyze_file(self, file_path: Path) -> List[Diagnostic]:
        """Reads a file from disk and analyzes it."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="shift_jis", errors="replace") as f:
                code = f.read()
        except Exception as e:
            return [
                Diagnostic(
                    rule_id="FILE-READ-ERR",
                    severity=Severity.ERROR,
                    message=f"ファイルを開けませんでした: {str(e)}",
                    suggestion="ファイルの存在とアクセス権限を確認してください。",
                    file_path=str(file_path),
                    line=1,
                    col=0,
                    line_content=""
                )
            ]

        return self.analyze_source(code, str(file_path))
