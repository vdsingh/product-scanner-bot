from socket import timeout

import discord
from discord.ext import tasks, commands
import asyncio

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

currentTasks = {}
urlTitles = {}

driver = webdriver.Chrome('./chromedriver/90.0.4430.24/chromedriver')
# driver.manage().window().maximize(); 


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
  if url.contains("bestbuy"):
    task = client.loop.create_task(scanBestBuyURL(ctx, url, 1))
    currentTasks[url] = task
  else:
    await ctx.send("I am not coded to scan that URL.")


@client.command()
async def tasks(ctx):
  await client.wait_until_ready()
  print("printing tasks")

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
      # self.cancel()
    else:
      print(f"Sold Out of {title}")
      driver.refresh()
    await asyncio.sleep(sleep)



# client.loop.create_task(ping())
client.run('ODM0OTQ2NTcxODg2OTE5NzEx.YIISlw.D4_Bbx4ZYG6DK8pVY_2vejNzx8g')

# Handle Web Scraping/Checking Code


# urls = []

# url = input("Enter URL: ")
# sleepTime = int(input("How often do you want to check (seconds)?: "))

# driver = webdriver.Chrome('./chromedriver/90.0.4430.24/chromedriver')

# def handleBestBuy(url):
#   addButton = driver.find_element_by_class_name("add-to-cart-button")
#   if not "btn-disabled" in addButton.get_attribute("class").split():
    
#     print("\n------------------------------------")
#     print("IN STOCK: ", title, "\n")
#     return True
#     print(url)
#     print("\n------------------------------------")
    
#     exit()
#     # notification.notify(title="BestBuy Product Available", message=url, timeout=10)
#   else:
#     print("Sold Out.")
#     driver.refresh()

# def scan(url, sleepTime):
#   driver.get(url)
#   while True:
#     if "bestbuy" in url:
#       if handleBestBuy(url):
#         return True
#       time.sleep(sleepTime)
#     else:
#       break
