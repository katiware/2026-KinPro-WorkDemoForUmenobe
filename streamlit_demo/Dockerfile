# ==============================================================================
# Streamlit Webアプリ用 Dockerfile
# ------------------------------------------------------------------------------
# 【役割】
#   ホストPCにPythonやライブラリを直接インストールすることなく、
#   コンテナ内でStreamlitサーバーを起動し、ブラウザ（ポート8501）からアクセスできるようにします。
# ==============================================================================

FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージ定義をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# Streamlitのデフォルトポート
EXPOSE 8501

# ヘルスチェック
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Streamlitサーバーの起動（外部アクセスを許可）
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
