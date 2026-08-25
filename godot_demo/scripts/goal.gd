# goal.gd: ゴールフラグ判定
extends Area2D

class_name GoalGate

func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		var gm = get_tree().get_first_node_in_group("game_manager")
		if gm and gm.has_method("on_goal_reached"):
			gm.on_goal_reached()
