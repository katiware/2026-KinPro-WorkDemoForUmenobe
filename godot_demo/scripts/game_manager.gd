# game_manager.gd: ゲーム全体の進行・スコア・タイマー・状態管理
extends Node2D

class_name GameManager

# シグナル定義（UIなどの他ノードへ通知）
signal score_updated(new_score: int)
signal coin_collected(current_coins: int, total_coins: int)
signal time_updated(remaining_time: float)
signal game_over(reason: String)
signal stage_cleared(final_score: int, remaining_time: float)

@export var stage_time_limit: float = 45.0  # 制限時間（秒）
@export var coin_points: int = 100          # コイン1枚あたりのスコア

var current_score: int = 0
var collected_coins: int = 0
var total_coins_in_stage: int = 0
var remaining_time: float = 0.0
var is_game_active: bool = false


func _ready() -> void:
	# ステージ内の全コイン数をカウント
	var coins = get_tree().get_nodes_in_group("coins")
	total_coins_in_stage = coins.size()
	
	# 初期化
	remaining_time = stage_time_limit
	current_score = 0
	collected_coins = 0
	is_game_active = true
	
	# 初回UI更新
	score_updated.emit(current_score)
	coin_collected.emit(collected_coins, total_coins_in_stage)
	time_updated.emit(remaining_time)


func _process(delta: float) -> void:
	if not is_game_active:
		# Rキーでいつでもリスタート可能
		if Input.is_action_just_pressed("restart"):
			get_tree().reload_current_scene()
		return
	
	# タイマーカウントダウン
	remaining_time -= delta
	if remaining_time <= 0.0:
		remaining_time = 0.0
		time_updated.emit(remaining_time)
		trigger_game_over("時間切れ！ (Time Out)")
	else:
		time_updated.emit(remaining_time)


# コイン取得時の処理
func on_coin_picked() -> void:
	if not is_game_active:
		return
	
	collected_coins += 1
	current_score += coin_points
	score_updated.emit(current_score)
	coin_collected.emit(collected_coins, total_coins_in_stage)


# ゴール到達時の処理
func on_goal_reached() -> void:
	if not is_game_active:
		return
	
	is_game_active = false
	# 残り時間ボーナス加算
	var time_bonus = int(remaining_time * 20)
	current_score += time_bonus
	score_updated.emit(current_score)
	stage_cleared.emit(current_score, remaining_time)


# ゲームオーバー発生時
func trigger_game_over(reason: String) -> void:
	if not is_game_active:
		return
	
	is_game_active = false
	game_over.emit(reason)
