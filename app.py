import os
import secrets
import random
from flask import Flask, render_template, request, session, redirect, url_for
from questions import questions
from database import save_answer, get_category_stats, get_review_question_ids, init_db

app = Flask(__name__)

app.secret_key = os.environ.get("SHOGI_SECRET_KEY") or secrets.token_hex(32)

init_db()



@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        try:
            question_index = int(request.form.get("question_index"))
        except (ValueError, TypeError):
            return redirect(url_for("home"))

        question_order = session.get("question_order")

        if not question_order:
            return redirect(url_for("home"))

        if not (0 <= question_index < len(question_order)):
            return redirect(url_for("home"))

        question = questions[question_order[question_index]]
        
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
        try:
            answer_number = int(answer)
        except (ValueError, TypeError):
            return redirect(url_for("home", q=question_index))

        if not (1 <= answer_number <= len(question["choices"])):
            return redirect(url_for("home", q=question_index))

        answer = str(answer_number)

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
        # SQLiteに解答履歴を保存
        save_answer(
            question_id=question["id"],
            category=question["category"],
            selected=answer,
            is_correct=(answer == question["answer"])
        )

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
        session["mode"] = "normal"
        question_order = list(range(len(questions)))
        random.shuffle(question_order)
        session["question_order"] = question_order

    else:
        try:
            question_index = int(q)
        except ValueError:
            return redirect(url_for("home"))

    # ここからはifとelseの共通処理
    question_order = session.get("question_order")

    if not question_order:
        return redirect(url_for("home"))

    if not (0 <= question_index < len(question_order)):
        return redirect(url_for("home"))

    question = questions[question_order[question_index]]

    if question_order is None:
        return redirect(url_for("home"))

    question = questions[question_order[question_index]]

    result_code = request.args.get("result")
    selected = request.args.get("selected")

    if result_code == "correct":
        result = "正解！"
    elif result_code == "wrong":
        result = "不正解！"
    else:
        result = None
    
    display_board = question["board"]
    display_hands = question.get("hands")

    if result and question.get("answer_board"):
        display_board = question["answer_board"]

    if result and question.get("answer_hands") is not None:
        display_hands = question["answer_hands"]
   
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
        total_questions=len(question_order),
        score=session.get("score", 0),
        board=display_board,
        hands=display_hands,
        mode=session.get("mode", "normal")
    )


@app.route("/result")
def result():
    score = session.get("score", 0)
    question_order = session.get("question_order", [])

    total = len(question_order)
    correct_rate = round(score / total * 100) if total > 0 else 0

    answers = session.get("answers", [])
    answer_results = []

    for item in answers:
        question_index = item["question_index"]
        question = questions[question_order[question_index]]

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
        total_questions=total,
        correct_rate=correct_rate,
        answer_results=answer_results
    )

@app.route("/stats")
def stats_page():
    stats = get_category_stats()

    return render_template("stats.html", stats=stats)

@app.route("/review")
def review_page():
    review_ids = get_review_question_ids()

    review_indices = []

    for index, question in enumerate(questions):
        if question["id"] in review_ids:
            review_indices.append(index)

    # 復習候補がない場合
    if not review_indices:
        return render_template("review_empty.html")


    # 復習問題の出題順をシャッフル
    random.shuffle(review_indices)

    # 復習モードを設定
    session["mode"] = "review"
    session["question_order"] = review_indices

    # スコアと回答履歴をリセット
    session["score"] = 0
    session["answers"] = []

    # 復習問題の1問目へ移動
    return redirect(url_for("home", q=0))


if __name__ == "__main__":
    app.run(debug=False)