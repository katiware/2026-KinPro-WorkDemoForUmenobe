"""Rule definitions for beginner-friendly custom linter."""

import ast
import re
from typing import List, Set
from .models import Diagnostic, Severity


class BaseRule:
    """Base class for all lint rules."""
    rule_id: str = "RULE-000"
    name: str = "Base Rule"

    def check(self, tree: ast.AST, source_lines: List[str], file_path: str) -> List[Diagnostic]:
        raise NotImplementedError


class InfiniteLoopRule(BaseRule):
    """RULE-001: Detects while True loops without break, return, or exit."""
    rule_id = "RULE-001"
    name = "無限ループの危険性検知"

    def check(self, tree: ast.AST, source_lines: List[str], file_path: str) -> List[Diagnostic]:
        diagnostics = []

        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                # Check if condition is always truthy (e.g., while True: or while 1:)
                is_always_true = False
                if isinstance(node.test, ast.Constant) and bool(node.test.value) is True:
                    is_always_true = True
                elif isinstance(node.test, ast.NameConstant) and node.test.value is True:
                    is_always_true = True

                if is_always_true:
                    # Check if body contains break, return, raise, or sys.exit
                    has_exit = False
                    for child in ast.walk(node):
                        if isinstance(child, (ast.Break, ast.Return, ast.Raise)):
                            has_exit = True
                            break
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                            if child.func.attr == "exit":
                                has_exit = True
                                break

                    if not has_exit:
                        line_no = node.lineno
                        line_text = source_lines[line_no - 1] if line_no <= len(source_lines) else ""
                        diagnostics.append(Diagnostic(
                            rule_id=self.rule_id,
                            severity=Severity.ERROR,
                            message="`while True:` ループ内に `break` や終了条件が見当たりません。無限ループによりプログラムがフリーズする恐れがあります。",
                            suggestion="ループ内に `if 終了条件: break` を追加するか、`while count < 10:` のように終了条件を指定してください。",
                            file_path=file_path,
                            line=line_no,
                            col=node.col_offset,
                            line_content=line_text
                        ))
        return diagnostics


class MagicNumberRule(BaseRule):
    """RULE-002: Detects unexplainable magic numbers in business logic/expressions."""
    rule_id = "RULE-002"
    name = "マジックナンバーの検出"

    # Allow harmless numbers like 0, 1, 2, -1, 100, 24, 60, etc. in simple contexts
    ALLOWED_NUMBERS = {0, 1, 2, -1, 10, 100, 0.0, 1.0}

    def check(self, tree: ast.AST, source_lines: List[str], file_path: str) -> List[Diagnostic]:
        diagnostics = []

        for node in ast.walk(tree):
            # Check inside binary operations and comparisons (e.g. speed * 1.45, health - 38)
            if isinstance(node, (ast.BinOp, ast.Compare)):
                for child in ast.walk(node):
                    if isinstance(child, ast.Constant) and isinstance(child.value, (int, float)):
                        val = child.value
                        if val not in self.ALLOWED_NUMBERS and abs(val) > 2:
                            # Skip if it is an assignment to an UPPERCASE constant at module level
                            line_no = child.lineno
                            line_text = source_lines[line_no - 1] if line_no <= len(source_lines) else ""
                            # If line defines an UPPER_CASE constant, skip
                            if re.match(r"^[A-Z0-9_]+\s*=", line_text.strip()):
                                continue

                            diagnostics.append(Diagnostic(
                                rule_id=self.rule_id,
                                severity=Severity.INFO,
                                message=f"計算式の中に直接数値 `{val}`（マジックナンバー）が記述されています。",
                                suggestion=f"プログラム上部に `PLAYER_SPEED = {val}` や `MAX_DAMAGE = {val}` のように意味のある定数として定義すると読みやすくなります。",
                                file_path=file_path,
                                line=line_no,
                                col=child.col_offset,
                                line_content=line_text
                            ))
        return diagnostics


class SilentExceptionRule(BaseRule):
    """RULE-003: Detects bare except or except Exception: pass (swallowed exceptions)."""
    rule_id = "RULE-003"
    name = "例外の握りつぶし検知"

    def check(self, tree: ast.AST, source_lines: List[str], file_path: str) -> List[Diagnostic]:
        diagnostics = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                # Check if body only contains 'pass'
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    line_no = node.lineno
                    line_text = source_lines[line_no - 1] if line_no <= len(source_lines) else ""
                    diagnostics.append(Diagnostic(
                        rule_id=self.rule_id,
                        severity=Severity.WARNING,
                        message="例外処理ブロック内で `pass` によりエラーが握りつぶされています。バグの原因特定が極めて困難になります。",
                        suggestion="`print(f'エラーが発生しました: {e}')` などでエラー内容をログ出力するか、具体的な例外型（例: `ValueError`）を指定してください。",
                        file_path=file_path,
                        line=line_no,
                        col=node.col_offset,
                        line_content=line_text
                    ))
        return diagnostics


