# ui.gd: ゲームHUD（スコア、コイン、残り時間、ゲームオーバー/クリア画面）
extends CanvasLayer

@onready var score_label: Label = $HUD/ScoreLabel
@onready var coin_label: Label = $HUD/CoinLabel
@onready var timer_label: Label = $HUD/TimerLabel
@onready var result_panel: Panel = $ResultPanel
@onready var result_title: Label = $ResultPanel/ResultTitle
@onready var result_desc: Label = $ResultPanel/ResultDesc
@onready var restart_button: Button = $ResultPanel/RestartButton


func _ready() -> void:
	result_panel.visible = false
	restart_button.pressed.connect(_on_restart_pressed)

	# GameManager とシグナル接続
	var gm = get_tree().get_first_node_in_group("game_manager")
	if gm:
		gm.score_updated.connect(_update_score)
		gm.coin_collected.connect(_update_coins)
		gm.time_updated.connect(_update_timer)
		gm.game_over.connect(_show_game_over)
		gm.stage_cleared.connect(_show_stage_clear)


func _update_score(score: int) -> void:
	score_label.text = "🏆 スコア: %d" % score


func _update_coins(current: int, total: int) -> void:
	coin_label.text = "🪙 コイン: %d / %d" % [current, total]


func _update_timer(time: float) -> void:
	timer_label.text = "⏱️ 残り時間: %.1f 秒" % time
	if time <= 10.0:
		timer_label.modulate = Color(1.0, 0.3, 0.3)
	else:
		timer_label.modulate = Color.WHITE


func _show_game_over(reason: String) -> void:
	result_panel.visible = true
	result_title.text = "💥 GAME OVER"
	result_title.modulate = Color(1.0, 0.3, 0.3)
	result_desc.text = "%s\n\n[ R キー ] または下のボタンで再挑戦！" % reason


func _show_stage_clear(final_score: int, remaining_time: float) -> void:
	result_panel.visible = true
	result_title.text = "🎉 STAGE CLEAR!"
	result_title.modulate = Color(0.3, 1.0, 0.4)
	result_desc.text = "おめでとうございます！\n最終スコア: %d pt\n残り時間ボーナス: +%d pt\n\n[ R キー ] でもう一度プレイ！" % [
		final_score,
		int(remaining_time * 20)
	]


func _on_restart_pressed() -> void:
	get_tree().reload_current_scene()
