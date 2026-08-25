"""
==============================================================================
KinPro 2026: Streamlit Creative Studio & Game Dynamics Simulator
新入生向け作品制作デモ: インタラクティブ・ゲームパラメータ調整 & シミュレーション Webアプリ
------------------------------------------------------------------------------
【ファイルの役割】
  ・Pythonスクリプト1つで、ブラウザ上にリッチなUI・スライダー・グラフ・シミュレータを展開します。
  ・サイドバーで物理パラメータ（速度、重力、ジャンプ初速など）をリアルタイムに操作できます。
  ・Plotlyを用いて放物線グラフを描画し、AIボットの自動テストプレイ（モンテカルロ法）を行います。
  ・調整した値を Godot 用の GDScript や JSON データとして出力します。

【ここを変えるとどう変わるか？】
  ・st.sidebar 内の st.slider("HP最大値", 1, 10, 3) を追加 -> 新しい入力スライダーが即座に出現します。
  ・st.tabs に新しいタブ名を追加 -> 新しい機能ページ（例: 「サウンド設定」等）を増設できます。
  ・preset の選択肢を増やす -> 独自のパラメータセット（例: 「ボスモード」）を追加できます。
==============================================================================
"""

import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# ページ初期設定 & カスタムCSS
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KinPro 2026 Game Studio Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* メインコンテナの余白調整 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* タイトルとバッジ */
    .hero-container {
        background: linear-gradient(135deg, #1e1e38 0%, #2d1b4e 50%, #172554 100%);
        border-radius: 16px;
        padding: 24px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        background: rgba(99, 102, 241, 0.3);
        border: 1px solid #818cf8;
        color: #c7d2fe;
        margin-bottom: 8px;
    }
    /* カードデザイン */
    .stat-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stat-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .stat-val {
        color: #38bdf8;
        font-size: 1.6rem;
        font-weight: 800;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# ヘッダー表示
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero-container">
    <div class="badge">KinPro 2026 うめの辺祭 作品制作デモ</div>
    <h1 style="margin: 0 0 8px 0; font-size: 2.2rem; font-weight: 800;">🚀 Game Dynamics & Balance Simulator</h1>
    <p style="margin: 0; color: #cbd5e1; font-size: 1.05rem;">
        PythonとStreamlitで制作された、ゲーム物理パラメータのリアルタイム調整・ステージ難易度分析・AIプレイシミュレーションのデモアプリです。
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# サイドバー: プロジェクト設定 & プリセット
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ パラメータ設定")

    preset = st.selectbox(
        "🎮 プリセット選択",
        ["標準アクション (Default)", "月面重力 (Low Gravity)", "高速スピードラン (Speedrun)", "重量級タンク (Heavy Tank)"],
        index=0,
    )

    st.markdown("---")

    if preset == "標準アクション (Default)":
        init_speed = 300
        init_gravity = 980
        init_jump = -450
        init_friction = 0.15
    elif preset == "月面重力 (Low Gravity)":
        init_speed = 220
        init_gravity = 350
        init_jump = -380
        init_friction = 0.05
    elif preset == "高速スピードラン (Speedrun)":
        init_speed = 520
        init_gravity = 1400
        init_jump = -620
        init_friction = 0.25
    else:
        init_speed = 180
        init_gravity = 1800
        init_jump = -500
        init_friction = 0.35

    st.subheader("🏃 プレイヤー物理設定")
    speed = st.slider("移動速度 (px/s)", 100, 800, init_speed, 10)
    gravity = st.slider("重力加速度 (px/s²)", 200, 2500, init_gravity, 50)
    jump_force = st.slider("ジャンプ初速 (px/s)", -1000, -200, init_jump, 25)
    air_resistance = st.slider("空気抵抗係数", 0.0, 0.5, init_friction, 0.01)

    st.markdown("---")
    st.subheader("🗺️ ステージ生成パラメータ")
    stage_length = st.slider("ステージ全長 (m)", 50, 500, 150, 10)
    coin_density = st.slider("コイン配置密度", 1, 10, 5)
    trap_count = st.slider("トラップ・敵の数", 0, 30, 8)

    st.markdown("---")
    st.info("💡 **新入生へのヒント**: スライダーを動かすと、右側のグラフやシミュレーション結果がリアルタイムに更新されます！")


# ─────────────────────────────────────────────────────────────────────────────
# タブレイアウト
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 物理軌道シミュレータ",
    "🗺️ ステージ設計 & 難易度分析",
    "🤖 AIエージェント自動攻略",
    "💾 設定エクスポート (Godot/JSON)"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: 物理軌道シミュレータ
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("🎮 ジャンプ軌道 & 滞空特性のリアルタイム解析")

    # ジャンプ軌道の計算
    t_max = 2 * abs(jump_force) / gravity  # 着地までの理論時間
    t_steps = np.linspace(0, max(0.2, t_max * 1.05), 100)

    # x(t), y(t)
    vx = speed * (1.0 - air_resistance * 0.5)
    x_coords = vx * t_steps
    # y = v0*t + 0.5*g*t^2  (画面座標系ではなく数学座標系: 上向き正)
    v0_y = abs(jump_force)
    y_coords = np.maximum(0, v0_y * t_steps - 0.5 * gravity * (t_steps ** 2))

    max_height = (v0_y ** 2) / (2 * gravity)
    jump_distance = vx * t_max
    air_time = t_max

    # KPIカード
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("🚀 最高到達高度", f"{max_height:.1f} px", f"{'高め' if max_height > 120 else '標準'}")
    with kpi2:
        st.metric("📏 最大ジャンプ飛距離", f"{jump_distance:.1f} px")
    with kpi3:
        st.metric("⏱️ 滞空時間 (Air Time)", f"{air_time:.2f} 秒")
    with kpi4:
        st.metric("💨 初速ベクトル角度", f"{np.degrees(np.arctan2(v0_y, vx)):.1f}°")

    # Plotly 軌道グラフ
    fig_jump = go.Figure()

    # 地面
    fig_jump.add_trace(go.Scatter(
        x=[-20, jump_distance * 1.15],
        y=[0, 0],
        mode="lines",
        name="地面 (Ground)",
        line=dict(color="#64748b", width=3, dash="solid")
    ))

    # ジャンプ軌道
    fig_jump.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode="lines+markers",
        name="ジャンプ弾道 (Trajectory)",
        line=dict(color="#38bdf8", width=4),
        marker=dict(size=4, color="#818cf8")
    ))

    # 最高点マーカー
    fig_jump.add_trace(go.Scatter(
        x=[jump_distance / 2],
        y=[max_height],
        mode="markers+text",
        name="最高点 (Apex)",
        text=[f"Apex: {max_height:.1f}px"],
        textposition="top center",
        marker=dict(size=12, color="#f59e0b", symbol="star")
    ))

    fig_jump.update_layout(
        title="ジャンプ物理解析グラフ (X: 水平距離 px / Y: 垂直高度 px)",
        xaxis_title="水平移動距離 (px)",
        yaxis_title="高さ (px)",
        template="plotly_dark",
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
    )
    st.plotly_chart(fig_jump, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: ステージ設計 & 難易度分析
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("🗺️ ステージ自動レイアウト & バランススコア")

    np.random.seed(42)
    # ステージ要素の疑似生成
    num_coins = int(stage_length * coin_density / 10)
    coin_x = np.random.uniform(5, stage_length - 5, num_coins)
    coin_y = np.random.uniform(1, 4, num_coins)

    trap_x = np.random.uniform(10, stage_length - 10, trap_count)
    trap_y = np.zeros(trap_count)

    # 難易度スコア計算
    density_factor = trap_count / (stage_length / 10)
    jump_req_factor = max(1.0, 150 / (max_height + 1))
    difficulty_score = min(100, int(density_factor * 35 + jump_req_factor * 25 + (speed / 800) * 15))

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("### 📊 ステージ評価メトリクス")
        st.metric("⚠️ 推定クリア難易度", f"{difficulty_score} / 100",
                  "激ムズ！" if difficulty_score > 75 else ("中級" if difficulty_score > 40 else "初心者向け"))
        st.metric("🪙 総配置コイン数", f"{num_coins} 枚")
        st.metric("⚡ トラップ遭遇率", f"約 {stage_length / max(1, trap_count):.1f} mに1回")

        st.progress(difficulty_score / 100)

    with col_right:
        # ステージ2Dマッププレビュー
        fig_stage = go.Figure()

        # 地面
        fig_stage.add_trace(go.Scatter(
            x=[0, stage_length], y=[0, 0],
            mode="lines", name="地面", line=dict(color="#475569", width=6)
        ))

        # ゴールフラグ
        fig_stage.add_trace(go.Scatter(
            x=[stage_length], y=[1],
            mode="markers+text", name="GOAL",
            text=["🏁 GOAL"], textposition="top center",
            marker=dict(size=14, color="#22c55e", symbol="triangle-up")
        ))

        # コイン
        fig_stage.add_trace(go.Scatter(
            x=coin_x, y=coin_y,
            mode="markers", name="コイン (Coins)",
            marker=dict(size=8, color="#eab308", symbol="circle")
        ))

        # トラップ
        fig_stage.add_trace(go.Scatter(
            x=trap_x, y=trap_y,
            mode="markers", name="トラップ (Traps)",
            marker=dict(size=10, color="#ef4444", symbol="x")
        ))

        fig_stage.update_layout(
            title="2Dステージ俯瞰プレビュー (横軸: ステージ進行度 m)",
            xaxis_title="ステージ位置 (m)",
            yaxis_title="高度 (ブロック)",
            yaxis_range=[-0.5, 6],
            template="plotly_dark",
            height=320,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#1e293b",
        )
        st.plotly_chart(fig_stage, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: AIエージェント自動攻略
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("🤖 ボットによる自動テストプレイシミュレーション (モンテカルロ法)")

    st.write("設定したパラメータでAIボットが100回テストプレイを行い、クリア率や平均クリア時間を測定します。")

    if st.button("▶️ シミュレーションを実行する (100試行)", type="primary"):
        with st.spinner("AIエージェントがステージを攻略中..."):
            np.random.seed(int(speed + gravity))
            num_trials = 100

            # プレイヤー能力に応じたクリア判定
            base_skill = (speed / 300) * 0.4 + (abs(jump_force) / 500) * 0.4 - (difficulty_score / 100) * 0.5
            success_probs = np.clip(0.5 + base_skill * 0.3 + np.random.normal(0, 0.15, num_trials), 0.05, 0.98)
            successes = np.random.rand(num_trials) < success_probs

            times = []
            scores = []
            for s in successes:
                if s:
                    t = (stage_length / (speed / 50)) * np.random.uniform(0.85, 1.25)
                    sc = int(num_coins * np.random.uniform(0.6, 1.0) * 100)
                else:
                    t = np.random.uniform(2.0, (stage_length / (speed / 50)) * 0.7)
                    sc = int(num_coins * np.random.uniform(0.1, 0.5) * 100)
                times.append(t)
                scores.append(sc)

            df_sim = pd.DataFrame({
                "Trial": range(1, num_trials + 1),
                "Success": successes,
                "ClearTime": times,
                "Score": scores
            })

            win_rate = (df_sim["Success"].sum() / num_trials) * 100
            avg_time = df_sim[df_sim["Success"]]["ClearTime"].mean() if win_rate > 0 else 0

            res_c1, res_c2, res_c3 = st.columns(3)
            with res_c1:
                st.metric("🏆 ステージクリア率", f"{win_rate:.1f} %", f"{'良好' if win_rate >= 60 else '難易度高'}")
            with res_c2:
                st.metric("⏱️ 平均クリアタイム", f"{avg_time:.2f} 秒")
            with res_c3:
                st.metric("🌟 平均獲得スコア", f"{int(df_sim['Score'].mean()):,} pt")

            # スコア分布ヒストグラム
            fig_hist = px.histogram(
                df_sim, x="Score", color="Success",
                color_discrete_map={True: "#22c55e", False: "#ef4444"},
                title="100試行におけるスコア分布と勝敗",
                labels={"Success": "クリア成否", "Score": "スコア (pt)"},
                template="plotly_dark",
                nbins=20
            )
            fig_hist.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#1e293b")
            st.plotly_chart(fig_hist, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: 設定エクスポート
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("💾 ゲームエンジン向け設定コード生成")
    st.write("調整したパラメータを、Godot 4.x GDScript または JSON 形式でコピー＆ペーストできます。")

    col_gd, col_json = st.columns(2)

    with col_gd:
        st.markdown("#### 🔹 Godot 4.x 用 GDScript コード")
        gd_code = f"""# player_config.gd (Godot 4.x)
# 生成元: KinPro 2026 Streamlit Creative Studio

extends CharacterBody2D

# 物理定数
const SPEED: float = {float(speed)}
const JUMP_VELOCITY: float = {float(jump_force)}
const GRAVITY: float = {float(gravity)}
const AIR_FRICTION: float = {float(air_resistance)}

# ステージ情報
const STAGE_LENGTH_M: float = {float(stage_length)}
const COIN_COUNT: int = {num_coins}
"""
        st.code(gd_code, language="gdscript")

    with col_json:
        st.markdown("#### 🔹 JSON 形式設定データ")
        json_data = {
            "version": "2026.1",
            "preset": preset,
            "physics": {
                "speed": speed,
                "gravity": gravity,
                "jump_force": jump_force,
                "air_resistance": air_resistance,
            },
            "stage": {
                "length_meters": stage_length,
                "coin_density": coin_density,
                "trap_count": trap_count,
                "estimated_difficulty": difficulty_score
            }
        }
        st.code(json.dumps(json_data, indent=2, ensure_ascii=False), language="json")
