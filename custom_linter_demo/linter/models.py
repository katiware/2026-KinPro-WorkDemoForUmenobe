"""Data models for linter diagnostics and severity levels."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Severity levels for lint findings."""
    ERROR = "ERROR"      # 致命的・動作に支障が出る可能性が高い問題 (赤)
    WARNING = "WARNING"  # バグの温床や規約違反 (黄)
    INFO = "INFO"        # より良いコードにするためのアドバイス (青/シアン)

    @property
    def display_name(self) -> str:
        if self == Severity.ERROR:
            return "【重大なエラー】"
        elif self == Severity.WARNING:
            return "【注意 / 警告】"
        else:
            return "【改善のヒント】"


@dataclass
class Diagnostic:
    """Represents a single issue found by the linter."""
    rule_id: str
    severity: Severity
    message: str
    suggestion: str
    file_path: str
    line: int
    col: int
    line_content: Optional[str] = None
