# ==============================================================================
# player.gd: プレイヤーキャラクターの物理挙動・操作・状態制御
# ------------------------------------------------------------------------------
# 【役割】
#   ・キーボード（WASD / 矢印キー / スペース）入力を受け取り、2D物理運動を計算します。
#   ・ジャンプ時の伸縮演出、床や壁との衝突判定、穴への転落死、敵との接触死を管理します。
#
# 【ここを変えるとどう変わるか？】
#   ・speed を大きくする（例: 500.0）   -> 足が速くなり、爽快なダッシュ移動になります。
#   ・jump_velocity を小さくする（例: -650.0） -> より高く大ジャンプできるようになります。
#   ・gravity を小さくする（例: 600.0） -> 月面のようにふわっとゆっくり落下します。
# ==============================================================================
extends CharacterBody2D

class_name Player

# --- 物理パラメータ（エディタのインスペクターからも調整可能） ---
@export var speed: float = 320.0             # 水平移動速度 (px/s)
@export var jump_velocity: float = -480.0    # ジャンプ初速 (上向きはマイナス値)
@export var gravity: float = 1200.0          # 重力加速度 (大きいほど素早く落下)
@export var max_fall_speed: float = 800.0    # 最大落下速度 (落下速度の上限)

# ノード参照と生存フラグ
@onready var visual_rect: ColorRect = $VisualRect
var is_alive: bool = true


func _physics_process(delta: float) -> void:
	if not is_alive:
		return

	# 1. 重力の適用（空中にいる時のみ落下速度を加算）
	if not is_on_floor():
		velocity.y += gravity * delta
		if velocity.y > max_fall_speed:
			velocity.y = max_fall_speed

	# 2. ジャンプ処理（床の上にいる時のみジャンプ可能）
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity
		# ジャンプ時のちょっとしたアニメーション演出（縦に引き伸ばす）
		visual_rect.scale = Vector2(0.8, 1.2)

	# 3. 左右移動入力の取得 (A/D または ←/→)
	var direction := Input.get_axis("move_left", "move_right")
	if direction != 0:
		velocity.x = direction * speed
	else:
		# キーを離したときの摩擦減速
		velocity.x = move_toward(velocity.x, 0, speed * 10 * delta)

	# 4. アニメーションスケールを徐々に通常サイズ (1.0) へ戻す
	visual_rect.scale = visual_rect.scale.lerp(Vector2.ONE, delta * 12.0)

	# 5. 移動と地形衝突の実行 (Godot 4 の標準物理処理)
	move_and_slide()

	# 6. 画面外（奈落の穴）への落下判定（Y座標が 800px を超えたら死亡）
	if global_position.y > 800:
		die("穴に落下しました！")


# プレイヤー死亡処理（敵接触時や奈落落下時に呼び出される）
func die(reason: String = "トラップに衝突しました！") -> void:
	if not is_alive:
		return
	
	is_alive = false
	velocity = Vector2.ZERO
	# 死亡演出: 赤く点滅・縮小
	visual_rect.color = Color(1.0, 0.2, 0.2, 0.8)
	visual_rect.scale = Vector2(0.5, 0.5)

	# ゲーム全体を管理する GameManager にゲームオーバーを通知
	var gm = get_tree().get_first_node_in_group("game_manager")
	if gm and gm.has_method("trigger_game_over"):
		gm.trigger_game_over(reason)
