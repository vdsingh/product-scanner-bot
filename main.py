import discord
from discord.ext import tasks, commands
import asyncio

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

# CHROMEDRIVER_PATH = './chromedriver/90.0.4430.24/chromedriver'
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')


CHROMEDRIVER_PATH='/app/.chromedriver/bin/chromedriver'

currentTasks = {}
urlTitles = {}


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = CHROMEDRIVER_PATH

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)



client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
  print("bot is ready.")

@client.event
async def on_member_update(before, after):
  print(f"{before} updated.")


@client.command()
async def scan(ctx, *, args):
  await client.wait_until_ready()
  arguments = args.split(" ")
  print("starting scan.")
  await ctx.send("Please wait while I load my browser.")
  url = arguments[0]
  if "bestbuy" in url:
    task = client.loop.create_task(scanBestBuyURL(ctx, url, 1))
    currentTasks[url] = task
  else:
    await ctx.send("I am not coded to scan that URL.")

@client.command()
async def stop(ctx, *, args):
  arguments = args.split(" ")
  url = arguments[0]
  if not url in currentTasks:
      await ctx.send(f"There is currently no task for URL: {url}")
      return

  currentTasks[url].cancel()
  currentTasks.pop(url, None)
  await ctx.send(f"Canceled task for URL: {url}")

@client.command()
async def tasks(ctx):
  await client.wait_until_ready()
  print("printing tasks")
  if len(currentTasks) == 0:
      await ctx.send("I am not currently scanning for anything ")
      return
  await ctx.send("I am currently scanning for: ")
  for url in currentTasks.keys():
    await ctx.send(f"{urlTitles[url]} at <{url}>")

async def scanBestBuyURL(ctx, url, sleep):
  driver.get(url)
  title = driver.find_element_by_tag_name("h1").text
  urlTitles[url] = title
  await ctx.send(f"Now scanning <{url}> \n {title}")
  await asyncio.sleep(1)

  while True:
    addButton = driver.find_element_by_class_name("add-to-cart-button")
    if not "btn-disabled" in addButton.get_attribute("class").split():
      await ctx.send(f"{title} is now in stock! I will remove it from my tasks.")
      currentTasks.pop(url, None)
      print(f"removed {url} from tasks")
      return
    else:
      print(f"Sold Out of {title}")
      driver.refresh()
    await asyncio.sleep(sleep)

client.run(DISCORD_BOT_TOKEN)