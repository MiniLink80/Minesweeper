import tkinter as tk
from functools import partial
from PIL import ImageTk, Image
import random
import time


#board info
w = 30
h = 20
bombCount = 60
foundBombs = 0
gameOver = False
bombList = []
bg2 = "gray87"


#window initialization
root = tk.Tk()
root.resizable(0,0)

#main panel creation
butPanel = tk.Frame(relief=tk.RAISED, borderwidth=3)
butPanel.pack()

#main list creation
buttonList = [0]*h
for a in range(h):
    buttonList[a] = [0]*w


#loading images
images = {}

#small cells
cellSize = 25
imgSize = 26
pos = 27

"""
#big cells
cellSize = 35
imgSize = 37
pos = 38
"""

for a in range(9):
    #img = Image.open(f"images2/{a}.png")
    #img = img.resize((imgSize,)*2, Image.ANTIALIAS)
    #images[a] = ImageTk.PhotoImage(img)
    #compact form below
    images[a] = ImageTk.PhotoImage(Image.open(f"images/{a}.png").resize((imgSize,)*2, Image.ANTIALIAS))
images["flag"] = ImageTk.PhotoImage(Image.open(f"images/flag.png").resize((imgSize,)*2, Image.ANTIALIAS))
images["bomb"] = ImageTk.PhotoImage(Image.open(f"images/bomb2.png").resize((imgSize,)*2, Image.ANTIALIAS))


class Buttons():
    
    def __init__(self, canv: tk.Canvas(), i, j):
        self.canv = canv
        self.i = i
        self.j = j
        self.bomb = False
        self.val = 0
        self.exposed = False
        self.flagged = False
    

    def Click(self, event):
        global gameOver
        if self.flagged:
            return
        if self.bomb:
            gameOver = True
            print("You lost !")
            #loss
            self.Expose()
            Buttons.ShowAllBombs()
        else:
            if not self.flagged and not gameOver:
                self.RecurExpose()

    def RightClick(self, event):
        global foundBombs, gameOver
        if self.exposed or gameOver:
            return
        if self.flagged:
            self.canv.delete("all")
            self.flagged = False
            if self.bomb:
                foundBombs -= 1
        else:
            self.canv.create_image(pos, pos, anchor="se", image=images["flag"])
            self.flagged = True
            if self.bomb:
                foundBombs += 1
        if foundBombs == bombCount:
            print("You won !")
            #win

    def Expose(self):
        if self.exposed:
            return
        if self.bomb:
            self.canv.delete("all")
            self.canv.create_image(pos, pos, anchor="se", image=images["bomb"])
            self.exposed = True
        else:
            self.canv.delete("all")
            self.canv.create_image(pos, pos, anchor="se", image=images[self.val])
            self.exposed = True
    
    
    def RecurExpose(self):
        if self.bomb:
            return
        self.Expose()
        if self.val != 0:
            return
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                i = self.i + dy
                j = self.j + dx
                if i in range(h) and j in range(w):
                    if not buttonList[i][j].exposed:
                        buttonList[i][j].RecurExpose()

    #Gives each tile its value by counting the number of bombs around it
    def SetValue(self):
        if self.bomb:
            return
        val = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                i = self.i + dy
                j = self.j + dx
                if i in range(h) and j in range(w):
                    if buttonList[i][j].bomb:
                        val += 1
        self.val = val
    
    #It's in the name
    @classmethod
    def ShowAllBombs(cls):
        i = 1
        for a in bombList:
            #the number here is the delay between each bomb reveal in milliseconds
            root.after(30*i, a.Expose)
            i+=1
            
            


#Creating canvases and assigning them to buttonList
for i in range(h):
    for j in range(w):
        tempButton = Buttons(tk.Canvas(master=butPanel, width=cellSize, height=cellSize, bg=bg2), i, j)
        tempButton.canv.bind("<Button-1>", tempButton.Click)
        tempButton.canv.bind("<Button-3>", tempButton.RightClick)
        tempButton.canv.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")

        buttonList[i][j] = tempButton

#Generating bombs
index = 0
while index < bombCount:
    i = random.randint(0, h-1)
    j = random.randint(0, w-1)
    if buttonList[i][j].bomb:
        continue
    bombList.append(buttonList[i][j])
    buttonList[i][j].bomb = True
    index += 1
    
#Assigning the value of each cell
for i in range(h):
    for j in range(w):
        buttonList[i][j].SetValue()

root.mainloop()