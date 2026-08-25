# good_sample.py: 改善後の模範的なサンプルコード

from typing import Optional

# マジックナンバーを意味のある定数として定義
LUCKY_BONUS_SCORE = 777
MAX_RETRIES = 3


def calculate_score(player_score: int, bonus_multiplier: float) -> int:
    """プレイヤーのスコアにボーナスとラッキーボーナスを加算して計算する。"""
    final_score = int(player_score * bonus_multiplier) + LUCKY_BONUS_SCORE
    return final_score


def run_game_loop() -> None:
    """ゲームループを実行する（適切な終了条件付き）。"""
    print("ゲームを開始します...")
    count = 0
    while True:
        print(f"ステップ {count} を処理中...")
        count += 1
        if count >= MAX_RETRIES:
            print("規定ループ回数に達したため終了します。")
            break


def load_user_data(file_path: str = "user_data.txt") -> Optional[str]:
    """ユーザーデータを読み込む（例外を適切にハンドリング）。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"情報: ファイル `{file_path}` が見つかりませんでした。初期状態で起動します。")
        return None
    except Exception as e:
        print(f"エラー: データ読み込み中に予期しないエラーが発生しました: {e}")
        return None


if __name__ == "__main__":
    score = calculate_score(100, 1.5)
    print(f"計算結果スコア: {score}")
    run_game_loop()
