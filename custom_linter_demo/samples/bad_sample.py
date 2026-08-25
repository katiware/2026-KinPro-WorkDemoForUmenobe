# bad_sample.py: 初心者が陥りがちなミスが含まれるサンプルコード

def calculateScore(playerScore, bonusMultiplier):
    # RULE-004: 関数名・変数名がキャメルケースになっている
    # RULE-002: マジックナンバー (777) が直接式に埋め込まれている
    finalScore = playerScore * bonusMultiplier + 777
    return finalScore


def runGameLoop():
    # RULE-001: breakのない while True (無限ループの危険性)
    print("ゲームを開始します...")
    while True:
        print("処理中...")


def loadUserData():
    try:
        with open("user_data.txt", "r") as f:
            data = f.read()
    except Exception:
        # RULE-003: 例外の握りつぶし (pass)
        pass


# RULE-005: if __name__ == '__main__': なしで直接関数を呼び出している
runGameLoop()
