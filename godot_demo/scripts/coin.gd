# coin.gd: 収集アイテム（コイン/クリスタル）の回転アニメーションと取得判定
extends Area2D

class_name CoinItem

@export var bob_amplitude: float = 6.0   # 上下浮遊の幅 (px)
@export var bob_frequency: float = 3.0   # 浮遊の速さ

var initial_y: float = 0.0
var time_passed: float = 0.0


func _ready() -> void:
	initial_y = position.y
	add_to_group("coins")
	# プレイヤーとの接触検知シグナルを接続
	body_entered.connect(_on_body_entered)


func _process(delta: float) -> void:
	time_passed += delta
	# サイン波でふわふわ浮遊させる
	position.y = initial_y + sin(time_passed * bob_frequency) * bob_amplitude


func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		# GameManager に通知
		var gm = get_tree().get_first_node_in_group("game_manager")
		if gm and gm.has_method("on_coin_picked"):
			gm.on_coin_picked()

		# 消滅エフェクト・ノード破棄
		queue_free()
