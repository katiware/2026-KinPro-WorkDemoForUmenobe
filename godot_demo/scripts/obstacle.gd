# ==============================================================================
# obstacle.gd: 左右に往復巡回するトラップ・敵ギミック
# ------------------------------------------------------------------------------
# 【役割】
#   ・一定の距離（patrol_distance）を自動で左右に往復移動します。
#   ・プレイヤーが接触したら、プレイヤーの die() 関数を呼んでミスにします。
#
# 【ここを変えるとどう変わるか？】
#   ・speed を 200.0 にする           -> 高速で突進してくる回避の難しい敵になります。
#   ・patrol_distance を 300.0 にする -> 長い直線通路を警備するトラップになります。
# ==============================================================================
extends Area2D

class_name ObstacleHazard

# --- 巡回パラメータ ---
@export var patrol_distance: float = 120.0  # 初期位置からの左右往復移動距離 (px)
@export var speed: float = 80.0             # 移動速度 (px/s)

var start_x: float = 0.0
var direction: int = 1  # 1: 右向き移動, -1: 左向き移動


func _ready() -> void:
	start_x = position.x
	# プレイヤーとの接触検知シグナルを接続
	body_entered.connect(_on_body_entered)


func _process(delta: float) -> void:
	# 指定方向へ進む
	position.x += direction * speed * delta

	# 右端の折り返し地点に到達したら左向きへ反転
	if position.x > start_x + patrol_distance:
		position.x = start_x + patrol_distance
		direction = -1
	# 左端の折り返し地点に到達したら右向きへ反転
	elif position.x < start_x - patrol_distance:
		position.x = start_x - patrol_distance
		direction = 1


# プレイヤーと接触したときのコールバック
func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		body.die("トラップに当たってしまいました！")
