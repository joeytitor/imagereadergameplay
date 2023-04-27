import cv2
from pytesseract import pytesseract
import numpy as np
import discord
from json import dumps
from random import random


def splitImage(im):
    image=cv2.imread("sofiimage.png")
    
    (h,w)=image.shape[:-1] #ignore third dimension w/ [:-1]
    #treat w as "x"-coordinate, h and "y"-coordinate

    onethirdw=w // 3
    twothirdw=2*w // 3
    ##cv2.imshow("Original",image)
    #Crop the images
    firstCharacter=image[0:h, 0:(onethirdw-20)]
    secondCharacter=image[0:h, (10+onethirdw):(twothirdw-10)]
    thirdCharacter=image[0:h, (19+twothirdw):(w-1)]

    return firstCharacter, secondCharacter, thirdCharacter

def locateText(im, characterCounter, confidence=0.8) -> (int):
    #identify which character you're loading in
    if characterCounter==1:
        #cv2.imshow("firstCharacter", im)
        characterPath="firstCharacter.png"
        cv2.imwrite(characterPath, im)
        #cv2.waitKey(200)

    elif characterCounter==2:
        #cv2.imshow("secondCharacter", im)
        characterPath="secondCharacter.png"
        cv2.imwrite(characterPath, im)
        #cv2.waitKey(0)

    elif characterCounter==3:
        #cv2.imshow("thirdCharacter", im)
        characterPath="thirdCharacter.png"
        cv2.imwrite(characterPath, im)
        #cv2.waitKey(0)

    #now, we want to get rid of the character image at the card to evaluate the text
    card=cv2.imread(characterPath)
    (hc,wc)=card.shape[:-1]
    (bottomfourthh,bottomfourthw)=(3 * hc // 4, 3 * wc // 4)
    characterTextBlock=card[bottomfourthh+33:hc,0:wc]
    return characterTextBlock

def locateElement(im, characterCounter):
    #first, initialize all element colors
    #list of tested BGR VALUES to determine ranges:
    fire=[50,66,232]
    wood=[72,198,75]
    wind=[150,180,57]
    void=[164,85,125]
    ice=[255,205,100]
    metal=[158,158,158]
    light=[76,214,255]
    earth=[50,118,159]
    
    #check card BGR colors, important for filter
    colorWidth=4
    colorHeight=2
    #read pixel data @ point to find element color
    cardColor=im[colorWidth,colorHeight] #BGR value for the card
    (b,g,r)=cardColor
    
    #COMPARISON
    if b<=80 and b>=20 and g<=90 and g>=40 and r<=255 and r>=200:
        element="fire"
    elif b<=102 and b>=42 and g<=230 and g>=168 and r<=105 and r>=45:
        element="wood"
    elif b<=180 and b>=120 and g<=210 and g>=150 and r<=87 and r>=27:
        element="wind"
    elif b<=184 and b>=144 and g<=105 and g>=65 and r<=145 and r>=105:
        element="void"
    elif b<=255 and b>=235 and g<=225 and g>=185 and r<=120 and r>=80:
        element="ice"
    elif b<=178 and b>=138 and g<=178 and g>=138 and r<=178 and r>=138:
        element="metal"
    elif b<=96 and b>=56 and g<=234 and g>=194 and r<=255 and r>=235:
        element="light"
    elif b<=70 and b>=30 and g<=138 and g>=98 and r<=179 and r>=139:
        element="earth"
    elif b < 5 and g < 5 and r >= 149 and r <= 159:
        print("element rose")
        element="rose"
    else:
        print("element event")
        element="event"
        #maybe check different card color im[] and while loop it
    return element

def filterElement(im, element, characterCounter):
    #set path for saving filter image
    if characterCounter==1:
        filterPath="firstFilter.png"
    elif characterCounter==2:
        filterPath="secondFilter.png"
    elif characterCounter==3:
        filterPath="thirdFilter.png"

    #set bounds for element filters
    if element=="fire":
        lower_black = np.array([0,50,50]) #just change H
        upper_black = np.array([80,255,255])
    elif element=="wood":
        lower_black = np.array([70/2,50,50]) #just change H
        upper_black = np.array([170/2,255,255])
    elif element=="wind":
        lower_black = np.array([140/2,50,50]) #just change H
        upper_black = np.array([170/2,255,255])
    elif element=="void":
        lower_black = np.array([120/2,50,50]) #just change H
        upper_black = np.array([310/2,255,255])
    elif element=="ice":
        lower_black = np.array([25/2,50,50]) #just change H
        upper_black = np.array([210/2,255,255])
    elif element=="metal":
        lower_black = np.array([0/2,0,10]) #just change H
        upper_black = np.array([360/2,255,255])
    elif element=="light":
        lower_black = np.array([40/2,50,50]) #just change H
        upper_black = np.array([70/2,255,255])
    elif element=="earth":
        lower_black = np.array([0/2,50,50]) #just change H
        upper_black = np.array([70/2,255,255])
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only black colors
    if element != "rose":
        mask = cv2.inRange(hsv, lower_black, upper_black)
        #cv2.imshow("filtered", mask)
        cv2.imwrite(filterPath,mask)
    pass

def readText(im, characterCounter):
    text=pytesseract.image_to_string(im,config='--psm 6 -c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/\(){}.,!|?+=-')
    return text
