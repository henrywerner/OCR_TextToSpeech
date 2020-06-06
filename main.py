import cv2
import numpy as nm 
import pytesseract
import time
import keyboard
#import win32api as win32
import pyautogui as pyag
import pyttsx3 as tts

from PIL import Image, ImageGrab, ImageEnhance

class Monoculus:

    # screen capture framerate limit
    fps = 15

    # screen capture coords
    x = 200
    y = 200
    offx = 150
    offy = 50

    engine = tts.init()
  
    def __init__(self):
        volume = self.engine.getProperty('volume')
        voice = self.engine.getProperty('voices')
        print('{+} TTS Volume: ', end="")
        print(volume)
        print('{+} TTS Voice: ', end="")
        print(voice)
        print('{+} Screen Size: ', end="")
        print(pyag.size())
        
        #TODO: Make this actually work
        keyboard.wait('ctrl')
        print(pyag.position())
        mouseX, mouseY = pyag.position()
        self.x = mouseX
        self.y = mouseY
        print('x = ' + str(self.x))
        print('y = ' + str(self.y))

        keyboard.wait('ctrl')
        mouseX, mouseY = pyag.position()
        self.offx = mouseX
        self.offy = mouseY
        print('offx = ' + str(self.offx))
        print('offy = ' + str(self.offy))


    def screenToString(self):
        # Path of tesseract executable 
        pytesseract.pytesseract.tesseract_cmd ='E:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        # Setting up cv2 window for image preview
        cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE) # _NORMAL or _AUTOSIZE

        ocrText = "a"
        ocrTextPrev = "a"

        self.engine.say("Starting text to speech.")

        while True:
            cap = self.captureScr()     # Calls screen capture method
            cv2.imshow('image',cap)     # Draws cap to window

            ocrTextPrev = ocrText
            ocrText = pytesseract.image_to_string(cap,lang ='eng') 
            
            # I stole this from Michael Reeves and now my code works
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            if (ocrText != ocrTextPrev):
                print(ocrText)
                self.engine.say(ocrText)
                self.engine.runAndWait()

            time.sleep(1./self.fps)

        self.engine.stop()


    def captureScr(self):
        cap = ImageGrab.grab(bbox =(self.x, self.y, self.offx, self.offy), all_screens = False)
        cap = cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY)
        # cap = cv2.cvtColor(nm.array(cap), cv2.COLOR_RGB2BGR)          # Color Image
        return cap



### Calling the functions 
m = Monoculus()
m.screenToString()
