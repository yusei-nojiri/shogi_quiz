from flask import Flask, render_template, request, session, redirect, url_for
from questions import questions

app = Flask(__name__)
app.secret_key = "shogi-quiz-secret-key"



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
            for item in answers:
                if item["question_index"] == question_index:
                    previous_result = "correct" if item["correct"] else "wrong"

                    return redirect(
                        url_for(
                            "home",
                            q=question_index,
                            result=previous_result,
                            selected=item["selected"]
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