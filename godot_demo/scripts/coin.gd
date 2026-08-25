# ==============================================================================
# coin.gd: 収集アイテム（コイン・クリスタル）の浮遊演出と取得判定
# ------------------------------------------------------------------------------
# 【役割】
#   ・三角関数（sin波）を使ってコインをふわふわ上下に浮遊アニメーションさせます。
#   ・プレイヤーが接触した瞬間に GameManager に得点加算を依頼し、自身を消滅させます。
#
# 【ここを変えるとどう変わるか？】
#   ・bob_amplitude を 15.0 にする -> コインが大きく上下にゆらゆら動きます。
#   ・bob_frequency を 8.0 にする  -> コインが小刻みに素早く振動します。
# ==============================================================================
extends Area2D

class_name CoinItem

# --- 浮遊アニメーション設定 ---
@export var bob_amplitude: float = 6.0   # 上下に揺れる幅 (ピクセル単位)
@export var bob_frequency: float = 3.0   # 揺れる速さ (周波数)

var initial_y: float = 0.0
var time_passed: float = 0.0


func _ready() -> void:
	initial_y = position.y
	# コイングループに登録（GameManagerが全コイン数を数えるため）
	add_to_group("coins")
	# プレイヤーとの接触検知シグナルを接続
	body_entered.connect(_on_body_entered)


func _process(delta: float) -> void:
	time_passed += delta
	# サイン波 (sin) による滑らかな浮遊移動
	position.y = initial_y + sin(time_passed * bob_frequency) * bob_amplitude


# プレイヤー（CharacterBody2D）が接触したときのコールバック
func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		# GameManager ノードを探してコイン獲得を通知
		var gm = get_tree().get_first_node_in_group("game_manager")
		if gm and gm.has_method("on_coin_picked"):
			gm.on_coin_picked()

		# コイン自身をシーンから消去（取得演出）
		queue_free()
