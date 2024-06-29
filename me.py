from random import choice, sample, shuffle
from json import loads
from time import sleep
from termcolor import colored
from time import time

sleepTime = 0.6666
while True:
    try:
        tp = int(input("만약 문장 암기 첫 번째 유형(보기에서 고르기)를 하실 거면 1, 문장 암기 두 번째 유형(보기 없이 쓰기)를 하실 거면 2, 단어 암기를 하시려면 3, 설정에 들어가려면 4를 입력하세요: "))
    except ValueError:
        print("잘못된 입력입니다.")
        exit()
    if tp<=3: break
    if tp>=5:
        print("잘못된 입력입니다.")
        exit()
    print("아무것도 입력하지 않으면 스킵됩니다.")
    try:
        ins = input("문제 사이 대기 시간 설정 (초): "+str(sleepTime)+" -> ")
        if ins == "": raise ArithmeticError
        sleepTime = float()
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
    elif tp == 3:
        print("외울 단어 목록을 고르세요: 1. 클래스카드, 2. 기말범위")
        try:
            temp = int(input())
        except ValueError:
            print("잘못된 입력입니다.")
            exit()
        if temp==1:
            with open("words0.json", "r", encoding="utf-8") as f:
                quiz = loads(f.read())
        elif temp==2:
            with open("words00.json", "r", encoding="utf-8") as f:
                quiz = loads(f.read())
    else:
        print("잘못된 입력입니다.")
        exit()
except FileNotFoundError:
    print("파일을 찾지 못했습니다.")
    exit()
ttp = -1
if tp == 3:
    print("모드를 선택하세요: 1. 보기 중 단어 고르기, 2. 보기 없이 단어 쓰기, 3. 보기 중 뜻 고르기")
    try:
        ttp = int(input())
    except ValueError:
        print("잘못된 입력입니다.")
        exit()

meanings = []
if tp <= 2 or ttp != 3:
    for i in quiz:
        meanings.append(i["word"])
else:
    for i in quiz:
        meanings.append(i["meaning"])
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
quiz_str = 'quiz' if tp<=2 else 'meaning'
ans_str = 'answer' if tp<=2 else 'word'
if ttp==3:
    quiz_str = 'word'
    ans_str = 'meaning'
for i in range(N):
    question = choice(quiz)
    quiz.remove(question)

    print(f"{colored(f"#{i + 1}.", "green")} {question[quiz_str]}")
    if tp == 2:
        print(f"{colored("의미:", "white")} {question['korean_meaning']}\n")

    if tp == 1 or ttp==1:
        choices = sample(meanings, 4)
        while question["word"] in choices:
            choices = sample(meanings, 4)
        choices.append(question["word"])
        shuffle(choices)

        print(" ".join(map(lambda x: f"{colored(str(x[0]), "white")}. {x[1]}", enumerate(choices, 1))))
        print()
    choices=[]
    if ttp==3:
        choices = sample(meanings, 4)
        while question["meaning"] in choices:
            choices = sample(meanings, 4)
        choices.append(question["meaning"])
        shuffle(choices)
        print(' ',end='')
        print(" ".join(map(lambda x: f"{colored(str(x[0]), "white")}. {x[1]}\n", enumerate(choices, 1))))
        print()

    temp = time()
    answer = input("답을 입력하세요: ")
    try:
        test = int(answer)
        if ttp != 3:
            print("단어를 입력해야 합니다.")
            exit()
        elif ttp==3:
            answer = choices[test-1]
    except ValueError:
        if ttp == 3:
            print("숫자를 입력해야 합니다.")
            exit()
    if answer == question[ans_str]:
        combo += 1
        tsc=score
        combonus = (combo//5+5)/5
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
        print(f"정답은 {colored(question[ans_str], "yellow")} 입니다.")
        st = f"{colored("예문:", "white")} {question["sentence"]}" if tp<=2 else ""
        review.append(str(answer) + "(X), " + str(question[ans_str]) + "(O)\n"+f"{colored("뜻:", "white")} {question["word"]} -> {question["meaning"]}\n"+st)
    if tp<=2:
        print("\n문제의 뜻과 예문은 다음과 같습니다.")
        print(f"{colored("뜻:", "white")} {question["word"]} -> {question["meaning"]}")
        print(f"{colored("예문:", "white")} {question["sentence"]}")
    print('\n')
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
