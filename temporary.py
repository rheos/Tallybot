import discord
import os
import requests
import json
import random
from replit import db
from collections import defaultdict


client = discord.Client()

#record the vote 
def update_poll(ticker,requestor):
  vote = {ticker : {requestor : 1}}

for (key, value) in vote.items():
    if 'poll' not in db.keys():
        db['poll'] = []
    if key in db['poll'].keys():
        db['poll'][key].append(value)
    else:
        db['poll'][key] = value

#format and sort results for printing
def print_results(poll):
 # result = ""
 # for ticker in sorted(poll, key=lambda t: sum(poll[t].values()), reverse=True):
 #   result += (f"{ticker}: {', '.join(sorted(poll[ticker]))}\n")
  
  result = ("\n".join([" : ".join([elem[0]," ".join(list(elem[1].keys()))]) for elem in sorted(poll.items(), key = lambda item : len(list(item[1].keys())), reverse = True)]))
  
  return result

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
 
#record a vote

  if msg.startswith("!v"):
    ticker = msg.split("!v ",1)[1]
    author = str(message.author).split("#",1)[0]
    update_poll(ticker,author)
     
    await message.channel.send("vote for " + ticker + " by " + author + " added.")
    await message.channel.send(db["poll"])

  if msg.startswith("!clear"):
    
    db["poll"] = {}
    
    await message.channel.send("poll cleared")
    await message.channel.send(db["poll"])

# create a test set of data

  if msg.startswith("!testset"):

    db["poll"] = {
     'LINK' : {'MoonRaccoon' : 1, 'TheDirtyTree' : 1},
	   'ZRX' : {'MoonRaccoon' : 1, 'Dontcallmeskaface' : 1, 'TheDirtyTree' : 1},  
	   'XRP' : {'Dontcallmeskaface' : 1},
     'XLM' : {'aeon' : 1, 'Bob' : 1} 
	   }


    await message.channel.send("results:")
    await message.channel.send(db["poll"])
    print (db)

# print results of the poll
  if msg.startswith("!results"):

    await message.channel.send("results:")
    await message.channel.send(print_results(db["poll"]))


client.run(os.getenv('TOKEN'))