import random
import pygame
import math
from tkinter import *

# global vars
pygame.init()
pygame.font.init()
global e, wordItem
# game vars
hangman_status = 0
guessed = []
wordSet1 = {"VOLUNTEER", "DETECTIVE", "PARTY", "VISUAL", "NOTHING"}
# word pos
WORD_X, WORD_Y = 400, 200
ENDGAMEWORD_X, ENDGAMEWORD_Y = 325, 150
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()
run = True

# fonts
LETTER_FONT = pygame.font.SysFont('arial', 25)
WORD_FONT = pygame.font.SysFont('arial', 40)

file1 = open("userInput.txt", "r")
wordSet2 = set(line.strip() for line in open("userInput.txt"))
file1.close()
wordSet3 = wordSet2.union(wordSet1)
wordItem: str = random.sample(wordSet3, k=1)[0]


# display circle
def draw():
    win.fill(WHITE)
    text = WORD_FONT.render("HANGMAN!", 1, BLACK)
    win.blit(text, (310, 5))
    display_word = ""
    for letter in wordItem:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (WORD_X, WORD_Y))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (25, 50))
    pygame.display.update()


def draw_menu():
    menuList = ["Hangman!", "Play", "Add", "Exit"]

    win.fill(WHITE)
    text = WORD_FONT.render(menuList[0], 1, BLACK)
    win.blit(text, (300, 5))

    text = WORD_FONT.render(menuList[1], 1, BLACK)
    win.blit(text, (350, 200))

    text = WORD_FONT.render(menuList[2], 1, BLACK)
    win.blit(text, (350, 275))

    text = WORD_FONT.render(menuList[3], 1, BLACK)
    win.blit(text, (350, 350))
    win.blit(images[0], (25, 50))
    pygame.display.update()


# tkinter gui adds word to text file and puts it in word set 3
def input_to_text_file():
    s = e.get()
    if s == '':
        label4 = Label(root, text="You added nothing").grid(row=6, column=2)
    if s != '':
        file1 = open("userInput.txt", "a")
        file1.write(s.upper() + "\n")
        file1.close()

        # read file
        file1 = open("userInput.txt", "r")
        wordSet2 = set(line.strip() for line in open("userInput.txt"))
        file1.close()
        wordSet3 = wordSet2.union(wordSet1)
        wordItem = random.sample(wordSet3, k=1)[0]
        label3 = Label(root, text="Your word has been added!").grid(row=6, column=2)


def print_word_bank():
    label2 = Label(root, text="brother this don't work").grid(row=7, column=2)


# actual game/setup display

WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button vars
RADIUS = 20
GAP = 15
letters = []
startX = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
startY = 400
A: int = 65
for i in range(26):
    x = startX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = startY + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# load image
images = []
for i in range(8):
    image = pygame.image.load("image" + str(i) + ".png")
    images.append(image)
    print(images)

# Game loop
while run:
    clock.tick(FPS)
    while hangman_status == 0:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
                if 500 > mouse_x_pos > 300 and 270 > mouse_y_pos > 200:
                    pygame.time.delay(1000)
                    hangman_status = 1
                elif 500 > mouse_x_pos > 300 and 345 > mouse_y_pos > 275:
                    pygame.time.delay(1000)
                    # tkinter pop
                    root = Tk()
                    root.title('Add Words')
                    root.geometry("215x200")
                    label1 = Label(root, text="Enter your word that you'd like to add:")
                    label1.grid(row=0, column=2)

                    e = Entry(root, width=25, borderwidth=5)
                    button1 = Button(root, text='Enter', command=input_to_text_file)
                    button2 = Button(root, text='Show word bank', command=print_word_bank)

                    button1.grid(row=2, column=2)
                    button2.grid(row=3, column=2)

                    e.grid(row=1, column=2)

                    root.mainloop()
                elif 500 > mouse_x_pos > 300 and 420 > mouse_y_pos > 350:
                    pygame.time.delay(1000)
                    pygame.quit()

    while hangman_status >= 1 and hangman_status <= 7:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        distance = math.sqrt((x - mouse_x_pos) ** 2 + (y - mouse_y_pos) ** 2)
                        if distance < RADIUS:
                            letters.pop(letters.index(letter))
                            guessed.append(ltr)
                            if ltr not in wordItem:
                                hangman_status += 1

        won = True
        if hangman_status == 7:
            break
        elif won:
            break

    for letter in wordItem:
        if letter not in guessed:
            won = False
            break

    if won:
        pygame.time.delay(2000)
        win.fill(WHITE)
        text = WORD_FONT.render("You Won!", 1, BLACK)
        win.blit(text, (ENDGAMEWORD_X, ENDGAMEWORD_Y))
        pygame.display.update()

        pygame.time.delay(3000)
        break
    if hangman_status == 7:
        win.fill(WHITE)
        text = WORD_FONT.render("You lost!", 1, BLACK)
        win.blit(text, (ENDGAMEWORD_X, ENDGAMEWORD_Y))
        win.blit(images[7], (25, 50))
        pygame.time.delay(2000)
        pygame.display.update()
        pygame.time.delay(3000)
        break

pygame.quit()
