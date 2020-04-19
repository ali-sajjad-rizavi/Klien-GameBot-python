from python_imagesearch.imagesearch import imagesearch
import cv2
from PIL import Image
import pyautogui
import numpy as np

from tkinter import *
from tkinter import messagebox
import time
import random
import re

#-log----------------------------
import atexit

logfile = open('log.txt', 'w', encoding='utf-8')
def closeLogFile():
    logfile.close()
atexit.register(closeLogFile)
#--------------------------------

#-OCR--
import pytesseract
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#print("Done getting tesseract...")
#------

#img = cv2.imread('testpic.png')
#text = pytesseract.image_to_string(img)
#print(text)
#-----------

def getUpscaledImage(img):
    w, h = img.size
    #w = int(img.shape[1]*4)
    #h = int(img.shape[0]*4)
    cv2image = np.array(img.convert('RGB'))[:, :, ::-1].copy()
    resizedimage = cv2.resize(cv2image, (w*5, h*5))
    return resizedimage

#-----------

class Robot:
    def __init__(self):
        self.__imgpos = imagesearch("button.png")
        #self.__buttonCVImage = cv2.imread('button.png')
    def clickOnButton(self):
        posX, posY = pyautogui.position()
        if posX < 100 and posY < 100:
            #print('Stopping the program...')
            return False
        #-------
        if self.__imgpos[0] == -1:
            #print('Button not found!')
            return False
        width, length = self.__imgpos
        #if pyautogui.locateOnScreen(self.__buttonCVImage, region=(width, length, width+50, length+50)) == None:
            #print('Button is here but PYAUTOGUI could not find it but lets continue!')
        #pyautogui.moveTo(self.__imgpos, duration=0.1)
        pyautogui.moveTo(self.__imgpos, duration=random.choice(np.arange(0.09, 0.14, 0.01)))
        #print('Moved to button!')
        pyautogui.click(self.__imgpos, interval=0.25)
        #print('Clicked the button!')
        width, length = self.__imgpos
        #pyautogui.moveTo(width - 150, length - 150, duration=0.1)
        pyautogui.moveTo(width - 150, length - 150, duration=random.choice(np.arange(0.09, 0.14, 0.01)))
        #print('Moved away!')
        return True

    def isGoodBonus(self, minBonus):
        width, length = self.__imgpos
        #-----Capturing boxes-------------------
        boxesScreenshots = []
        boxesScreenshots.append(pyautogui.screenshot(region=(width - 114, length - 276, 281, 40)))
        #boxesScreenshots.append(pyautogui.screenshot(region=(width - 114, length - 276 + 52, 281, 40)))
        #boxesScreenshots.append(pyautogui.screenshot(region=(width - 114, length - 276 + 104, 281, 40)))
        #boxesScreenshots.append(pyautogui.screenshot(region=(width - 114, length - 276 + 156, 281, 40)))
        #boxesScreenshots.append(pyautogui.screenshot(region=(width - 114, length - 276 + 208, 281, 40)))

        #print('Started to convert images to text!')
        #-----Converting-to-String--------------
        boxesStrings = []
        for screenshot in boxesScreenshots:
            boxesStrings.append(pytesseract.image_to_string(getUpscaledImage(screenshot)))#lang='hun' maybe needed
        #print(boxesStrings)
        #log---
        for bstr in boxesStrings:
            logfile.write(bstr + ', ')
        logfile.write('\n')
        #------
        #---------------------------------------
        for text in boxesStrings:
            numList = re.findall('[0-9]+', text)
            if len(numList) > 0:
                if int(numList[0]) >= minBonus and int(numList[0]) < 100:
                    return True
        return False

#======================================================

def startTheRobot(minimumBonus):
    theRobot = Robot()
    #print('Robot initialized!')
    if theRobot.clickOnButton() == False:
        messagebox.showinfo('gombra kattintás', 'Nem lehet kattintani!')
        #print('Could not perform first click!')
        return
    while theRobot.isGoodBonus(minimumBonus) == False:
        if theRobot.clickOnButton() == False:
            messagebox.showinfo('gombra kattintás', 'Nem lehet kattintani!')
            #print('Could not click!')
            return
    messagebox.showinfo('Kész!', 'bónusz található')

#======================================================

class BotWindow:
    def __init__(self):
        self.__root = Tk()
        self.__root.title("GameBot")
        self.__root.geometry("300x100")
        self.__root.resizable(False, False)
        #
        frame1 = Frame(self.__root)
        Label(frame1, text='Írja be a bónuszt:').grid(row=0, column=0)
        self.__textEntry = Entry(frame1)
        self.__textEntry.grid(row=0, column=1, padx=5)
        frame1.grid(row=0, padx=15, pady=15)
        #
        frame2 = Frame(self.__root)
        self.__startbotButton = Button(frame2, text=' Rajt ', command=lambda: startTheRobot(int(self.__textEntry.get())))
        self.__startbotButton.grid(column=0, padx=80)
        frame2.grid(row=1, padx=15, pady=5)

    def getMinimumBonus():
        return int(textEntry.get())

    def show(self):
        self.__root.mainloop()

def main():
    #print('Started main...')
    form = BotWindow()
    form.show()

#if __name__ == 'main':
    #main()


main()
