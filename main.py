import asyncio
import discord
import requests
import re
import pyautogui
import cv2

import sys
from http.client import HTTPSConnection
import schedule # pip install schedule
import time
import threading
import csv

from sofiimagereader import *

# header information for authorization of user login
# CHANGE AUTHORIZATION TO USER AUTH TOKEN
# CHANGE REFERRER TO CHANNEL URL LINK OF CHOICE
header_data = {
  "content-type": "application/json",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
  "authorization": "MTcxMzg3MzExMzU4MDgzMDcy.GogpHK.Z9y-LPdTLHjbSeGEL1ybU17g1qb7m9trEiOINo",
  "host": "discordapp.com",
  "referrer": "https://discord.com/channels/1050236914852175872/1050236915691044896"
} #hard coded to auth key, and discord server channel

header_data_channel2 = {
  "content-type": "application/json",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
  "authorization": "MTcxMzg3MzExMzU4MDgzMDcy.GogpHK.Z9y-LPdTLHjbSeGEL1ybU17g1qb7m9trEiOINo",
  "host": "discordapp.com",
  "referrer": "https://discord.com/channels/1050236914852175872/1050240758558502992"
} #hard coded to auth key, and discord server channel

# message data to send as your user
message_data = {
  "content": "sd",
  "tts": "false"
}

# hook to connect python to discord as your user
def get_connection():
  return HTTPSConnection("discordapp.com", 443)

# sends out message_data to channel_id
def send_message(conn, channel_id, message_data):
  try:
    conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
    resp = conn.getresponse()

    if 199 < resp.status < 300:
      print("Message sent!")
      pass

    else:
      sys.stderr.write(f"Received HTTP {resp.status}: {resp.reason}\n")
      pass

  except:
    sys.stderr.write("Failed to send_message\n")
    for key in header_data:
      print(key + ": " + header_data[key])

# daemon thread to run dropping job continuously until stopped by command (Python reads blocks at a time, NEED this to have it not focus on cron job)
def run_continuously(interval=1):
  cease_continuous_run = threading.Event()

  class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
      while not cease_continuous_run.is_set():
        schedule.run_pending()
        time.sleep(interval)

  continuous_thread = ScheduleThread()
  continuous_thread.start()
  return cease_continuous_run

def background_job():
  #second argument is channel ID
  send_message(get_connection(), "1050236915691044896", dumps(message_data))

def assignMessage(name):
  wishlistmessage_data = {
  "content": "scl " + str(name),
  "tts": "false"
  }
  return wishlistmessage_data

async def pickCharacter(flag):
  if flag == 1:
    x, y = (2236,1070)
    pyautogui.click(x, y)
    print(x, y)
    return
  if flag == 2:
    x, y = (2290,1070)
    pyautogui.click(x, y)
    print(x, y)
    return
  if flag == 3:
    x, y = (2353,1070)
    pyautogui.click(x, y)
    print(x, y)
    return

async def checkRose():
  print("checkRose")
  card1 = cv2.imread('firstText.png')
  card2 = cv2.imread('secondText.png')
  card3 = cv2.imread('thirdText.png')
  cardArr = [card1, card2, card3]

  colorWidth = 4
  colorHeight = 2

  for idx, card in enumerate(cardArr):
    cardColor = card[colorWidth, colorHeight]
    (b,g,r) = cardColor

    if b < 5 and g < 5 and r >= 149 and r <= 159:
      print("pick rose")
      await pickCharacter(idx+1)

  return

async def checkEvent():
  print("checkEvent")
  sofiimage = cv2.imread('sofiimage.png')
  (h,w) = sofiimage.shape[:-1]

  if h==524 and w==1008:
    return False

  print("Event pull")
  card1 = cv2.imread('firstCharacter.png')  
  card2 = cv2.imread('secondCharacter.png')
  card3 = cv2.imread('thirdCharacter.png')
  cardArr = [card1, card2, card3]

  for idx, card in enumerate(cardArr):
    if idx == 0:
      cardColor = card[82, 43]
      (b,g,r) = cardColor
      
      if b >= 87 and b <= 97 and g >= 52 and g <= 62 and r >= 229 and r <= 239:
        await pickCharacter(1)
    
    elif idx == 1:
      cardColor = card[79, 22]
      (b,g,r) = cardColor

      if b >= 87 and b <= 97 and g >= 52 and g <= 62 and r >= 229 and r <= 239:
        await pickCharacter(2)

    elif idx == 2:
      cardColor = card[78, 5]
      (b,g,r) = cardColor

      if b >= 87 and b <= 97 and g >= 52 and g <= 62 and r >= 229 and r <= 239:
        await pickCharacter(3)

  return True


async def checkWL(namesArr): #discord send "scl" message
  print("checkWL")
  for name in namesArr:
    wishlistmessage_data=assignMessage(name)
    await asyncio.sleep(5)
    send_message(get_connection(), "1050240758558502992", dumps(wishlistmessage_data))

  flag = await compare()
  # clear text files for next input
  file = open("wishlist.txt", "w") 
  file.close()
  file = open("generations.txt", "w")
  file.close()
  print(flag)
  await pickCharacter(flag)

