from random import choice, sample, shuffle
from json import loads
from time import sleep

from termcolor import colored


tp = int(input("만약 첫번째 유형(보기에서 고르기)를 하실거면 1, 두번째 유형(문장에 단어 그냥 박기)를 하실거면 2를 입력하세요: "))
if tp == 1:
    with open("words1.json", "r", encoding="utf-8") as f:
        quiz = loads(f.read())
elif tp == 2:
    with open("words2.json", "r", encoding="utf-8") as f:
        quiz = loads(f.read())
else:
    print("[검열] 난독증있냐? 1이나 2만 입력해라")
    exit()

meanings = []
for i in quiz:
    meanings.append(i["word"])

N = int(input(f"몇 문제를 푸실 건가요? (전체 {len(quiz)} 문제) "))
print("\n")

if N > len(quiz):
    print(f"[검열]아 {len(quiz)}개 이하로 입력해라")
    exit()

ans = 0

for i in range(N):
    question = choice(quiz)
    quiz.remove(question)

    print(f"{colored(f"#{i + 1}.", "green")} {question['quiz']}")
    if tp == 2:
        print(f"{colored("의미:", "grey")} {question['korean_meaning']}\n")

    if tp == 1:
        choices = sample(meanings, 4)
        choices.append(question["word"])
        shuffle(choices)
    
        print(" ".join(map(lambda x: f"{colored(str(x[0]), "grey")}. {x[1]}", enumerate(choices, 1))))
        print()

    answer = input("답을 입력하세요: ")
    if answer == question["answer"]:
        print(colored("정답입니다!", "green"))
        ans += 1
    else:
        print(f"{colored("틀렸습니다.", "red")} 정답은 {colored(question["answer"], "yellow")} 입니다.")
    print()
    print("문제의 뜻과 예문은 다음과 같습니다.")
    print(f"{colored("뜻:", "grey")} {question["word"]} -> {question["meaning"]}")
    print(f"{colored("예문:", "grey")} {question["sentence"]}")
    print("\n")

    sleep(1)

print(f"총 {colored(str(N), "yellow")}문제 중 {colored(str(ans), "yellow")}문제를 맞추셨습니다.")
if ans < N // 2:
    print("절반이다 틀리다니 [검열]이네요! 공부나 다시하세요")
elif N // 2 < ans < N //3 * 2:
    print("[검열] 신세는 면하셨군요! 하지만 수행평가 만점을 받기엔 어림도 없죠!")
elif N == ans:
    print("영어의 귀재군요!")
