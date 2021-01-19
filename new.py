#### backgrounder stuff

from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def main():
  return "Your Bot Is Ready"
def run():
  app.run(host="0.0.0.0", port=8000)
def keep_alive():
  server = Thread(target=run)
  server.start()


status = 'with Python'
@bot.event
async def on_ready():
  change_status.start()
  print("Your bot is ready")
@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(status))


####