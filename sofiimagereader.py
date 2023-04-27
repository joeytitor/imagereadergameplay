import asyncio
from PIL import Image
import cv2
from pytesseract import pytesseract
import numpy as np
from utilities import *

async def sofiimagereader():    
    #Fetch file different, from discord. this is to test, i'll just
    #save it as sofiimage.webp when i grab it
    im=Image.open("sofiimage.webp").convert("RGB")
    im.save("sofiimage.png","png")
    tesseractPath=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = tesseractPath

    #First, split the image into 3 "cards"/"characters"
    pause=0
    firstCharacter, secondCharacter, thirdCharacter = splitImage(im)

    #Second, crop to only keep text
    characterCounter=1
    firstCharacterTextBlock = locateText(firstCharacter, characterCounter)
    cv2.imwrite("firstText.png",firstCharacterTextBlock)
    characterCounter=2
    secondCharacterTextBlock = locateText(secondCharacter, characterCounter)
    cv2.imwrite("secondText.png",secondCharacterTextBlock)
    characterCounter=3
    thirdCharacterTextBlock = locateText(thirdCharacter, characterCounter)
    cv2.imwrite("thirdText.png",thirdCharacterTextBlock)

    #Third, we find what "element" the card is to apply correct filters later
    characterCounter=1
    firstElement=locateElement(firstCharacterTextBlock, characterCounter)
    characterCounter=2
    secondElement=locateElement(secondCharacterTextBlock, characterCounter)
    characterCounter=3
    thirdElement=locateElement(thirdCharacterTextBlock, characterCounter)

    if firstElement != "event" and secondElement != "event" and thirdElement != "event":
        #Fourth, we filter the images based on element
        characterCounter=1
        filterElement(firstCharacterTextBlock,firstElement, characterCounter)
        characterCounter=2
        filterElement(secondCharacterTextBlock,secondElement, characterCounter)
        characterCounter=3
        filterElement(thirdCharacterTextBlock, thirdElement, characterCounter)

    #Fifth, with the filtered cards for clarity, we read the text off of them.
    characterCounter=1
    firstText = readText("firstFilter.png", characterCounter)
    characterCounter=2
    secondText = readText("secondFilter.png", characterCounter)
    characterCounter=3
    thirdText = readText("thirdFilter.png", characterCounter)
    print(firstText,secondText,thirdText)
    #seperate text into gen, name, series
    firstText=firstText.splitlines()
    #print(firstText)
    firstGen=firstText[0]
    firstName=firstText[1]
    firstSeries=firstText[2]

    secondText=secondText.splitlines()
    secondGen=secondText[0]
    secondName=secondText[1]
    secondSeries=secondText[2]

    thirdText=thirdText.splitlines()
    thirdGen=thirdText[0]
    thirdName=thirdText[1]
    thirdSeries=thirdText[2]
    return firstName, firstGen, firstSeries, secondName, secondGen, secondSeries, thirdName, thirdGen, thirdSeries
