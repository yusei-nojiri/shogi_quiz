questions = [
    {
        "question": "角道を開ける一手はどれ？",
        "choices": ["▲7六歩", "▲2六歩", "▲5六歩"],
        "answer": "1",
        "explanation": "▲7六歩と指すことで、先手の角の斜めの道が開きます。",
        "correct_square": [5, 2]
    },
    {
        "question": "この局面で1マス前に進んでいる先手の駒は？",
        "choices": ["歩", "角", "飛"],
        "answer": "1",
        "explanation": "先手の歩が初期位置から1マス前に進んでいます。"
    },
    {
        "question": "飛車先の歩を進める一手はどれ？",
        "choices": ["▲2六歩", "▲6六歩", "▲4六歩"],
        "answer": "1",
        "explanation": "▲2六歩と指すことで、飛車先の歩を進めます。",
        "correct_square": [5, 7]
    }
]

board1 = [
    [("香", "gote"), ("桂", "gote"), ("銀", "gote"), ("金", "gote"), ("玉", "gote"), ("金", "gote"), ("銀", "gote"), ("桂", "gote"), ("香", "gote")],
    [("", ""), ("飛", "gote"), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("角", "gote"), ("", "")],
    [("歩", "gote"), ("歩", "gote"), ("歩", "gote"), ("歩", "gote"), ("歩", "gote"), ("歩", "gote"), ("歩", "gote"), ("歩", "gote"), ("歩", "gote")],
    [("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", "")],
    [("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", "")],
    [("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", "")],
    [("歩", "sente"), ("歩", "sente"), ("歩", "sente"), ("歩", "sente"), ("歩", "sente"), ("歩", "sente"), ("歩", "sente"), ("歩", "sente"), ("歩", "sente")],
    [("", ""), ("角", "sente"), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("飛", "sente"), ("", "")],
    [("香", "sente"), ("桂", "sente"), ("銀", "sente"), ("金", "sente"), ("玉", "sente"), ("金", "sente"), ("銀", "sente"), ("桂", "sente"), ("香", "sente")]
]
board2 = [row.copy() for row in board1]
board2[6][2] = ("", "")
board2[5][2] = ("歩", "sente")

board1_answer = [row.copy() for row in board1]
board1_answer[6][2] = ("", "")
board1_answer[5][2] = ("歩", "sente")

board3 = [row.copy() for row in board1_answer]

board3_answer = [row.copy() for row in board3]
board3_answer[6][7] = ("", "")
board3_answer[5][7] = ("歩", "sente")

questions[0]["board"] = board1
questions[1]["board"] = board2
questions[2]["board"] = board3

questions[0]["answer_board"] = board1_answer
questions[2]["answer_board"] = board3_answer