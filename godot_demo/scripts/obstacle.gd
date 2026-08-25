# obstacle.gd: 左右に往復パトロールするトラップ / 敵ギミック
extends Area2D

class_name ObstacleHazard

@export var patrol_distance: float = 120.0  # 往復する移動距離
@export var speed: float = 80.0             # 移動速度

var start_x: float = 0.0
var direction: int = 1


func _ready() -> void:
	start_x = position.x
	body_entered.connect(_on_body_entered)


func _process(delta: float) -> void:
	position.x += direction * speed * delta

	# 端に到達したら反転
	if position.x > start_x + patrol_distance:
		position.x = start_x + patrol_distance
		direction = -1
	elif position.x < start_x - patrol_distance:
		position.x = start_x - patrol_distance
		direction = 1


func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		body.die("トラップに当たってしまいました！")
