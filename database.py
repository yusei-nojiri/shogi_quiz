import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("shogi_quiz.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS answer_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id TEXT NOT NULL,
            category TEXT NOT NULL,
            selected TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            answered_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_answer(question_id, category, selected, is_correct):
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO answer_history
        (question_id, category, selected, is_correct)
        VALUES (?, ?, ?, ?)
    """, (question_id, category, selected, int(is_correct)))

    conn.commit()
    conn.close()

def get_category_stats():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute("""
        SELECT
            category,
            COUNT(*) AS total,
            SUM(is_correct) AS correct_count,
            ROUND(100.0 * SUM(is_correct) / COUNT(*), 1) AS correct_rate
        FROM answer_history
        GROUP BY category
    """)

    stats = cursor.fetchall()

    conn.close()

    return stats

def get_review_question_ids():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute("""
        SELECT question_id
        FROM answer_history AS a
        WHERE is_correct = 0
        AND id = (
          SELECT MAX(id)
          FROM answer_history AS b
          WHERE b.question_id = a.question_id
        )
        ORDER BY question_id
    """)

    question_ids = []

    for row in cursor.fetchall():
        question_ids.append(row[0])

    conn.close()

    return question_ids

if __name__ == "__main__":
    init_db()
    print("データベースの初期化が完了しました！")

    # 解答履歴の保存テスト
    #save_answer("q004", "受け", "2", True)
    #print("テスト用の解答履歴を保存しました！")
    # データベースに接続
    conn = sqlite3.connect(DB_PATH)

    # テーブルの情報を取得
    cursor = conn.execute("PRAGMA table_info(answer_history)")

    # 取得した情報を表示
    for column in cursor.fetchall():
        print(column[1], column[2])

    conn.close()

    # 保存した解答履歴を確認
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute("""
        SELECT *
        FROM answer_history
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    print("最新の解答履歴：", row)
    # 解答履歴の件数を取得
    count = conn.execute("SELECT COUNT(*) FROM answer_history").fetchone()[0]
    print("保存済みの解答数：", count)

    # 関数を使ってカテゴリ別成績を取得
    stats = get_category_stats()

    for category, total, correct_count, correct_rate in stats:
        print(category, total, correct_count, correct_rate)

    # 関数を使って復習候補を取得
    review_ids = get_review_question_ids()

    print("復習候補：", review_ids)

    conn.close()
