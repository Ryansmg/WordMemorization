from random import choice, sample, shuffle
from json import loads
from time import sleep
from termcolor import colored
from time import time
from tkinter import *
import threading

sleepTime = 0.6666
while True:
    try:
        tp = int(input("만약 첫번째 유형(보기에서 고르기)를 하실 거면 1, 두번째 유형(보기 없이 쓰기)를 하실 거면 2, 설정에 들어가려면 3을 입력하세요: "))
    except ValueError:
        print("잘못된 입력입니다.")
        exit()
    if tp<=2: break
    if tp>=4:
        print("잘못된 입력입니다.")
        exit()
    print("아무것도 입력하지 않으면 스킵됩니다.")
    try:
        ins = input("문제 사이 대기 시간 설정 (초): "+str(sleepTime)+" -> ")
        if ins == "": raise ArithmeticError
        sleepTime = float(ins)
    except ValueError:
        print("잘못된 입력입니다.")
    except ArithmeticError:
        pass

try:
    if tp == 1:
        with open("words1.json", "r", encoding="utf-8") as f:
            quiz = loads(f.read())
    elif tp == 2:
        with open("words2.json", "r", encoding="utf-8") as f:
            quiz = loads(f.read())
    else:
        print("잘못된 입력입니다.")
        exit()
except FileNotFoundError:
    print("파일을 찾지 못했습니다.")
    exit()

meanings = []
for i in quiz:
    meanings.append(i["word"])
try:
    N = int(input(f"몇 문제를 푸실 건가요? (전체 {len(quiz)} 문제) "))
except ValueError:
    print("잘못된 입력입니다.")
    exit()
print("\n")

if N > len(quiz):
    print(f"{len(quiz)}개 이하로 입력하세요.")
    exit()

if N < 1:
    print("1개 이상으로 입력하세요.")
    exit()

ans = 0
combo = 0
score = 0
max_combo = 0
review = []

entry = Text()
label = Label()
end = False
def f():
    global entry, label, end
    tk = Tk()
    tk.geometry("333x100")

    label = Label(tk, text="답을 입력하세요 (----):", font=('맑은 고딕',15))
    label.grid(row=0, column=0)
    entry = Text(tk, font=('맑은 고딕',15), width=30)
    entry.grid(row=1,column=0)
    tk.protocol("WM_DELETE_WINDOW")
    tk.mainloop()
    end = True
th = threading.Thread(target=f)
th.start()

for i in range(N):
    question = choice(quiz)
    quiz.remove(question)

    print(f"{colored(f"#{i + 1}.", "green")} {question['quiz']}")
    if tp == 2:
        print(f"{colored("의미:", "white")} {question['korean_meaning']}\n")

    if tp == 1:
        choices = sample(meanings, 4)
        while question["word"] in choices:
            choices = sample(meanings, 4)
        choices.append(question["word"])
        shuffle(choices)

        print(" ".join(map(lambda x: f"{colored(str(x[0]), "white")}. {x[1]}", enumerate(choices, 1))))
        print()

    temp = time()
    combonus = (combo//5+5)/5
    while '\n' not in entry.get(1.0,'end-1c') and not end:
        p = str(int(max(combonus * (20.0 - (time() - temp)) / 20.0 * 1000, 100 * combonus)))
        while len(p) < 4:
            p = '0'+p
        label.config(text='답을 입력하세요 ('+p+"): ")
    answer = entry.get(1.0,'end-1c').strip()
    entry.delete('1.0', END)
    try:
        test = int(answer)
        print("단어를 입력해야 합니다.")
        exit()
    except ValueError: pass
    if answer == question["answer"]:
        combo += 1
        tsc=score
        combostr = ""
        if combonus!=1 :
            combostr = " ("+str(int(combonus*100)/100)+"x)"
        score += int(max(combonus*(20.0-(time()-temp))/20.0*1000, 100*combonus))
        max_combo = max(max_combo, combo)
        print(colored("정답입니다!", "green"), "[ Combo:", combo, "| Score:", str(score)+" (+"+str(score-tsc)+combostr+")","]")
        ans += 1
    else:
        combo = 0
        score -= 100
        print(f"{colored("틀렸습니다.", "red")}", "[ Combo:", combo, "| Score:", str(score)+" (-100)","]")
        print(f"정답은 {colored(question["answer"], "yellow")} 입니다.")
        review.append(str(answer) + "(X), " + str(question["answer"]) + "(O)\n"+f"{colored("뜻:", "white")} {question["word"]} -> {question["meaning"]}\n"+f"{colored("예문:", "white")} {question["sentence"]}")
    print("\n문제의 뜻과 예문은 다음과 같습니다.")
    print(f"{colored("뜻:", "white")} {question["word"]} -> {question["meaning"]}")
    print(f"{colored("예문:", "white")} {question["sentence"]}\n\n")
    sleep(sleepTime)

print(f"총 {colored(str(N), "yellow")}문제 중 {colored(str(ans), "yellow")}문제를 맞추셨습니다.")
if ans < N // 4:
    print("열심히 공부하세요")
elif ans < N // 2:
    print("절반 이상이나 틀리다니..")
elif N // 2 <= ans <= N // 3 * 2:
    print("수행평가 만점을 받기엔 아직 일러요")
elif N == ans:
    print("영어의 귀재군요!")
else:
    print("영어의 범재군요.")
print("[ Max Combo:", max_combo,"| Score:",score,"(avg:",str(score/N)+")",']')

try:
    if input("\n틀린 단어들을 보려면 Enter를 누르세요. (아무거나 입력해 종료)")!="":exit()
except KeyboardInterrupt:exit()
for s in review:
    print(s)
    try:
        if input()!="":exit()
    except KeyboardInterrupt: exit()
