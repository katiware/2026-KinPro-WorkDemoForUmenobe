# 🔍 Custom Linter デモ (KinPro 2026)

新入生が作品制作を行う際に、**初心者が陥りがちなミスを自動検知して親切な日本語でアドバイスを提示する** カスタム静的解析ツール（リンター）のデモです。

Python標準ライブラリの `ast`（抽象構文木）を使用しているため、外部パッケージのインストール不要で即座に動作します。

---

## 🎯 実装されている初心者支援ルール一覧

| ルールID | 種別 | ルール名 | 検知内容とアドバイス |
| :--- | :--- | :--- | :--- |
| **RULE-001** | `ERROR` | 無限ループの危険性検知 | `while True:` 内に `break` や終了条件がない場合、フリーズを防ぐため修正を促す |
| **RULE-002** | `INFO` | マジックナンバーの検出 | 計算式に直接書かれた数値を、意味のある定数（`UPPER_CASE`）として定義するよう案内 |
| **RULE-003** | `WARNING` | 例外の握りつぶし検知 | `except: pass` によりエラー原因が不明になるのを防ぎ、ログ出力や特定例外の指定を推奨 |
| **RULE-004** | `WARNING` | 命名規則（snake_case） | 関数名や変数名がキャメルケースの場合、Python標準の `snake_case` への変換を提案 |
| **RULE-005** | `INFO` | メインガードの確認 | スクリプトが直接実行される場合に、`if __name__ == '__main__':` の利用を案内 |

---

## 🚀 使い方

### 1. NGサンプル（ミスを含むコード）を検査
```bash
python run_linter.py samples/bad_sample.py
```
👉 ターミナルに各エラーの行番号、コード抜粋、および具体的な修正アドバイスが表示されます。

### 2. OKサンプル（改善後のコード）を検査
```bash
python run_linter.py samples/good_sample.py
```
👉 「🎉 すべてのチェックをクリアしました！」と合格表示されます。

### 3. 自作スクリプトを検査
```bash
python run_linter.py path/to/your_script.py
```

---

## 💡 新しいルールの追加方法

新入生が自分たちで新しいルールを追加したい場合は、`linter/rules.py` に `BaseRule` を継承したクラスを作成し、`DEFAULT_RULES` に追加するだけで拡張できます。

```python
class MyCustomRule(BaseRule):
    rule_id = "RULE-006"
    name = "print文の過剰使用チェック"

    def check(self, tree: ast.AST, source_lines: List[str], file_path: str) -> List[Diagnostic]:
        diagnostics = []
        # ast.walk(tree) で構文木を探索して検査ロジックを実装
        return diagnostics
```
