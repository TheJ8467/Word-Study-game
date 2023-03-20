
BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
import pandas
import random

window = Tk()
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("words_to_learn.csv")                ## 모르는 단어만 저장한 것에서 데이터를 끌어온다.
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")    ## 맨 처음 실행시 다운받은 데이터에서 끌어와서 시작한다.
    to_learn = original_data.to_dict(orient="records")          ## 그 다운받은 데이터로 리스트화된 딕셔너리 데이터 프레임을 만든다.
else:
    to_learn = data.to_dict(orient="records")                   ## 처음 실행이 아니아서 try가 무사히 실행되면 원래 의도대로 모르는 단어 저장된 파일에서 데이터를 만든다.

def is_known():
    to_learn.remove(current_card)                               ## 실행될 경우 최초의 to_learn 또는 기존의 to_learn에서 현재의 카드에 해당하는 글자 셋트 삭제
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)                           ## to_learn을 csv로 넣기 위해 다시 DF화
    data.to_csv("words_to_learn.csv", index=False)              ## index가 매번 추가되는 것을 막고 csv 파일로 생성
    next_card()                                                 ## 아는 단어이므로 다음 단어로 넘어가게함

# -----------Make Saving----------------------#

# def save():
#     saved_list = []
#     try:
#         with open("words_to_learn.csv", "r") as study_file:
#             study_list = study_file.readlines()
#     except:
#         with open("words_to_learn.csv", "w") as study_file:
#             for n in word_dict.items():
#                 study_file.write(f"{n[0]}, {n[1]}\n")
#     else:
#         random_french_in_english = word_dict[random_french]
#         study_list.remove(f"{random_french}, {random_french_in_english}\n")
#         print(f"{random_french}, {random_french_in_english}\n")
#     finally:
#         for n in study_list:
#             saved_list += n
#         with open("words_to_learn.csv", "w") as study_file:
#             for m in saved_list:
#                 study_file.write(m)
# -----------Make Flash Card----------------------#
def next_card ():
    global timer
    global current_card
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(image_canvas, image=front_image)
    canvas.itemconfig(title_canvas, text="French", fill="black")
    canvas.itemconfig(word_canvas, text=current_card["French"], fill="black")
    timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(image_canvas, image=back_image)
    canvas.itemconfig(title_canvas, text="English", fill="white")
    canvas.itemconfig(word_canvas, text=current_card["English"], fill="white")

timer = window.after(3000, flip_card)

# def button_click():
#     next_card()

# -----------Make UI----------------------#

window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


front_image = PhotoImage(file="images/card_front.png")
image_canvas = canvas.create_image(400, 263, image=front_image)
title_canvas = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_canvas = canvas.create_text(400, 253, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

back_image = PhotoImage(file="images/card_back.png")
x_mark = Button(text="💀", font=("Arial", "50"), command=next_card, highlightbackground=BACKGROUND_COLOR)
x_mark.grid(column=0, row=1)
check_mark = Button(text="🐐", font=("Arial", "50"), command=is_known,  highlightbackground=BACKGROUND_COLOR)
check_mark.grid(column=1, row=1)

next_card ()

window.mainloop()