from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "shogi-quiz-secret-key"

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

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        question_index = int(request.form.get("question_index"))
        question = questions[question_index]
        
        answers = session.get("answers", [])

        already_answered = False

        for item in answers:
            if item["question_index"] == question_index:
                already_answered = True
        
        if already_answered:
            return redirect(
                url_for(
                    "home",
                    q=question_index
                )
            )
                
        answer = request.form.get("answer")
        if answer is None:
            return redirect(
                url_for(
                    "home",
                    q=question_index
                )
            )

        if answer == question["answer"]:
            session["score"] += 1
            result = "correct"
        else:
            result = "wrong"
            
        answers = session.get("answers", [])

        answers.append({
            "question_index": question_index,
            "selected": answer,
            "correct": answer == question["answer"]
        })

        session["answers"] = answers

        return redirect(
            url_for(
                "home",
                q=question_index,
                result=result,
                selected=answer
            )
        )

    # ここからGETの処理
    q = request.args.get("q")

    if q is None:
        question_index = 0
        session["score"] = 0
        session["answers"] = []
    else:
        question_index = int(q)

    question = questions[question_index]

    result_code = request.args.get("result")
    selected = request.args.get("selected")

    if result_code == "correct":
        result = "正解！"
    elif result_code == "wrong":
        result = "不正解！"
    else:
        result = None
    
    display_board = question["board"]

    if result and question.get("answer_board"):
        display_board = question["answer_board"]

    correct_choice = None
    selected_choice = None

    if result:
        correct_choice = question["choices"][int(question["answer"]) - 1]

    if selected:
        selected_choice = question["choices"][int(selected) - 1]

    return render_template(
        "index.html",
        question=question,
        result=result,
        correct_choice=correct_choice,
        selected_choice=selected_choice,
        question_index=question_index,
        total_questions=len(questions),
        score=session.get("score", 0),
        board=display_board
    )


@app.route("/result")
def result():
    score = session.get("score", 0)
    correct_rate = round(score / len(questions) * 100)

    answers = session.get("answers", [])
    answer_results = []

    for item in answers:
        question = questions[item["question_index"]]

        selected_choice = question["choices"][int(item["selected"]) - 1]
        correct_choice = question["choices"][int(question["answer"]) - 1]

        answer_results.append({
            "question": question["question"],
            "selected_choice": selected_choice,
            "correct_choice": correct_choice,
            "correct": item["correct"]
        })

    return render_template(
        "result.html",
        score=score,
        total_questions=len(questions),
        correct_rate=correct_rate,
        answer_results=answer_results
    )

if __name__ == "__main__":
    app.run(debug=True)