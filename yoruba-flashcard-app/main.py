from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}  # placeholder variable
words_to_learn = {} #placeholder variable

# Reading the yoruba_words.csv or words_to_learn file (if they have already tried the app atleast 1 time) and getting
# all the words/translations as a list of dictionaries
try:
    yoruba_words = pandas.read_csv("data/yoruba_words_to_learn.csv")
except FileNotFoundError:
    original_yoruba_words = pandas.read_csv("data/yoruba_words.csv")
    words_to_learn = original_yoruba_words.to_dict(orient="records")
else:
    words_to_learn = yoruba_words.to_dict(orient="records")


# Creating a function that generates a random Yoruba word and puts it into the flash card.
def generate_word():
    global current_card, flip_timer
    # Everytime the user generates a new card, the timer resets
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    random_yoruba = current_card['Yoruba']
    # Everytime the wrong or right buttons are pressed, it generates a new yoruba word and
    # resets the card back to the front
    canvas.itemconfig(flashcard_side,image=card_front)
    canvas.itemconfig(card_title, text="Yoruba", fill="black")
    canvas.itemconfig(card_word, text=random_yoruba, fill="black")
    flip_timer = window.after(5000, func=flip_card)  # now the timer can run


# Created a function to get hold of the current card's english translation, and then
# puts it onto the flash card

def flip_card():
    canvas.itemconfig(flashcard_side,image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white")

# Created a function to remove the current card if the user presses the "correct" or check
# button, meaning that they know the yoruba word
def knows_card():
    words_to_learn.remove(current_card)
    not_known_data = pandas.DataFrame(words_to_learn)
    not_known_data.to_csv("data/yoruba_words_to_learn.csv",index=False)
    generate_word()


# Window settings
window = Tk()
window.title("Learn Yoruba: Flash Card App")
window.config(padx=50, pady=50,bg=BACKGROUND_COLOR)

# Gives the user 5 seconds (I entered it as milliseconds) to guess the yoruba word, and then it flips the card
flip_timer = window.after(5000,func=flip_card)

# Canvas settings and adding front/back flashcards to the window
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
flashcard_side = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
# Creating the text for the front of the card; Yoruba and then a yoruba word
card_title = canvas.create_text(400, 150, text="Langauge", fill="black", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", fill="black", font=("Ariel", 60, "bold"))

# Creating the buttons for user the click if they got the word right or wrong
wrong_image = PhotoImage(file="images/wrong.png")
right_image = PhotoImage(file="images/right.png")

wrong_button = Button(image=wrong_image, highlightthickness=0,command=generate_word)
right_button = Button(image=right_image, highlightthickness=0,command=knows_card)
wrong_button.grid(column=0, row=1)
right_button.grid(column=1, row=1)


# When the program first runs, it shows "word" instead of yoruba word, to change that I have to call the
# generate_word function so that it shows a yoruba word on the first run
generate_word()


window.mainloop()