class NamingConventionRule(BaseRule):
    """RULE-004: Checks if functions and variables follow Python's snake_case convention."""
    rule_id = "RULE-004"
    name = "命名規則（snake_case）チェック"

    CAMEL_CASE_REGEX = re.compile(r"^[a-z]+[A-Z0-9]")

    def check(self, tree: ast.AST, source_lines: List[str], file_path: str) -> List[Diagnostic]:
        diagnostics = []

        for node in ast.walk(tree):
            # Function definitions
            if isinstance(node, ast.FunctionDef):
                fn_name = node.name
                if not fn_name.startswith("__") and self.CAMEL_CASE_REGEX.match(fn_name):
                    line_no = node.lineno
                    line_text = source_lines[line_no - 1] if line_no <= len(source_lines) else ""
                    # Convert to snake_case recommendation
                    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", fn_name).lower()
                    diagnostics.append(Diagnostic(
                        rule_id=self.rule_id,
                        severity=Severity.WARNING,
                        message=f"関数名 `{fn_name}` がキャメルケースになっています。Pythonでは `snake_case`（小文字とアンダースコア）が標準規約です。",
                        suggestion=f"`def {snake}(...):` のように小文字とアンダースコアで命名することを推奨します。",
                        file_path=file_path,
                        line=line_no,
                        col=node.col_offset,
                        line_content=line_text
                    ))

            # Variable assignments inside functions
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        # If not ALL_CAPS (constant) and is camelCase
                        if not var_name.isupper() and self.CAMEL_CASE_REGEX.match(var_name):
                            line_no = target.lineno
                            line_text = source_lines[line_no - 1] if line_no <= len(source_lines) else ""
                            snake = re.sub(r"(?<!^)(?=[A-Z])", "_", var_name).lower()
                            diagnostics.append(Diagnostic(
                                rule_id=self.rule_id,
                                severity=Severity.INFO,
                                message=f"変数名 `{var_name}` がキャメルケースになっています。",
                                suggestion=f"`{snake}` のように小文字の `snake_case` に変更するとPythonらしい読みやすいコードになります。",
                                file_path=file_path,
                                line=line_no,
                                col=target.col_offset,
                                line_content=line_text
                            ))
        return diagnostics


class MainGuardRule(BaseRule):
    """RULE-005: Checks if an executable script has if __name__ == '__main__': guard."""
    rule_id = "RULE-005"
    name = "メインガード（__main__）の確認"

    def check(self, tree: ast.AST, source_lines: List[str], file_path: str) -> List[Diagnostic]:
        diagnostics = []

        has_function_or_class = False
        has_main_guard = False
        top_level_calls = []

        if isinstance(tree, ast.Module):
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    has_function_or_class = True
                elif isinstance(node, ast.If):
                    # Check if test is __name__ == '__main__'
                    if isinstance(node.test, ast.Compare):
                        left = node.test.left
                        if isinstance(left, ast.Name) and left.id == "__name__":
                            has_main_guard = True
                elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    top_level_calls.append(node)

            if has_function_or_class and top_level_calls and not has_main_guard:
                first_call = top_level_calls[0]
                line_no = first_call.lineno
                line_text = source_lines[line_no - 1] if line_no <= len(source_lines) else ""
                diagnostics.append(Diagnostic(
                    rule_id=self.rule_id,
                    severity=Severity.INFO,
                    message="関数定義があるファイルで、トップレベル（最上位）から直接処理を実行しています。",
                    suggestion="他のスクリプトからimportした際の誤作動を防ぐため、`if __name__ == '__main__':` ブロック内に実行コードを記述することをおすすめします。",
                    file_path=file_path,
                    line=line_no,
                    col=first_call.col_offset,
                    line_content=line_text
                ))
        return diagnostics


# Default ruleset registered for the beginner linter
DEFAULT_RULES: List[BaseRule] = [
    InfiniteLoopRule(),
    SilentExceptionRule(),
    NamingConventionRule(),
    MagicNumberRule(),
    MainGuardRule(),
]
