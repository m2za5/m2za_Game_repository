import tkinter as tk
import random

index = False
timer = False
score = False
highScore = False
nextDrink = False

cursorX = False
cursorY = False
mouseX = False
mouseY = False
mouseClick = False

def mouseMove(z):
    global mouseX, mouseY
    mouseX = z.x
    mouseY = z.y

def mouseClicked(z):
    global mouseClick
    mouseClick = 1

drink = []
drinkCheck = []
for i in range(10):
    drink.append([0, 0, 0, 0, 0, 0, 0, 0])
    drinkCheck.append([0, 0, 0, 0, 0, 0, 0, 0])

def drawDrink():
    canvas.delete("DRINK")
    for j in range(10):
        for i in range(8):
            if drink[j][i] > 0:
                canvas.create_image(i * 72 + 60, j * 72 + 60, image=drinkPic[drink[j][i]], tag="DRINK")

def isItRightDrink():
    for j in range(10):
        for i in range(8):
            drinkCheck[j][i] = drink[j][i]

    for j in range(1, 9):
        for i in range(8):
            if drinkCheck[j][i] > 0:
                if drinkCheck[j - 1][i] == drinkCheck[j][i] and drinkCheck[j + 1][i] == drinkCheck[j][i]:
                    drink[j - 1][i] = 7
                    drink[j][i] = 7
                    drink[j + 1][i] = 7

    for j in range(10):
        for i in range(1, 7):
            if drinkCheck[j][i] > 0:
                if drinkCheck[j][i - 1] == drinkCheck[j][i] and drinkCheck[j][i + 1] == drinkCheck[j][i]:
                    drink[j][i - 1] = 7
                    drink[j][i] = 7
                    drink[j][i + 1] = 7

    for j in range(1, 9):
        for i in range(1, 7):
            if drinkCheck[j][i] > 0:
                if drinkCheck[j - 1][i - 1] == drinkCheck[j][i] and drinkCheck[j + 1][i + 1] == drinkCheck[j][i]:
                    drink[j - 1][i - 1] = 7
                    drink[j][i] = 7
                    drink[j + 1][i + 1] = 7
                if drinkCheck[j + 1][i - 1] == drinkCheck[j][i] and drinkCheck[j - 1][i + 1] == drinkCheck[j][i]:
                    drink[j + 1][i - 1] = 7
                    drink[j][i] = 7
                    drink[j - 1][i + 1] = 7

def drinkLine():
    numOfDel = 0
    for j in range(10):
        for i in range(8):
            if drink[j][i] == 7:
                drink[j][i] = 0
                numOfDel += 1
    return numOfDel

def drinkFall():
    notFall = False
    for j in range(8, -1, -1):
        for i in range(8):
            if drink[j][i] != 0 and drink[j + 1][i] == 0:
                drink[j + 1][i] = drink[j][i]
                drink[j][i] = 0
                notFall = True
    return notFall

def failGame():
    for i in range(8):
        if drink[0][i] > 0:
            return True
    return False

def failLineDrink():
    for i in range(8):
        drink[0][i] = random.randint(0, 6)

def cafeGameText(txt, x, y, siz, col, tg):
    fnt = ("DungGeunMo", siz)
    canvas.create_text(x + 2, y + 2, text=txt, fill="black", font=fnt, tag=tg)
    canvas.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

def mainGame():
    global index, timer, score, highScore, nextDrink
    global cursorX, cursorY, mouseClick
    if index == 0:
        cafeGameText("Cafe Game", 312, 240, 80, "violet", "TITLE")
        cafeGameText("Click to start.", 312, 560, 50, "orange", "TITLE")
        index = 1
        mouseClick = 0
    elif index == 1:
        if mouseClick == 1:
            for j in range(10):
                for i in range(8):
                    drink[j][i] = 0

            mouseClick = 0
            score = 0
            nextDrink = 0
            cursorX = 0
            cursorY = 0
            failLineDrink()
            drawDrink()
            canvas.delete("TITLE")
            index = 2

    elif index == 2:
        if drinkFall() == False:
            index = 3
        drawDrink()

    elif index == 3:
        isItRightDrink()
        drawDrink()
        index = 4

    elif index == 4:
        delNumOFDL = drinkLine()
        score = score + delNumOFDL * 10
        if score > highScore:
            highScore = score
        if delNumOFDL > 0:
            index = 2
        else:
            if failGame() == False:
                nextDrink = random.randint(1, 6)
                index = 5
            else:
                index = 6
    elif index == 5:
        if 24 <= mouseX and mouseX < 24 + 72 * 8 and 24 <= mouseY and mouseY < 24 + 72 * 10:
            cursorX = int((mouseX - 24) / 72)
            cursorY = int((mouseY - 24) / 72)
            if mouseClick == 1:
                mouseClick = 0
                failLineDrink()
                drink[cursorY][cursorX] = nextDrink
                nextDrink = 0
                index = 2
        canvas.delete("CURSOR")
        canvas.create_image(cursorX * 72 + 60, cursorY * 72 + 60, image=cursor, tag="CURSOR")
        drawDrink()
    elif index == 6:
        timer = timer + 1
        if timer == 1:
            cafeGameText("GAME OVER", 312, 348, 60, "red", "OVER")
        if timer == 50:
            canvas.delete("OVER")
            index = 0
    canvas.delete("INFO")
    if score is not False:  # score가 설정되지 않았을 때 "score false" 표시 방지
        cafeGameText("High Score " + str(highScore), 450, 60, 32, "yellow", "INFO")
        cafeGameText("SCORE " + str(score), 160, 60, 32, "blue", "INFO")
    if nextDrink > 0:
        canvas.create_image(752, 128, image=drinkPic[nextDrink], tag="INFO")
    mainHandling.after(100, mainGame)

mainHandling = tk.Tk()
mainHandling.title("CAFE GAME")
mainHandling.geometry("912x768")
mainHandling.resizable(False, False)
mainHandling.bind("<Motion>", mouseMove)
mainHandling.bind("<ButtonPress>", mouseClicked)
canvas = tk.Canvas(mainHandling, width=912, height=768)
canvas.pack()

background = tk.PhotoImage(file="background.png")
cursor = tk.PhotoImage(file="cursor.png")
drinkPic = [
    None,
    tk.PhotoImage(file="coffee.png"),
    tk.PhotoImage(file="latte.png"),
    tk.PhotoImage(file="choco.png"),
    tk.PhotoImage(file="oreo.png"),
    tk.PhotoImage(file="strawberry.png"),
    tk.PhotoImage(file="greentea.png"),
    tk.PhotoImage(file="boom!.png")
]

canvas.create_image(456, 384, image=background)
mainGame()
mainHandling.mainloop()