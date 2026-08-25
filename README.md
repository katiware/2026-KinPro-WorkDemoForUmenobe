# 2026-KinPro-WorkDemoForUmenobe

2026年うめの辺祭における、新入生作品制作用の技術デモおよび環境構築ガイドリポジトリです。

---

## 🚀 デモプロジェクト一覧

新入生が作品制作を行う主要な3つの技術スタックについて、独立したサンプル作品・デモを用意しています。

| ディレクトリ | 制作コース | 必要なもの | 単独動作 |
| :--- | :--- | :--- | :--- |
| [`godot_demo/`](./godot_demo/) | **🎮 Godot 2Dゲーム制作** | **Godot 4.x のみ**（Python不要・インストール不要） | ✅ 単独で完結 |
| [`streamlit_demo/`](./streamlit_demo/) | **🌐 Streamlit Webアプリ制作** | **Python 3.9+** & `requirements.txt` | ✅ 単独で完結 |
| [`custom_linter_demo/`](./custom_linter_demo/) | **🔍 Custom Linter（静的解析）** | **Python 3.9+ のみ**（標準機能のみ・追加pip不要） | ✅ 単独で完結 |

> 💡 **ポイント**: 各環境は**完全に独立**しています。「Godotだけ触りたい新入生」はPythonのインストールすら不要で、Godotをダウンロードするだけで即座に制作を始められます。

---

## 📖 環境構築ガイド

各技術のセットアップ手順、VSCodeの推奨設定、トラブルシューティングは以下に詳しくまとめています：

👉 **[初心者向け 環境構築完全ガイド (SETUP_GUIDE.md)](./SETUP_GUIDE.md)**

---

## 💻 クイックスタート

### 1. Custom Linter デモを実行
```bash
cd custom_linter_demo
python run_linter.py samples/bad_sample.py
```

### 2. Streamlit デモを実行
```bash
cd streamlit_demo
pip install -r requirements.txt
streamlit run app.py
```

### 3. Godot デモを実行
1. [Godot 4.x Standard](https://godotengine.org/download/) をダウンロード
2. Godot を起動し、「インポート」から `godot_demo/project.godot` を選択して実行（F5キー）
