# 2026-KinPro-WorkDemoForUmenobe

2026年うめの辺祭における、新入生作品制作用の技術デモおよび環境構築ガイドリポジトリです。

---

## 🚀 デモプロジェクト一覧

新入生が作品制作を行う主要な3つの技術スタックについて、独立したサンプル作品・デモを用意しています。

| ディレクトリ | 制作コース | 内容・作れる作品 | 単独動作 |
| :--- | :--- | :--- | :--- |
| [`godot_demo/`](./godot_demo/) | **🎮 Godot 2Dゲーム制作** | コイン収集・トラップ回避・スコア加算などの基本要素が詰まった、拡張しやすい2Dアクションゲーム | ✅ 単独で完結（Python不要） |
| [`streamlit_demo/`](./streamlit_demo/) | **🌐 Streamlit Webアプリ制作** | インタラクティブなシミュレーションやデータ分析・パラメータ調整ができるリッチなWebアプリケーション | ✅ 単独で完結 |
| [`customtkinter_demo/`](./customtkinter_demo/) | **🖥️ CustomTkinter デスクトップ制作** | ダークモード対応、モダンなGUIコンポーネント、ファイル操作・文字数カウントツール、単一.exe化 | ✅ 単独で完結 |

> 💡 **ポイント**: 各環境は**完全に独立**しています。「Godotだけ触りたい新入生」はPythonのインストールすら不要で、Godotをダウンロードするだけで即座に制作を始められます。

---

## 📖 ガイドドキュメント

新入生が迷わず制作を進められるよう、2つの完全ガイドを用意しています：

- 👉 **[🛠️ 初心者向け 環境構築完全ガイド (SETUP_GUIDE.md)](./SETUP_GUIDE.md)**: 各ツールのインストール・起動手順・トラブルシューティング
- 👉 **[📚 初学者向け ファイル役割＆構造解説ガイド (FILE_GUIDE.md)](./FILE_GUIDE.md)**: 各ファイルが何をしているかの詳細解説・改造逆引き表

---

## 💻 各デモの起動方法

### 1. Godot 2D ゲームデモを実行
1. [Godot 4.x Standard](https://godotengine.org/download/) をダウンロード・解凍
2. Godot を起動し、「インポート」から `godot_demo/project.godot` を選択して実行（`F5` キー）

### 2. Streamlit Webアプリ デモを実行
```bash
# 【方法A: ローカルPythonで動かす場合】
cd streamlit_demo
pip install -r requirements.txt
streamlit run app.py

# 【方法B: 🐳 Dockerで動かす場合（Pythonインストール不要！）】
docker compose up streamlit
# -> ブラウザで http://localhost:8501 にアクセス
```

### 3. CustomTkinter デスクトップアプリ デモを実行
```bash
cd customtkinter_demo
pip install -r requirements.txt
python app.py
```
*(おまけ: `pyinstaller --noconsole --onefile app.py` で単一 `.exe` ファイルを作成可能)*
