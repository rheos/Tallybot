import discord
import os
import requests
import json
import random
from replit import db

#keep bot alive
import keep_alive
keep_alive.keep_alive()

max_votes = 3

client = discord.Client()

#record the vote 
def record_vote(ticker,requestor):
  poll = {}
  vote_count = {}

  if 'vote_count' in db.keys():
    vote_count = db['vote_count']

  if requestor in vote_count.keys() :
    if vote_count[requestor] < max_votes :
      vote_count[requestor] += 1
    else :
      error = "I'm sorry, " + requestor + ". I'm afraid I can't do that.  (max votes reached)"
      return error
  else :
    vote_count[requestor] = 1

  db['vote_count'] = vote_count

#  print(vote_count)

  if 'poll' in db.keys():
    poll = db['poll']
  poll.setdefault(ticker, {})[requestor] = 1
  db['poll'] = poll
  
  return 1


def delete_vote(ticker,requestor):
  poll = {}
  vote_count = {}

  if "vote_count" in db.keys() :
    vote_count = db['vote_count']

  if requestor in vote_count.keys() :
    vote_count[requestor] -= 1
    if vote_count[requestor] < 1 :
      del vote_count[requestor]
  else :
    error = "I'm sorry, " + requestor + ". I'm afraid I can't do that.  (no vote found)"
    return error

  if 'poll' in db.keys():
    poll = db['poll']
    if ticker in poll.keys():
      if requestor in poll[ticker].keys():
        del poll[ticker][requestor]
        if len(poll[ticker]) < 1 :
          del poll[ticker]
      else :
        error = "I'm sorry, " + requestor + ". I'm afraid I can't do that.  (no vote found)"
        return error

  db['poll'] = poll
  db['vote_count'] = vote_count
  return 1
    

#format and sort results for printing
def print_results(poll):
  result = ("\n".join([" : ".join([elem[0],", ".join(list(elem[1].keys()))]) for elem in sorted(poll.items(), key = lambda item : len(list(item[1].keys())), reverse = True)]))
  
  return result

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#
# START BOT LOGIC
#

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
 
#record a vote

  if msg.startswith("+"):
    ticker = msg.split("+",1)[1].upper().split(" ")[0]
    author = str(message.author).split("#",1)[0]
    result = record_vote(ticker,author)

    if result == 1 : 
      await message.channel.send("vote for " + ticker + " by " + author + " added.")
    else :
      await message.channel.send(result)

#remove a vote

  if msg.startswith("-"):
    ticker = msg.split("-",1)[1].upper()
    author = str(message.author).split("#",1)[0]
    result = delete_vote(ticker,author)
     
    if result == 1 :
      await message.channel.send("vote for " + ticker + " by " + author + " removed")
    else :
      await message.channel.send(result)

#clear the poll

  if msg.startswith("!shhh"):
    db["poll"] = {}
    db["vote_count"] = {}
    await message.channel.send("poll cleared")

#    cleared = False
#    for r in message.author.roles :
#      print (r)
#      if r == "@poll-admin" :
#        db["poll"] = {}
#        await message.channel.send("poll cleared")
#        cleared = True    
#    if not cleared :
#      await message.channel.send("you don't have permission to clear the poll")

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
    if len(db["poll"]) > 0 :
      await message.channel.send("Today's TA requests:")
      await message.channel.send(print_results(db["poll"]))
    else :
      await message.channel.send("poll is empty")

# print usage
  if msg.startswith("!usage"):

    usage = "+SYMBOL  - add a vote\n"
    usage += "-SYMBOL  - delete a vote\n"
    usage += "!results  - see poll results\n"
    usage += "!usage - see this message"
    

    await message.channel.send("Poll Usage:")
    await message.channel.send(usage)
    
#inspire 

  if msg.startswith("!inspire"):
    quote = get_quote()
    await message.channel.send(quote)



client.run(os.getenv('TOKEN'))