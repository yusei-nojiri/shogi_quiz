from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "shogi-quiz-secret-key"

questions = [
    {
        "question": "次の一手を選んでください。",
        "choices": ["▲7六歩", "▲2六歩", "▲5六歩"],
        "answer": "2",
        "explanation": "飛車先の歩を進め、攻撃の準備をする手です。"
    },
    {
        "question": "次のうち、振り飛車の戦法は？",
        "choices": ["矢倉", "四間飛車", "角換わり"],
        "answer": "2",
        "explanation": "四間飛車は飛車を4筋に振る振り飛車の戦法です。"
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

questions[0]["board"] = board1
questions[1]["board"] = board2


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        question_index = int(request.form.get("question_index"))
        question = questions[question_index]
        answer = request.form.get("answer")

        if answer == question["answer"]:
            session["score"] += 1
            result = "correct"
        else:
            result = "wrong"

        return redirect(
            url_for(
                "home",
                q=question_index,
                result=result
            )
        )

    # ここからGETの処理
    q = request.args.get("q")

    if q is None:
        question_index = 0
        session["score"] = 0
    else:
        question_index = int(q)

    question = questions[question_index]

    result_code = request.args.get("result")

    if result_code == "correct":
        result = "正解！"
    elif result_code == "wrong":
        result = "不正解！"
    else:
        result = None

    correct_choice = None

    if result:
        correct_choice = question["choices"][int(question["answer"]) - 1]

    return render_template(
        "index.html",
        question=question,
        result=result,
        correct_choice=correct_choice,
        question_index=question_index,
        total_questions=len(questions),
        score=session.get("score", 0),
        board=question["board"]
    )


@app.route("/result")
def result():
    score = session.get("score", 0)

    return render_template(
        "result.html",
        score=score,
        total_questions=len(questions)
    )


if __name__ == "__main__":
    app.run(debug=True)