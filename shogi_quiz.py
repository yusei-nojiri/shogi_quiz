question1 = {
    "question": "次の一手を選んでください。",
    "choices": ["▲7六歩", "▲2六歩", "▲5六歩"],
    "answer": "2",
    "explanation": "飛車先の歩を進め、攻撃の準備をする手です。"
}
question2 = {
    "question": "次のうち、振り飛車の戦法は？",
    "choices": ["矢倉", "四間飛車", "角換わり"],
    "answer": "2",
    "explanation": "四間飛車は飛車を4筋に振る振り飛車の戦法です。"
}
questions = [
    question1,
    question2
]

def ask_question(q):
    print(q["question"])

    for number, choice in enumerate(q["choices"], start=1):
        print(number, ":", choice)
    while True:
            ans = input("回答を入力してください：")
            if ans.isdigit() and 1 <= int(ans) <= len(q["choices"]):
                break
            print("1〜", len(q["choices"]), "の数字を入力してください。")
    
    if ans == q["answer"]:
        print("正解")
        print(q["explanation"])
        print()
        return True
    else:
        print("不正解")
        print("正解は",q["answer"],":",q["choices"][int(q["answer"])-1],"です。")
        print(q["explanation"])
        print()
        return False



def run_quiz(questions):
    score = 0
    for question_number, q in enumerate(questions, start=1):
    
        print("問題", question_number)
        
        if ask_question(q):
            score+=1
        
        
    print("最終結果:", len(questions), "問中", score, "問正解")
    rate = score / len(questions) * 100
    print("正答率:", rate, "%")
        
if __name__ == "__main__":
    run_quiz(questions)