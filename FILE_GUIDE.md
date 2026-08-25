# 📚 初学者向け ファイル役割＆構造 完全解説ガイド

2026年うめの辺祭（KinPro）での作品制作へようこそ！  
このガイドでは、リポジトリ内にある**すべてのファイルに「どんな情報が書かれているのか」「コードのどこを変えたらゲームやアプリがどう変化するのか」**を、初学者向けに具体的に詳しく解説します。

---

## 📑 目次
1. [全体ファイルマップ](#1-全体ファイルマップ)
2. [🎮 Godot 2Dゲーム (`godot_demo/`) のファイル詳細解説](#2-godot-2dゲーム-godot_demo-のファイル詳細解説)
3. [🌐 Streamlit Webアプリ (`streamlit_demo/`) のファイル詳細解説](#3-streamlit-webアプリ-streamlit_demo-のファイル詳細解説)
4. [🖥️ CustomTkinter デスクトップ (`customtkinter_demo/`) のファイル詳細解説](#4-customtkinter-デスクトップ-customtkinter_demo-のファイル詳細解説)
5. [🔄 「ここを変えたらこう変わる！」実践コード変更集](#5-ここを変えたらこう変わる実践コード変更集)

---

## 1. 全体ファイルマップ

```
2026-KinPro-WorkDemoForUmenobe/
├── README.md                      # プロジェクト全体の紹介とクイックスタート
├── SETUP_GUIDE.md                 # 各ツールのインストール・環境構築手順書
├── FILE_GUIDE.md                  # ★ 本ファイル（各ファイルの詳細解説＆変更ガイド）
│
├── godot_demo/                    # 🎮 2Dゲーム制作コース（Godot Engine 4）
│   ├── project.godot              # Godotの根幹設定（解像度、キー設定、起動シーン）
│   ├── icon.svg                   # ゲームのアイコン画像
│   ├── scenes/                    # ゲーム画面に登場する「部品（シーン）」たち
│   │   ├── main.tscn              # ステージ全体（足場、コイン、敵、ゴール、UIを統合）
│   │   ├── player.tscn            # プレイヤーキャラクター（操作・当たり判定）
│   │   ├── coin.tscn              # 集めるコイン（星・クリスタル）
│   │   ├── obstacle.tscn          # 左右に往復するトゲ・敵ギミック
│   │   ├── goal.tscn              # ステージクリアのゴール旗
│   │   └── ui.tscn                # HUD（スコア、タイマー、リザルト画面）
│   ├── scripts/                   # 各部品の「頭脳・動き（GDScriptプログラム）」
│   │   ├── game_manager.gd        # 全体ルール（スコア計算、制限時間、クリア/敗北判定）
│   │   ├── player.gd              # 移動、ジャンプ、重力落下、穴への転落死
│   │   ├── coin.gd                # ふわふわ浮遊アニメーション、取得時の判定
│   │   ├── obstacle.gd            # 往復パトロール移動、衝突死の処理
│   │   ├── goal.gd                # ゴール到達時のシグナル通知
│   │   └── ui.gd                  # 画面上の文字更新、リトライボタンの動作
│   └── README.md                  # 遊び方・起動手順
│
├── streamlit_demo/                # 🌐 Webアプリ制作コース（Streamlit）
│   ├── app.py                     # Webアプリ本体（UI、物理シミュレータ、AI攻略、エクスポート）
│   ├── requirements.txt           # 必要なPythonライブラリ一覧（streamlit, plotly等）
│   ├── Dockerfile                 # 🐳 Streamlitコンテナ化定義ファイル
│   ├── .dockerignore              # 🐳 Dockerビルド時の除外設定
│   └── README.md                  # 起動手順と機能一覧
│
├── customtkinter_demo/            # 🖥️ デスクトップアプリ制作コース（CustomTkinter）
│   ├── app.py                     # デスクトップアプリ本体（ウィンドウ、サイドバー、エディタ）
│   ├── requirements.txt           # 必要なPythonライブラリ一覧（customtkinter, Pillow）
│   └── README.md                  # 起動手順と単一.exe化（PyInstaller）手順
│
└── docker-compose.yml             # 🐳 ワンコマンドでStreamlit等を起動できるDocker Compose設定
```

---

## 2. 🎮 Godot 2Dゲーム (`godot_demo/`) のファイル詳細解説

Godotでは、画面に配置する物体（パーツ）を **「シーン (`.tscn`)」** と呼び、そのパーツの動きやルールを記述するプログラムを **「スクリプト (`.gd`)」** と呼びます。

---

### ⚙️ 設定ファイル

#### `project.godot`
- **何が書いてあるか**:
  - ゲームのタイトル（`config/name="KinPro 2026 2D Game Demo"`）
  - ウィンドウ解像度（横 1152px × 縦 648px）
  - ゲーム起動時に最初に開くメインシーン（`res://scenes/main.tscn`）
  - キーボードの操作割り当て（`move_left` に Aキーと左矢印、`move_right` に Dキーと右矢印、`jump` に スペースキーとWキーと上矢印、`restart` に Rキー）
- **ここを変えるとどう変わるか**:
  - `viewport_width` や `viewport_height` を変更すると、ゲームウィンドウの初期サイズや画面比率が変わります。
  - `[input]` セクションに新しいキーを追加すると、攻撃キー（Zキーなど）やダッシュキー（Shiftキーなど）を新設できます。

#### `icon.svg`
- **何が書いてあるか**: GodotロボットとKinProテーマカラーのベクター画像データ。
- **ここを変えるとどう変わるか**: 画像を差し替えることで、ゲームのアイコンやウィンドウの左上アイコンが変わります。

---

### 🎬 シーンファイル (`scenes/`)

#### `scenes/main.tscn`
- **何が書いてあるか**:
  - ゲーム全体の「親シーン」。`Ground1`（地面）や `Platform1, Platform2, Platform3`（浮遊する足場）の座標・サイズが定義されています。
  - この中に `Player`, `Coins`（5枚のコイン配置）, `Obstacles`（2体の敵配置）, `Goal`, `UI` が子ノードとして埋め込まれています。
- **ここを変えるとどう変わるか**:
  - 足場（Platform）の `position` 座標を変えたりコピペして増やすと、ステージの形（アスレチックコース）を自由自在に作り直せます。

#### `scenes/player.tscn`
- **何が書いてあるか**:
  - `CharacterBody2D`（物理運動できる2Dノード）をルートとし、中に当たり判定（`CollisionShape2D`: 32×32pxの四角形）と見た目の四角形（`VisualRect`: 水色）が入っています。
- **ここを変えるとどう変わるか**:
  - `VisualRect` の `color` を変えるとプレイヤーの色が変わり、`RectangleShape2D` の `size` を変えると当たり判定の大きさが変わります。

#### `scenes/coin.tscn`
- **何が書いてあるか**:
  - `Area2D`（すり抜け可能な接触検知エリア）と、半径12pxの丸い当たり判定（`CircleShape2D`）、45度回転した黄色の四角形が入っています。
- **ここを変えるとどう変わるか**:
  - 色や形を変えてクリスタルや星、ハート（回復アイテム）などの別アイテムに改造できます。

#### `scenes/obstacle.tscn`
- **何が書いてあるか**:
  - プレイヤーが触れるとダメージを受ける `Area2D`。28×28pxの赤い正方形です。
- **ここを変えるとどう変わるか**:
  - 赤い四角からトゲの画像や敵モンスターのスプライトに差し替えることができます。

#### `scenes/goal.tscn`
- **何が書いてあるか**:
  - ゴール用の検知エリア（`Area2D`）と、灰色のポール（`Pole`）、緑色の旗（`Flag`）で構成されています。
- **ここを変えるとどう変わるか**:
  - ポールと旗のサイズや色を変えたり、宝箱やワープポータルの見た目に変えられます。

#### `scenes/ui.tscn`
- **何が書いてあるか**:
  - 画面最前面に固定表示される `CanvasLayer`。
  - 左上にスコアとコイン数、右上に残り時間タイマー、下部に操作案内ラベル、中央にクリア/ゲームオーバー時にポップアップする `ResultPanel` と「もう一度遊ぶ」ボタンが入っています。
- **ここを変えるとどう変わるか**:
  - フォントサイズ（`font_size`）や文字色（`font_color`）、ボタンの配置場所を変更できます。

---

### 📝 スクリプトファイル (`scripts/`)

#### `scripts/player.gd`
- **何が書いてあるか**:
  - プレイヤーの物理変数（`speed`: 移動速度 320、`jump_velocity`: ジャンプ力 -480、`gravity`: 重力 1200、`max_fall_speed`: 終端速度 800）
  - `_physics_process(delta)`: 毎フレーム呼ばれ、キーボード入力に応じて左右に移動し、スペースキーでジャンプさせ、`move_and_slide()` で床や壁と押し引きします。
  - ジャンプ時にキャラクターが縦に少し伸びるアニメーション演出（`visual_rect.scale = Vector2(0.8, 1.2)`）
  - 画面下（Y座標 800px以上）に落ちた時の穴落下死判定 (`die()`)
- **ここを変えるとどう変わるか**:
  - `speed = 500.0` にすると超高速で走るダッシュキャラになります。
  - `jump_velocity = -700.0` にすると画面上部まで大ジャンプできるようになります。
  - `gravity = 500.0` にすると月面のようにふわっと浮遊するジャンプになります。

#### `scripts/game_manager.gd`
- **何が書いてあるか**:
  - ゲーム全体のルール変数（`stage_time_limit`: 制限時間 45.0秒、`coin_points`: コイン1枚 100点）
  - `_process(delta)`: 毎フレーム残り時間を減算し、0秒になったらゲームオーバーを発動。また `R` キーが押されたらシーンを再読み込みして即座にリスタートします。
  - `on_coin_picked()`: コインを取得したときにスコアを加算してUIへシグナル送信。
  - `on_goal_reached()`: ゴール時に「残り時間 × 20点」のタイムボーナスを合算してクリア画面を表示。
- **ここを変えるとどう変わるか**:
  - `stage_time_limit = 30.0` にすると制限時間が厳しくなり、難易度が上がります。
  - `coin_points = 500` にするとコイン1枚の価値が高まり、コイン集めの重要度が上がります。

#### `scripts/coin.gd`
- **何が書いてあるか**:
  - 浮遊パラメータ（`bob_amplitude`: 浮遊の高さ 6.0px、`bob_frequency`: 浮遊の速さ 3.0）
  - `_process(delta)` でサイン波 `sin(time_passed * bob_frequency)` を使って滑らかに上下に揺れます。
  - `_on_body_entered(body)` でプレイヤーが接触した瞬間に GameManager に通知し、`queue_free()` でコイン自身を画面から消滅させます。
- **ここを変えるとどう変わるか**:
  - `bob_frequency = 8.0` にするとコインが細かくプルプル振動するようになります。

#### `scripts/obstacle.gd`
- **何が書いてあるか**:
  - パトロール変数（`patrol_distance`: 往復距離 120.0px、`speed`: 移動速度 80.0px/s）
  - 初期位置から `patrol_distance` だけ右に進んだら左に反転、左端に着いたら右に反転を繰り返します。
  - `_on_body_entered(body)` でプレイヤーがぶつかると即座に `player.die()` を呼び出します。
- **ここを変えるとどう変わるか**:
  - `speed = 200.0` にすると高速で突進してくる強敵になります。
  - `patrol_distance = 300.0` にすると長い通路を巡回する警備トラップになります。

#### `scripts/goal.gd`
- **何が書いてあるか**:
  - プレイヤーが旗のエリアに入ったかを検知し、`GameManager.on_goal_reached()` を呼び出します。

#### `scripts/ui.gd`
- **何が書いてあるか**:
  - GameManager から送られてくるシグナル（スコア更新、タイマー更新、クリア、ゲームオーバー）を受け取り、画面の文字を書き換えます。
  - 残り時間が10秒以下になるとタイマーの文字を赤色（`Color(1.0, 0.3, 0.3)`）に変えて危機感を演出します。
  - リザルトパネルの「もう一度遊ぶ」ボタンがクリックされたらリスタートを実行します。

---

## 3. 🌐 Streamlit Webアプリ (`streamlit_demo/`) のファイル詳細解説

Streamlitは、**Pythonスクリプトを1つ書くだけでWebブラウザ上に本格的なUI・グラフ・操作パネルを展開できる**画期的なフレームワークです。

---

### `streamlit_demo/app.py`
このファイルは、上から下へ順番に実行される構造になっています。

- **行ごとの情報と役割**:
  1. **ページ基本設定 & カスタムCSS (`st.set_page_config`)**:
     - ブラウザのタブ名（`page_title="KinPro 2026 Game Studio Demo"`）やアイコン（🚀）、画面横幅いっぱいに使う `layout="wide"` を設定。
     - 紫・藍色のグラデーション（`linear-gradient`）や角丸カードなどのカスタムスタイルを適用。
  2. **サイドバー設定 (`st.sidebar`)**:
     - `st.selectbox`: 4種類のプリセット（「標準アクション」「月面重力」「高速スピードラン」「重量級タンク」）の選択肢。選択するとスライダーの初期値が一括で切り替わります。
     - `st.slider`: 移動速度（100〜800 px/s）、重力（200〜2500 px/s²）、ジャンプ初速（-1000〜-200 px/s）、ステージ長、コイン密度の入力スライダー。
  3. **タブ1: 📈 物理軌道シミュレータ (`tab1`)**:
     - 数式 `v0_y * t - 0.5 * gravity * t^2` から放物線の各点座標を計算。
     - 最高到達点（Apex）と最大ジャンプ飛距離、滞空時間を算出して KPIカード (`st.metric`) に表示。
     - `plotly.graph_objects.Figure` で暗色テーマ（`plotly_dark`）の美しいリアルタイム弾道グラフを描画。
  4. **タブ2: 🗺️ ステージ設計 & 難易度分析 (`tab2`)**:
     - NumPyの乱数（`np.random`）でステージ上のコインとトラップのX/Y位置を自動生成。
     - トラップ密度とジャンプ要求度からステージの「クリア難易度（0〜100点）」を自動算出し、プログレスバーで表示。
     - 2D俯瞰マップグラフ上に地面・ゴール旗・黄色いコイン・赤いトラップを描画。
  5. **タブ3: 🤖 AIエージェント自動攻略 (`tab3`)**:
     - 「シミュレーションを実行する」ボタンを押すと、AIボットが設定されたステージを100回連続でテストプレイ（モンテカルロシミュレーション）。
     - クリア率（%）、平均タイム（秒）、スコアの分布ヒストグラム（勝敗色分け）を瞬時に集計・グラフ化。
  6. **タブ4: 💾 設定エクスポート (`tab4`)**:
     - スライダーで調整した値を、Godot 4用の `player_config.gd` スクリプトおよび `game_config.json` データとして整形し、ワンクリックでコピーできるようにコードブロック表示。

- **ここを変えるとどう変わるか**:
  - `st.sidebar` に `st.slider("HP最大値", 1, 10, 3)` を1行追加するだけで、画面に新しいスライダーが即座に出現します。
  - `tab1, tab2, tab3, tab4 = st.tabs([...])` に新しいタブ名を追加すれば、オリジナルの機能ページ（例: 「🎵 BGM・サウンド設定」「👾 敵モンスター図鑑」など）を簡単に追加できます。

---

### `streamlit_demo/requirements.txt`
- **何が書いてあるか**:
  - `streamlit`: Web画面を作る本体ライブラリ
  - `plotly`: マウスで拡大・縮小・ホバー値表示ができる高機能グラフライブラリ
  - `pandas`: 表データ（試行結果など）を管理・集計するライブラリ
  - `numpy`: 放物線の軌道計算や乱数生成を高速に行う数値計算ライブラリ
- **ここを変えるとどう変わるか**:
  - 新たに画像処理（`Pillow`）や機械学習（`scikit-learn`）などのライブラリを追記して `pip install -r requirements.txt` することで、さらに高度な機能をアプリに組み込めます。

---

## 4. 🖥️ CustomTkinter デスクトップ (`customtkinter_demo/`) のファイル詳細解説

CustomTkinterは、Pythonで**Windowsネイティブのモダンなウィンドウアプリケーション**を構築できるGUIライブラリです。

---

### `customtkinter_demo/app.py`
クラス構造（オブジェクト指向 `class KinProDesktopApp(ctk.CTk)`）で整理されています。

- **セクションごとの情報と役割**:
  1. **初期化 (`__init__`)**:
     - `self.geometry("1080x680")`: 起動時のウィンドウサイズ（横1080px × 縦680px）。
     - `self.grid_rowconfigure` / `grid_columnconfigure`: ウィンドウの伸縮ルールを設定（横に引き伸ばしたとき右側のメインエリアが自動拡張される）。
     - `self.project_data`: アプリ内で管理する初期データ（プロジェクト名、進捗率、タグ）のリスト。
  2. **サイドバー (`_create_sidebar`)**:
     - 左側の固定ナビゲーションバー。
     - 「📊 ダッシュボード」「📝 エディタ & ツール」「⚙️ 設定 & テーマ」の切り替えボタンを配置。
     - 下部には、ダーク/ライトモード切り替えプルダウン（`CTkOptionMenu`）とUI拡大率（80%/100%/120%）メニューを配置。
  3. **画面切り替えロジック (`_select_frame_by_name`)**:
     - クリックされた画面のフレームだけを `grid(row=0, column=1)` で表示し、他のフレームを `grid_forget()` で隠すことでスムーズなページ遷移を実現。
  4. **ダッシュボード画面 (`_build_dashboard_ui`)**:
     - 3つのKPIカード（進行中作品数、平均進捗、残り日数）。
     - `CTkScrollableFrame`（スクロール可能リスト）内に、タグバッジ、作品名、プログレスバー（`CTkProgressBar`）を一覧表示。
     - 「➕ 新規プロジェクト追加」ボタンを押すと、ポップアップ入力欄（`CTkInputDialog`）が表示され、入力した作品が即座にリストに追加されます。
  5. **エディタ＆ツール画面 (`_build_editor_ui`)**:
     - `CTkTextbox`: フォントに等幅フォント（`Consolas`）を指定したテキスト/コード入力エリア。
     - ツールバー: 「📂 ファイルを開く」（`filedialog.askopenfilename`）、「💾 保存する」（`filedialog.asksaveasfilename`）、「📊 文字数カウント」（文字数・行数・単語数をポップアップ通知）、「🗑️ クリア」ボタン。
  6. **設定画面 (`_build_settings_ui`)**:
     - テーマカラー切り替え（`blue`, `dark-blue`, `green`）。
     - 自動バックアップのトグルスイッチ（`CTkSwitch`）。

- **ここを変えるとどう変わるか**:
  - `ctk.set_appearance_mode("Light")` に書き換えると、初期状態が明るい白基調のアプリになります。
  - `self.geometry("800x600")` に変更すると、コンパクトなウィンドウサイズで起動します。
  - `_build_editor_ui` に「大文字変換ボタン」や「行番号表示機能」などの新機能ボタンを数行で追加できます。

---

## 5. 🔄 「ここを変えたらこう変わる！」実践コード変更集

初学者が「まずはここをいじって遊んでみたい！」というときの具体的な書き換え例です。

### 🎮 Godotの変更例（`godot_demo/scripts/player.gd`）

```gdscript
# 【変更前】標準のジャンプと移動速度
@export var speed: float = 320.0
@export var jump_velocity: float = -480.0
@export var gravity: float = 1200.0

# ⬇️ 【変更後: スピードスター仕様】足がものすごく速く、重力が軽くなる
@export var speed: float = 650.0          # 移動速度が約2倍にアップ！
@export var jump_velocity: float = -600.0  # より高くジャンプ！
@export var gravity: float = 700.0        # ふわっとゆっくり落ちてくる！
```

---

### 🌐 Streamlitの変更例（`streamlit_demo/app.py`）

```python
# 【変更前】プリセットの選択肢
preset = st.selectbox(
    "🎮 プリセット選択",
    ["標準アクション (Default)", "月面重力 (Low Gravity)", "高速スピードラン (Speedrun)", "重量級タンク (Heavy Tank)"],
    index=0
)

# ⬇️ 【変更後】「超巨大ボスモード」を自分で追加！
preset = st.selectbox(
    "🎮 プリセット選択",
    ["標準アクション (Default)", "月面重力 (Low Gravity)", "高速スピードラン (Speedrun)", "重量級タンク (Heavy Tank)", "🔥 超巨大ボスモード (Boss)"],
    index=0
)

# ボスモードのパラメータ定義を追加
if preset == "🔥 超巨大ボスモード (Boss)":
    init_speed = 120      # 巨大なので足は遅い
    init_gravity = 2200   # 超重量級
    init_jump = -750      # 地響きを起こす大ジャンプ
    init_friction = 0.4
```

---

### 🖥️ CustomTkinterの変更例（`customtkinter_demo/app.py`）

```python
# 【変更前】起動時の初期設定
ctk.set_appearance_mode("Dark")       # ダークモード
ctk.set_default_color_theme("blue")  # 青色テーマ

# ⬇️ 【変更後】爽やかなエメラルドグリーン基調のライトモードに変更！
ctk.set_appearance_mode("Light")      # ライトモード（白い背景）
ctk.set_default_color_theme("green")  # ボタンやバーが鮮やかな緑色に！
```
