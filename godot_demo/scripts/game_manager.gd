# ==============================================================================
# game_manager.gd: ゲーム全体のルール・スコア・タイマー・勝敗進行管理
# ------------------------------------------------------------------------------
# 【役割】
#   ・ステージの残り時間タイマーを減算し、0秒でゲームオーバーを発動します。
#   ・コイン取得時にスコアを加算し、ゴール到達時にタイムボーナスを合算します。
#   ・UIノードに対してシグナル（合図）を送信して画面表示を更新します。
#   ・ゲーム終了後、Rキーでいつでもステージをリスタートできるようにします。
#
# 【ここを変えるとどう変わるか？】
#   ・stage_time_limit を 30.0 にする -> 制限時間が厳しくなりスリリングな難易度になります。
#   ・coin_points を 500 にする        -> コイン1枚の価値が上がり、スコアアタックが熱くなります。
# ==============================================================================
extends Node2D

class_name GameManager

# --- 他ノード（UIなど）へ状況の変化を伝えるシグナル定義 ---
signal score_updated(new_score: int)
signal coin_collected(current_coins: int, total_coins: int)
signal time_updated(remaining_time: float)
signal game_over(reason: String)
signal stage_cleared(final_score: int, remaining_time: float)

# --- ゲームルール設定（インスペクターで変更可能） ---
@export var stage_time_limit: float = 45.0  # ステージの制限時間（秒）
@export var coin_points: int = 100          # コイン1枚取得時の加算スコア

# 内部状態
var current_score: int = 0
var collected_coins: int = 0
var total_coins_in_stage: int = 0
var remaining_time: float = 0.0
var is_game_active: bool = false


func _ready() -> void:
	# ステージ内に存在する全コインを "coins" グループから取得・集計
	var coins = get_tree().get_nodes_in_group("coins")
	total_coins_in_stage = coins.size()
	
	# ゲーム開始の初期化
	remaining_time = stage_time_limit
	current_score = 0
	collected_coins = 0
	is_game_active = true
	
	# 初回の状態をUIへ送信
	score_updated.emit(current_score)
	coin_collected.emit(collected_coins, total_coins_in_stage)
	time_updated.emit(remaining_time)


func _process(delta: float) -> void:
	# ゲーム終了状態（クリアまたはゲームオーバー）のとき
	if not is_game_active:
		# Rキーが押されたら現在のシーンを再読み込みしてリトライ
		if Input.is_action_just_pressed("restart"):
			get_tree().reload_current_scene()
		return
	
	# 毎フレーム制限時間を減算（カウントダウン）
	remaining_time -= delta
	if remaining_time <= 0.0:
		remaining_time = 0.0
		time_updated.emit(remaining_time)
		trigger_game_over("時間切れ！ (Time Out)")
	else:
		time_updated.emit(remaining_time)


# コイン取得時に coin.gd から呼び出される関数
func on_coin_picked() -> void:
	if not is_game_active:
		return
	
	collected_coins += 1
	current_score += coin_points
	score_updated.emit(current_score)
	coin_collected.emit(collected_coins, total_coins_in_stage)


# ゴール到達時に goal.gd から呼び出される関数
func on_goal_reached() -> void:
	if not is_game_active:
		return
	
	is_game_active = false
	# 残り時間ボーナス（残り秒数 × 20点）をスコアに上乗せ
	var time_bonus = int(remaining_time * 20)
	current_score += time_bonus
	score_updated.emit(current_score)
	stage_cleared.emit(current_score, remaining_time)


# ゲームオーバー発生時に player.gd や タイマーから呼び出される関数
func trigger_game_over(reason: String) -> void:
	if not is_game_active:
		return
	
	is_game_active = false
	game_over.emit(reason)
