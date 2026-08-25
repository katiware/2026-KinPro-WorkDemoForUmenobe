# 🛠️ 2026うめの辺祭 新入生作品制作 環境構築完全ガイド

本ガイドは、2026年うめの辺祭（KinPro）での作品制作に向けて、**Godot / Streamlit / CustomTkinter** の環境構築手順をまとめたものです。

---

## 📑 目次
1. [全体概要（単体でのセットアップが可能！）](#1-全体概要単体でのセットアップが可能)
2. [Python & pip のセットアップ（共通基盤）](#2-python--pip-のセットアップ共通基盤)
3. [Godot Engine 4（2Dゲーム制作）のセットアップ & 実行方法](#3-godot-engine-42dゲーム制作のセットアップ--実行方法)
4. [Streamlit（Webアプリ制作）のセットアップ & 実行方法](#4-streamlitwebアプリ制作のセットアップ--実行方法)
5. [CustomTkinter（デスクトップアプリ制作）のセットアップ & 実行方法](#5-customtkinterデスクトップアプリ制作のセットアップ--実行方法)
6. [推奨開発環境（VSCode & 拡張機能）](#6-推奨開発環境vscode--拡張機能)
7. [よくあるトラブルシューティング](#7-よくあるトラブルシューティング)

---

## 1. 全体概要（単体でのセットアップが可能！）

3つの技術は**完全に独立**しています。自分が制作したい作品・使いたい技術のセクションだけを進めればOKです（例: **「Godotだけ使う」場合はPythonのインストールすら不要**です）。
各ファイルの詳細な役割や改造方法は **[FILE_GUIDE.md](./FILE_GUIDE.md)** をご覧ください。

```
【目的に合わせて選べる3つのコース】
 ├─ 🎮 Godotコース          : GodotのみダウンロードすればOK（Python不要・インストール不要）
 ├─ 🌐 Streamlitコース      : Python + pip でライブラリをインストール（Webアプリ制作）
 └─ 🖥️ CustomTkinterコース  : Python + pip でライブラリをインストール（デスクトップアプリ制作）
```

| 制作コース | 作れる作品 | 必要なツール | 所要時間 |
| :--- | :--- | :--- | :--- |
| **🎮 Godot 2Dゲーム制作** | 2Dアクション、パズル、アニメーション | **Godot 4.x のみ** (zip解凍して実行するだけ) | 約 3分 |
| **🌐 Streamlit Webアプリ制作** | Webダッシュボード、分析ツール、オンラインシミュレータ | **Python 3.9+** & `pip install -r requirements.txt` | 約 5分 |
| **🖥️ CustomTkinter デスクトップ制作** | Windowsデスクトップツール、GUIエディタ、管理アプリ | **Python 3.9+** & `pip install -r requirements.txt` | 約 3分 |

---

## 2. Python & pip のセットアップ（共通基盤）

Streamlit および CustomTkinter の実行には **Python 3.9 以上** が必要です（**Godotのみ使う場合はスキップしてOK**です）。

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

---

## 3. Godot Engine 4（2Dゲーム制作）のセットアップ & 実行方法

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
   - Godot エディタ右上の **再生ボタン (▶)** または **`F5` キー** を押すと、ゲームが起動してプレイできます！

---

## 4. Streamlit（Webアプリ制作）のセットアップ & 実行方法

Streamlit は、Pythonコードだけで美しいWebアプリケーションが作成できるフレームワークです。
**ローカル環境で直接動かす方法** と **Docker を使って環境を汚さずに動かす方法** のどちらでも利用可能です！

### 🔹 方法A: ローカルのPythonで動かす場合

1. ターミナルで `streamlit_demo` フォルダに移動します：
   ```bash
   cd streamlit_demo
   ```
2. **必要なライブラリのインストール**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Streamlit アプリの起動**:
   ```bash
   streamlit run app.py
   ```
4. 自動的にブラウザが立ち上がり、`http://localhost:8501` でWebアプリが表示されます！

### 🔹 方法B: 🐳 Docker を使って仮想化して動かす場合（おすすめ！）
ホストPCに Python や pip パッケージをインストールすることなく、Dockerコンテナ内でStreamlitを起動できます。

1. プロジェクトのルートディレクトリで以下を実行します：
   ```bash
   docker compose up streamlit
   ```
2. ブラウザで `http://localhost:8501` を開くだけでアプリが利用できます！
   - ホスト側の `streamlit_demo/app.py` を編集すると、コンテナ内のWeb画面にも自動で即座に反映（ホットリロード）されます。

---

## 5. CustomTkinter（デスクトップアプリ制作）のセットアップ & 実行方法

CustomTkinter は、Pythonでモダンなダークテーマ・美しいGUIウィンドウを持つデスクトップアプリケーションを作成できるフレームワークです。

### 実行手順

1. ターミナルで `customtkinter_demo` フォルダに移動します：
   ```bash
   cd customtkinter_demo
   ```
2. **必要なライブラリのインストール**:
   ```bash
   pip install -r requirements.txt
   ```
3. **デスクトップアプリの起動**:
   ```bash
   python app.py
   ```
4. Windows上にモダンなGUIウィンドウが立ち上がります！

### 💡 単体 .exe ファイルへのビルド方法 (PyInstaller)
制作したデスクトップアプリは、Python未インストールのPCでも動くように `.exe` に変換できます：
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile app.py
```
👉 `dist/` フォルダの中に `app.exe` が生成されます！

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
`python -m streamlit run app.py` で実行してみてください。

### Q3. Godotでプロジェクトを開くとエラーが出る
**解決策**:
本デモは **Godot 4.x** 向けに作成されています。Godot 3.x ではなく、最新の Godot 4.x を使用しているか確認してください。
