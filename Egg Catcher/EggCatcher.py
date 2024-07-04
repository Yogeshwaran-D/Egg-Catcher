from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

canvasWidth = 800
canvasHeight = 400

root = Tk()
c = Canvas(root , width=canvasWidth , height=canvasHeight , background='deep sky blue')
c.create_rectangle(-5, canvasHeight-100, canvasWidth+5, canvasHeight+5, fill="sea green", width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

colorCycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
eggWidth = 45
eggHeight = 55
eggScore = 10
eggSpeed = 500
eggInterval = 4000
difficulty = 0.95
catcherColor = "blue"
catcherWidth = 100
catcherHeight = 100
catcherStartx = canvasWidth / 2 - catcherWidth / 2
catcherStarty = canvasHeight - catcherHeight - 20
catcherStartx2 = catcherStartx + catcherWidth
catcherStarty2 = catcherStarty + catcherHeight

catcher = c.create_arc(catcherStartx, catcherStarty, catcherStartx2, catcherStarty2, start=200, extent=140, style="arc", outline=catcherColor, width=3)
gameFont = font.nametofont("TkFixedFont")
gameFont.config(size=18)

score = 0
scoreText = c.create_text(10, 10, anchor="nw", font=gameFont, fill="darkblue", text="Score: "+ str(score))

livesRemaining = 3
livesText = c.create_text(canvasWidth-10, 10, anchor="ne", font=gameFont, fill="darkblue", text="Lives: "+ str(livesRemaining))

eggs = []

def createEgg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x+eggWidth, y+eggHeight, fill=next(colorCycle), width=0)
    eggs.append(new_egg)
    root.after(eggInterval, createEgg)

def eggDropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    loseALife()
    if livesRemaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: "+ str(score))
        root.destroy()

def moveEggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvasHeight:
            eggDropped(egg)
    root.after(eggSpeed, moveEggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    loseALife()
    if livesRemaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: "+ str(score))
        root.destroy()
def loseALife():
    global livesRemaining
    livesRemaining -= 1
    c.itemconfigure(livesText, text="Lives: "+ str(livesRemaining))

def checkCatch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increaseScore(eggScore)
    root.after(100, checkCatch)

def increaseScore(points):
    global score, eggSpeed, eggInterval
    score += points
    eggSpeed = int(eggSpeed * difficulty)
    eggInterval = int(eggInterval * difficulty)
    c.itemconfigure(scoreText, text="Score: "+ str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvasWidth:
        c.move(catcher, 20, 0)

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, createEgg)
root.after(1000, moveEggs)
root.after(1000, checkCatch)
root.mainloop()
