# ==============================================================================
# goal.gd: ステージクリア地点（ゴールフラグ）の判定
# ------------------------------------------------------------------------------
# 【役割】
#   ・プレイヤーがゴール旗に到達したかを検知し、GameManager にクリアを伝えます。
# ==============================================================================
extends Area2D

class_name GoalGate

func _ready() -> void:
	# プレイヤーとの接触検知シグナルを接続
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		var gm = get_tree().get_first_node_in_group("game_manager")
		if gm and gm.has_method("on_goal_reached"):
			gm.on_goal_reached()
