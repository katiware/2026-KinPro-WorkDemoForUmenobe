# 🛠️ 2026うめの辺祭 新入生作品制作 環境構築完全ガイド

本ガイドは、2026年うめの辺祭（KinPro）での作品制作に向けて、**Python / Streamlit / Custom Linter / Godot** の環境構築手順をまとめたものです。

---

## 📑 目次
1. [全体概要](#1-全体概要)
2. [Python & pip のセットアップ（共通基盤）](#2-python--pip-のセットアップ共通基盤)
3. [Custom Linter のセットアップ & 実行方法](#3-custom-linter-のセットアップ--実行方法)
4. [Streamlit のセットアップ & 実行方法](#4-streamlit-のセットアップ--実行方法)
5. [Godot Engine 4 のセットアップ & 実行方法](#5-godot-engine-4-のセットアップ--実行方法)
6. [推奨開発環境（VSCode & 拡張機能）](#6-推奨開発環境vscode--拡張機能)
7. [よくあるトラブルシューティング](#7-よくあるトラブルシューティング)

---

## 1. 全体概要（単体でのセットアップが可能！）

3つの技術は**完全に独立**しています。自分が制作したい作品・使いたい技術のセクションだけを進めればOKです（例: **「Godotだけ使う」場合はPythonのインストールすら不要**です）。

```
【目的に合わせて選べる3つのコース】
 ├─ 🎮 Godotコース       : GodotのみダウンロードすればOK（Python不要・インストール不要）
 ├─ 🌐 Streamlitコース   : Python + pip でライブラリをインストール
 └─ 🔍 Custom Linterコース: Python標準機能のみで動作（追加インストール不要）
```

| 制作コース | 必要なもの | 不要なもの | 所要時間 |
| :--- | :--- | :--- | :--- |
| **🎮 Godot 2Dゲーム制作** | **Godot 4.x のみ** (zip解凍して実行するだけ) | Python / pip / 各種ライブラリ | 約 3分 |
| **🌐 Streamlit Webアプリ制作** | **Python 3.9+** & `pip install -r requirements.txt` | Godot Engine | 約 5分 |
| **🔍 Custom Linter 制作** | **Python 3.9+ のみ** (追加パッケージ不要) | Godot Engine / Streamlit / pip | 約 2分 |

---

## 2. Python & pip のセットアップ（共通基盤）

Custom Linter および Streamlit の実行には **Python 3.9 以上** が必要です。

### 🔹 Windows の場合

1. **公式サイトからインストーラーをダウンロード**:
   - [python.org/downloads/windows](https://www.python.org/downloads/windows/) から最新の安定版（Python 3.10〜3.12推奨）の `Windows installer (64-bit)` をダウンロードします。
2. **インストール時の重要注意点**:
   - インストーラー起動時に、一番下にある **「Add python.exe to PATH」（PATHにPythonを追加）に必ずチェックを入れてください**。
   - 「Install Now」をクリックしてインストールを完了します。
3. **インストールの確認**:
   - PowerShellまたはコマンドプロンプトを開き、以下を実行します：
   ```powershell
   python --version
   # または
   py --version
   ```
   `Python 3.x.x` と表示されれば成功です！

### 🔹 macOS の場合

1. **Homebrew を使う場合**:
   ```bash
   brew install python
   ```
2. **インストールの確認**:
   ```bash
   python3 --version
   pip3 --version
   ```

---

## 3. Custom Linter のセットアップ & 実行方法

Custom Linter は **Pythonの標準ライブラリ（`ast`, `sys`, `pathlib` 等）のみ** で実装されているため、追加のパッケージインストールなしですぐに動作します。

### 実行手順

1. ターミナルで `custom_linter_demo` フォルダに移動します：
   ```bash
   cd custom_linter_demo
   ```
2. デモスクリプトを解析してみましょう：
   ```bash
   # NG例（意図的にミスを含んだコード）をチェック
   python run_linter.py samples/bad_sample.py

   # OK例（綺麗に書かれたコード）をチェック
   python run_linter.py samples/good_sample.py

   # samples フォルダ全体を一括チェック
   python run_linter.py samples/
   ```
3. ターミナルに色付きで親切な日本語のアドバイスが表示されます！

---

## 4. Streamlit のセットアップ & 実行方法

Streamlit は、Pythonコードだけで美しいWebアプリケーションが作成できるフレームワークです。

### 実行手順

1. ターミナルで `streamlit_demo` フォルダに移動します：
   ```bash
   cd streamlit_demo
   ```
2. **仮想環境（venv）の作成（推奨）**:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **必要なライブラリのインストール**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Streamlit アプリの起動**:
   ```bash
   streamlit run app.py
   ```
5. 自動的にブラウザが立ち上がり、`http://localhost:8501` でWebアプリが表示されます！

---

## 5. Godot Engine 4 のセットアップ & 実行方法

Godot Engine は、軽量で使いやすいオープンソースのゲームエンジンです。インストーラーによるインストール作業が不要で、zipを解凍して実行するだけで起動できます。

### 実行手順

1. **Godot 4 のダウンロード**:
   - [godotengine.org/download](https://godotengine.org/download/) にアクセスします。
   - **「Godot Engine 4.x - Standard version (64-bit)」** をダウンロードします。
2. **解凍と配置**:
   - ダウンロードした zip ファイルを解凍し、出てきた `Godot_v4.x.x_win64.exe` を任意のフォルダ（例: デスクトップや `C:\Tools\Godot\` など）に置きます。
3. **デモプロジェクトの読み込み**:
   - Godot の実行ファイルを開きます。
   - 「プロジェクトマネージャー」画面で、右側の **「インポート (Import)」** ボタンをクリックします。
   - 「参照 (Browse)」を押し、本リポジトリの `godot_demo/project.godot` を選択して「インポートして編集」をクリックします。
4. **ゲームの実行**:
   - Godot エディタ右上の **再生ボタン (▶)** または `F5` キーを押すと、ゲームが起動してプレイできます！

---

## 6. 推奨開発環境（VSCode & 拡張機能）

コードの編集には **Visual Studio Code (VSCode)** の利用を推奨します。

### おすすめのVSCode拡張機能
- **Python** (`ms-python.python`): Pythonの構文ハイライト・デバッグ機能。
- **godot-tools** (`geequlim.godot-tools`): GDScriptの自動補完やシンタックスハイライト。
- **Rainbow Brackets / indent-rainbow**: 括弧やインデントの対応関係が色分けされて見やすくなります。

---

## 7. よくあるトラブルシューティング

### Q1. PowerShellで `Activate.ps1` を実行すると「スクリプトの実行が無効」と怒られる
**解決策**: PowerShellを管理者権限で開き、以下を実行して実行ポリシーを許可してください：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q2. `streamlit` コマンドが見つからないと言われる
**解決策**:
1. 仮想環境が有効化（ターミナルの左端に `(.venv)` と表示）されているか確認してください。
2. もしくは `python -m streamlit run app.py` で実行してみてください。

### Q3. Godotでプロジェクトを開くとエラーが出る
**解決策**:
- 本デモは **Godot 4.x** 向けに作成されています。Godot 3.x ではなく、最新の Godot 4.x を使用しているか確認してください。
