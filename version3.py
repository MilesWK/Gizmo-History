# Current version

import os # For getting the secrets
import discord # For the bot
from keep_alive import keep_alive # This is a module created in the keep_alive.py file. 
import openai # Right now this is only used for image generation.
from discord import app_commands
from time import sleep
from termcolor import colored


#streamlit run --server.address 0.0.0.0 --server.headless true --server.enableCORS=false --server.enableWebsocketCompression=false main.py
def image(prompt):
  response = openai.Image.create(
    prompt=prompt,
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
def chat(prompt):
  messages = [
    { "role": "system", "content": "You are a discord bot named Gizmo. Due to chat limits, you can only speak in 1500 characters or less. You like emojis. You are kind of talkitive, and you don't use sophisticated language. Talk in 6th grader level English. You have a command to generate images: people can go /gizmo image followed by the prompt that they want a picture of. You have 3 commands: /gizmo image followed by the prompt of the image, /gizmo react followed by an emoji reacts to the message above the command. /gizmo nuke can only be used by an administrator and removes all the messages in a channel. You are being developed so stuff won't work"},
    { "role": "user", "content": f"I want to know this: {str(prompt)}" }
  ];
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", # or gpt-4
    messages=messages
  )
  return response.choices[0].message.content
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
tree = app_commands.CommandTree(client)

# Define the option for the command
from time import time
from datetime import datetime

@tree.command(name="image", description="Use Gizmo's AI to generate images!")
async def image_command(interaction, prompt: str):
    try:
        print(f"Received interaction: {prompt}")
        await interaction.response.defer()
        response = openai.Image.create(
          prompt=prompt,
          n=1,
          size="1024x1024",
        )
        url = (response["data"][0]["url"])
        await interaction.followup.send(f"Here is a {prompt}:\n{url}\n")
    except Exception as e:
      print(f"Error in image_command: {e}, occurred at {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
      if "API" in e:
        await interaction.followup.send("Hmm, The AI seems to be broken! If you can, contact the developer. The error has been put into a log!")
        await interaction.followup.send(f"Hmm... I ran into a problem! Try again another time!\n{e}")


@tree.command(name="supporters", description="Lists all the supporters")
async def supporters_command(interaction):
    try:
        await interaction.response.defer()
        await interaction.followup.send("""
# Supporters / Helpers

Gizmo is created and mostly maintained by [MilesWK](https://mileswk.glitch.me)

You guys make Gizmo possible. Without you, Gizmo wouldn't be here!

**Special Helpers:**
[AndrewDeng3](https://replit.com/@AndrewDeng3)
- Hosted for free
- Gave coding help and advice
[TechWithAnidrudh](https://www.techwithanirudh.com/)
- Gave API key and AI
- Gave coding help and advice

CodeWest: 
- Helped support Gizmo when Gizmo was down. Was very supportive to the developer.
- Became an official tester of Gizmo.

        """)
    except Exception as e:
        print(f"Error in supporters_command: {e}, occurred at {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")



@tree.command(name="nuke",description="Removes all the messages of that channel. Can only be used by an admin",)
async def nuke_command(interaction):  # Add the correct type annotation
  if interaction.author.guild_permissions.administrator:
    try:
      await interaction.channel.send("Nuking this channel in 3.")
      sleep(2)
      await interaction.channel.send("Nuking this channel in 2..")
      sleep(2)
      await interaction.channel.send("Nuking this channel in 1...")
      sleep(2)
      for x in range(0,10): 
        await interaction.channel.purge()
    except Exception as e:
      print(e)
@client.event
async def on_ready():

  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="a game called life!"))
  await tree.sync()
  print(f'We have logged in as {client.user}')
  sleep(3)
  print(colored("Gizmo Discord Bot! ","red") + colored("Please see documents at ","blue") +    
  colored("https://github.com/MilesWK/gizmo-Discord-Bot","red")+colored(".","blue"))
  return "<h1 style='font-family: monospace'>gizmoDiscord Bot</h1>"



keep_alive()
client.run(TokenID)

