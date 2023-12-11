
import os # For getting the secrets
import replit # For cleaing the console @AndrewDeng3 Use os.system('clear') it works better
from termcolor import colored # For colored console text
import discord # For the bot
from time import sleep # For waiting
from keep_alive import keep_alive # This is a module created in the keep_alive.py file. 
import openai # Right now this is only used for image generation.
from time import sleep

def image(prompt):
  response = openai.Image.create(
    prompt=string(prompt, 15),
    n=1,
    size="400x400"
  )
  return response
def check_second_line(string):
    lines = string.split('\n')
    # Check if there are at least two lines
    if len(lines) >= 2:
        return lines[1]
    else:
        return None
def remove_first_two_lines(string):
    lines = string.split('\n')
    # Check if there are at least two lines
    if len(lines) >= 2:
        # Join all lines except the first two
        result = '\n'.join(lines[2:])
        return result
    else:
        # Return the original string if it has fewer than two lines
        return string
# removes a certain amount of letters from the beginning of a string
def string(string, remove):
  StringPosition = remove
  ReturnString = ""
  for x in range(remove, len(string)):
    ReturnString = str(ReturnString) + str(string[StringPosition])
    StringPosition += 1
  return ReturnString

TokenID = os.environ['TOKEN ID'] # System Environment Variable
openai.api_key = os.getenv('OPENAI_API_KEY') # System Environment Variable 
openai.api_base = 'https://api.techwithanirudh.com/v1'
os.system('clear')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Going down January 1st. :("))
  print(f'We have logged in as {client.user}')
  sleep(3)
  replit.clear()
  print(colored("Gizmo Discord Bot! ","red") + colored("Please see documents at ","blue") +    
  colored("https://github.com/MilesWK/gizmo-Discord-Bot","red")+colored(".","blue"))
  return "<h1 style='font-family: monospace'>gizmoDiscord Bot</h1>"
def chat(prompt, message):
  username = message.author.name
  username_without_discriminator = username.split("#")[0]
  messages = [
    { "role": "system", "content": "You are a discord bot named Gizmo. Due to chat limits, you can only speak in 1500 characters or less. You like emojis. You are kind of talkitive. You have a command to generate images: people can go /gizmo image followed by the prompt that they want a picture of. You have 3 commands: /gizmo image followed by the prompt of the image, /gizmo react followed by an emoji reacts to the message above the command. /gizmo nuke can only be used by an administrator and removes all the messages in a channel. You are going down starting January 1st due to hosting issues. Be sure to let them know that. " },
    { "role": "user", "content": f"I am {str(username_without_discriminator)} and I want to know this: " + str(prompt) }
  ];
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", # or gpt-4
    messages=messages
  )
  return response.choices[0].message.content
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  elif message.content.startswith('/gizmo image'):
    async with message.channel.typing():
      try:
        response = image(message.content.lower())
        image_url = response['data'][0]['url']
        await message.channel.send("Here is your image: ") 
        embed = discord.Embed()
        embed.set_image(url=image_url)
        await message.channel.send(file=None, embed=embed)
      except Exception as e:
        print(e)
        if "moderation" in str(e):
          em = discord.Embed(title="**Whoops! Not doing that!**",description=f"Looks like the AI turned down the request due to an innapropriate topic! If you think this is a mistake, contact the developer!\n\n*{message.author}~this~: {message.content}*", color=discord.Colour.red())
        elif "rate" in str(e):
          print(e)
          em = discord.Embed(title="**Hold your horses!**",description=f"Looks like you just got rate-limited! This means you, or someone else has been using the AI feature a lot, and is getting this same message! Try again in like 10 minutes! Sorry! \n\n*{message.author}~this~: {message.content}*", color=discord.Colour.red())
        else:
          em = discord.Embed(title="**Uh, oh!**",description=f"Looks like we ran into some errors! Try again later or contact the developer!\n\n*{message.author}~this~: {message.content}*", color=discord.Colour.red())
        await message.channel.send(embed=em)
  elif "lol " in message.content.lower():
    await message.add_reaction("🤣") 

  elif "sad " in message.content.lower():
      await message.add_reaction("🙁")

  elif message.content.startswith('/gizmo react'):
    if "💩" in message.content.lower():
      em = discord.Embed(title="**Um, no. **",description=f"Yeah no. Nice try, but no.\n\n*{message.author}~this~: {message.content}*", color=discord.Colour.red())
      await message.channel.send(embed=em)
    else:
      async for msg in message.channel.history(limit=2):
        if msg != message:
          await msg.add_reaction(string(message.content.lower(),13))
          await message.delete()
          break

  elif message.content.startswith('/gizmo nuke'):
    if message.author.guild_permissions.administrator:
      try:
        await message.channel.send("Nuking this channel in 3.")
        sleep(2)
        await message.channel.send("Nuking this channel in 2..")
        sleep(2)
        await message.channel.send("Nuking this channel in 1...")
        sleep(2)
        for x in range(0,10): 
          await message.channel.purge()
        em = discord.Embed(title="**NUKED!**",description="All the messages on this channel has been \"Nuked\" By an admin! \n\nNow you have a clean slate to work with! Lovely!", color=discord.Colour.green())
        await message.channel.send(embed=em)
      except:
        em = discord.Embed(title="**Oh whoops,**",description=f"Whoops! I did that to fast! Try again another time.\n\n*{message.author}~this~: {message.content}*", color=discord.Colour.red())
        await message.channel.send(embed=em)

    else:
      em = discord.Embed(title="**Not allowed to do that!**",description=f"You do not have permission to do that. Contact the administrator of the channel to do that. \n\n*{message.author}~this~: {message.content}*", color=discord.Colour.red())
      await message.channel.send(embed=em)
  else:
    if isinstance(message.channel, discord.DMChannel):
      async with message.channel.typing():
        await message.channel.send(chat(message.content, message))
    elif isinstance(message.channel, discord.TextChannel) and client.user in message.mentions:
      async with message.channel.typing():
        await message.channel.send(chat(message.content, message))


keep_alive()
client.run(TokenID)