async def compare():
  file = open("wishlist.txt")
  wishlistArr = file.read().splitlines()
  file.close()
  file = open("generations.txt")
  Generations = file.read().splitlines()
  file.close()

  wishlistInt = [eval(i) for i in wishlistArr]
  GenerationsInt = [eval(i) for i in Generations]

  maxWish=max(wishlistInt)
  if maxWish>=50:
    index=wishlistInt.index(maxWish)
    flag=index+1 #so 0 -> 1 to represent 1st character and so on
    return flag
  else:
    maxGen=min(GenerationsInt)
    index=GenerationsInt.index(maxGen)
    flag=index+1
    return flag
      
async def parseDropImage():
  firstName,firstGen,firstSeries,secondName,secondGen,secondSeries,thirdName,thirdGen,thirdSeries= await sofiimagereader()
  names=[firstName,secondName,thirdName]
  firstGen=firstGen.strip("""
                          abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !?.,“_-~+='@#"$%^&/\><°`‘G
                          """)
  secondGen=secondGen.strip("""
                            abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !?.,“_-~+='@#"$%^&/\><°`‘G
                            """)
  thirdGen=thirdGen.strip("""
                          abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !?.,“_-~+='@#"$%^&/\><°`‘G
                          """)
  print(firstGen,secondGen,thirdGen)
  file = open("dropinfo.txt", "w")
  file.write(firstGen + "," + firstName + "," + firstSeries + "\n" + secondGen + "," + secondName + "," + secondSeries + "\n" + thirdGen + "," + thirdName + "," + thirdSeries)
  file.close()
  file = open("generations.txt", "w")
  file.write(firstGen + "\n" + secondGen + "\n" + thirdGen)
  file.close()

  return names
        
def main():    
    intents=discord.Intents.default() #MIGHT NEED TO CHANGE INTENTS
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if (message.author.bot):
            #things pertaining to sofi
            if (len(message.attachments) > 0): #logic for dropping
                #download file from message.attachments[0].url
                #save to dir as sofiimg.webp
                #run function from sofiimagereader.py
                attachment=message.attachments[0]
                if attachment.filename.endswith(".webp"):
                    imgData=requests.get(attachment.url).content
                    with open("sofiimage.webp","wb") as handler:
                        handler.write(imgData)
                    names = await parseDropImage()
                    await checkRose()
                    eventFlag = await checkEvent()
                    if eventFlag == False:
                      await checkWL(names)
                    
            elif (len(message.embeds) > 0): #logic for embeds
                #cycle through 1,2,3 characters
                embeds=message.embeds
                for embed in embeds:
                    embedDesc=message.embeds[0].description
                    embedTitle=message.embeds[0].title
                if "Characters Lookup" in embedTitle:
                  with open("dropinfo.txt") as csv_file:
                    reader = csv.reader(csv_file, delimiter=",")
                    for row in reader:
                        charName = row[1].lower()
                        seriesName = row[2].lower()
                        if all(x in embedDesc.lower() for x in [charName, seriesName]):
                            #we're in scl list
                            descArray=embedDesc.lower().splitlines()
                            for i in (descArray):
                                if seriesName in i:
                                    characterLine=i
                                    break
                            #Use regex to grab the "wishlist" number
                            wishlistAmntArray=re.findall(" (.*?)`",characterLine)
                            wishlistAmnt=wishlistAmntArray[1]
                            file = open("wishlist.txt", "a")
                            file.write(wishlistAmnt + "\n")
                            file.close()
                            return

                  file = open("wishlist.txt", "a")
                  file.write("0\n")
                  file.close()
                elif "LOOKUP" in embedTitle:
                    #we're in full-view of right character
                    #wishlist to grab number
                    wishlistAmntArray=re.findall("\*\*`Wishlisted     ` ➜\*\* `(.*?)`",embedDesc)
                    wishlistAmnt=wishlistAmntArray[0].strip()
                    file = open("wishlist.txt", "a")
                    file.write(wishlistAmnt + "\n")
                    file.close()

#without daemon thread, wouldnt be watching for these:
        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

        if message.content.startswith("!timer"):
          await message.channel.send("timer started")
          # defining/queueing scheduled job - doesn't run one at call time, after it passes (it waits the first 8 minutes).
          schedule.every(8).minutes.do(background_job)
          stop_run_continuously = run_continuously()

        if message.content.startswith("!stoptimer"):
          await message.channel.send("timer stopped")
          schedule.clear()
          stop_run_continuously.set()

        if message.content.startswith("!compare"):
          await compare()

        if message.content.startswith("!parseimage"):
          await parseDropImage()
        
        if message.content.startswith("!checkevent"):
          eventFlag = await checkEvent()
          print(eventFlag)

    client.run('MTAyMzI3Nzg4NzY1NjMxNjk5OQ.G8vnTM.5ceeRQBk0H57pL0gVMZ-ulQmZlyfvi7TFbEowM') #bot token goes here


main()
