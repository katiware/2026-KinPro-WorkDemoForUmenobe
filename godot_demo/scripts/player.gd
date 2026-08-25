# player.gd: プレイヤーの移動、ジャンプ、当たり判定の処理
extends CharacterBody2D

class_name Player

@export var speed: float = 320.0             # 水平移動速度 (px/s)
@export var jump_velocity: float = -480.0    # ジャンプ初速
@export var gravity: float = 1200.0          # 重力加速度
@export var max_fall_speed: float = 800.0    # 最大落下速度

@onready var visual_rect: ColorRect = $VisualRect
var is_alive: bool = true


func _physics_process(delta: float) -> void:
	if not is_alive:
		return

	# 重力の適用
	if not is_on_floor():
		velocity.y += gravity * delta
		if velocity.y > max_fall_speed:
			velocity.y = max_fall_speed

	# ジャンプ入力
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity
		# ジャンプ時のちょっとしたアニメーション演出（縦伸び）
		visual_rect.scale = Vector2(0.8, 1.2)

	# 左右移動入力 (A/D または ←/→)
	var direction := Input.get_axis("move_left", "move_right")
	if direction != 0:
		velocity.x = direction * speed
	else:
		# 減速（摩擦）
		velocity.x = move_toward(velocity.x, 0, speed * 10 * delta)

	# アニメーションスケールの復元
	visual_rect.scale = visual_rect.scale.lerp(Vector2.ONE, delta * 12.0)

	# 移動と衝突の実行 (CharacterBody2D標準メソッド)
	move_and_slide()

	# 画面外（奈落）への落下判定
	if global_position.y > 800:
		die("穴に落下しました！")


# プレイヤー死亡処理
func die(reason: String = "トラップに衝突しました！") -> void:
	if not is_alive:
		return
	
	is_alive = false
	velocity = Vector2.ZERO
	# 点滅・縮小演出
	visual_rect.color = Color(1.0, 0.2, 0.2, 0.8)
	visual_rect.scale = Vector2(0.5, 0.5)

	# GameManager に通知
	var gm = get_tree().get_first_node_in_group("game_manager")
	if gm and gm.has_method("trigger_game_over"):
		gm.trigger_game_over(reason)
