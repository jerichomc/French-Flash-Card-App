import pandas
from tkinter import *
from tkinter import messagebox
import random

current_card = {}
BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}

#--------------------------DATA-------------------------#
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv") #saves table as data frame
    to_learn = original_data.to_dict(orient="records") #if words_to_learn doesnt exist yet it will use this code
else:
    to_learn = data.to_dict(orient="records") #orient records gives a list of dictionaries of each key and their corresponding word



#-------------------------FUNCTIONS----------------------------#
def next_card():
    global current_card #modifies global current card variable so it will be usable later
    current_card = random.choice(to_learn)
    # print(current_card["French"])
    # print(current_card["English"])
    canvas.itemconfig(card_title, text="French") #changes the title to french
    canvas.itemconfig(card_word, text=current_card["French"])
    canvas.itemconfig(card_background, image=flash_front)

def flip_card():
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_card["English"])
    canvas.itemconfig(card_background, image=flash_back)

def is_known():
    to_learn.remove(current_card) #removes known cards from dictionary
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False) #permanently keeps the words you need to learn in a csv file
    #with the line above, index=False means that it wont save the index number to the csv file

#------------------------UI------------------------------#

window = Tk()
window.title("Flash Cards")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# window.after(10000, func=flip_card) #does this function every 10 seconds

canvas = Canvas(width=1000, height=800,bg=BACKGROUND_COLOR, highlightthickness=0)
flash_back = PhotoImage(file="./images/card_back.png")
flash_front = PhotoImage(file="./images/card_front.png")
card_background = canvas.create_image(500, 350, image=flash_front)
canvas.grid(row=1, column=1)

card_title = canvas.create_text(500, 220, text="", font=("Ariel", 36, "italic"))
card_word = canvas.create_text(500, 344, text="", font=("Ariel", 65, "bold"))


check_mark = PhotoImage(file="./images/right.png")
yes_button = Button(image=check_mark, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
yes_button.place(x=220, y=650)

x_mark = PhotoImage(file="./images/wrong.png")
no_button = Button(image=x_mark, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
no_button.place(x=675, y=650)

flip_button = Button(text="Flip Card", height=4, width=8, command=flip_card)
flip_button.place(x=479, y= 680)

next_card()

window.mainloop()