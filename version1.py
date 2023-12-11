# All the modules used!
import os # For getting the secrets
import random # For the random responses 
import replit # For cleaing the console
from termcolor import colored # For colored console text
import discord # For the bot
from time import sleep # For waiting
from keep_alive import keep_alive # This is a module created in the keep_alive.py file. 
import openai # Right now this is only used for image generation.
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
openai.api_key = os.environ['OPENAI_API_KEY'] # System Environment Variable 
openai.api_base = 'https://api.techwithanirudh.com/v1' # really important

replit.clear()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# These are the random responses
Hi = ["Hello ", "Hi ", "Oh hi! Didn't see you there ", "Good day, "]
Bye = ["Leaving already? ", "Goodbye! ", "See you later!", "Have a good one! "]
What_Is_Up = [
  "Nothing much!", "Just chilling", "Just having a good time with you!",
  "Nothing..."
]

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  sleep(3)
  replit.clear()
  print(colored("Gizmo Discord Bot! ","red") + colored("Please see documents at ","blue") +    
  colored("https://github.com/MilesWK/gizmo-Discord-Bot","red")+colored(".","blue"))
  return "<h1 style='font-family: monospace'>gizmoDiscord Bot</h1>"

  


@client.event
async def on_message(message):
  messageReturn = message.content.lower()
  if isinstance(message.channel, discord.DMChannel):
    if message.author == client.user:
      return
    elif "/gizmo say" in messageReturn:
      await message.channel.send(string(message.content,14))
    elif "/gizmo image" in messageReturn:
  
      await message.channel.send("Creating an image based off of your input. This might take a minute")
      try:
        promptWord=string(messageReturn, 15)
        response = openai.Image.create(
        prompt=promptWord,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']
        await message.channel.send("Here is your image: ") 
        embed = discord.Embed()
        embed.set_image(url=image_url)
        await     message.channel.send(file=None, embed=embed)
      except Exception as e:
        await message.channel.send("Hmmm... something went wrong, sorry!")
        print(e)
    elif "how are you" in messageReturn and "gizmo" in messageReturn:
      How_are_you = ["I am fine! Thank you for asking " + str(message.author) + "!","Just swell!","I'm Chill...","I am having a good time talking to you!"]
      customResponse = How_are_you[random.randint(0, 3)]
      await message.channel.send(str(customResponse))
    elif "hi" in messageReturn and len(messageReturn) < 20 or "hello" in messageReturn and len(messageReturn) < 20:
      customResponse = Hi[random.randint(0, 3)]
      await message.channel.send(str(customResponse) + str(message.author) + '!')
    elif "bye" in messageReturn or "goodbye" in messageReturn :
      customResponse = Bye[random.randint(0, 3)]
      await message.channel.send(str(customResponse))
    elif "what is up" in messageReturn or "what's up" in messageReturn:
      customResponse = What_Is_Up[random.randint(0, 3)]
      await message.channel.send(str(customResponse))
    elif "why" in messageReturn and "happy" in messageReturn :
      await message.channel.send(
        "I am happy because I am with you. It brings me great joy to talk with you!"
      )
    elif "case sensitive" in messageReturn :
      await message.channel.send("No commands are case sensitive!")
    elif "joe mama" in messageReturn:
      await message.channel.send("NO!!! NO JOE MAMA! ")
      await message.channel.send("ALERT!!! " + str(message.author) +
                                 " has said joe mama!")
    elif "gizmo" in messageReturn and "help" in messageReturn:
      await message.channel.send("I can help you! The commands I have are\n **/gizmospam**\n **/gizmosay *[what you want me to say***]")
      await message.channel.send("I respond to\n **- hi**\n **- hello**\n **- What's up (what is up)**\n **- How are you**\n **- Why are you so happy**\n **- Bye**\n **- Help**. \nFor the documentation of this bot, please visit **https://github.com/MilesWK/gizmo-Discord-Bot**")
    elif "be" in messageReturn and "sad" in messageReturn and "gizmo" in messageReturn:
      await message.channel.send("I cannot be sad when I have friends like you!")
    else:
      Question = messageReturn
      # Function to interact with ChatGPT
      def chat_with_gpt(prompt):
          prompt = prompt.replace("gizmo", "")
          response = openai.Completion.create(
              model='gpt-',  # Use the davinci-codex model
              prompt=prompt,
              max_tokens=2000,  # Adjust the length of the response as needed
              temperature=0.7,  # Adjust the temperature for more or less randomness
              n=1,  # Generate a single response
              stop=None,  # Let ChatGPT decide when to stop
              timeout=5 # Set a timeout limit for the API call (in seconds)
          )
          answer = response.choices[0].text.strip()
          if check_second_line(answer) == "":
            answer = remove_first_two_lines(answer)
          return answer
      # Main conversation loop
    
      # Add the user input as a prompt and get the response from ChatGPT
      response = chat_with_gpt(Question)
      await message.channel.send(response)
  else:
    if message.author == client.user:
      return
    elif "/gizmo say" in messageReturn:
      await message.channel.send(string(message.content,10))
    elif "/gizmo image" in messageReturn:
  
      await message.channel.send("Creating an image based off of your input. This might take a minute")
      try:
        promptWord=string(messageReturn, 12)
        response = openai.Image.create(
        prompt=promptWord,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']
        await message.channel.send("Here is your image: ") 
        embed = discord.Embed()
        embed.set_image(url=image_url)
        await     message.channel.send(file=None, embed=embed)
      except Exception as e:
        await message.channel.send(e)
        print(e)
    elif "how are you" in messageReturn and "gizmo" in messageReturn:
      How_are_you = ["I am fine! Thank you for asking " + str(message.author) + "!","Just swell!","I'm Chill...","I am having a good time talking to you!"]
      customResponse = How_are_you[random.randint(0, 3)]
      await message.channel.send(str(customResponse))
    elif "hi" in messageReturn and "gizmo" in messageReturn and len(messageReturn) < 20 or "hello" in messageReturn and "gizmo" in messageReturn and len(messageReturn) < 20:
      customResponse = Hi[random.randint(0, 3)]
      await message.channel.send(str(customResponse) + str(message.author) + '!')
    elif "bye" in messageReturn and "gizmo" in messageReturn or "goodbye" in messageReturn and "gizmo" in messageReturn:
      customResponse = Bye[random.randint(0, 3)]
      await message.channel.send(str(customResponse))
    elif "what is up" in messageReturn and "gizmo" in messageReturn or "what's up" in messageReturn and "gizmo" in messageReturn:
      customResponse = What_Is_Up[random.randint(0, 3)]
      await message.channel.send(str(customResponse))
    elif "why" in messageReturn and "happy" in messageReturn and "gizmo" in messageReturn:
      await message.channel.send(
        "I am happy because I am with you. It brings me great joy to talk with you!"
      )
    elif "case sensitive" in messageReturn and "gizmo" in messageReturn:
      await message.channel.send("No commands are case sensitive!")
    elif "joe mama" in messageReturn:
      await message.channel.send("NO!!! NO JOE MAMA! ")
      await message.channel.send("ALERT!!! " + str(message.author) +
                                 " has said joe mama!")
    elif "gizmo" in messageReturn and "help" in messageReturn:
      await message.channel.send("I can help you! You can talk to me ")
      await message.channel.send("I respond to\n **- hi**\n **- hello**\n **- What's up (what is up)**\n **- How are you**\n **- Why are you so happy**\n **- Bye**\n **- Help**. \nFor the documentation of this bot, please visit **https://github.com/MilesWK/gizmo-Discord-Bot**")
    elif "be" in messageReturn and "sad" in messageReturn and "gizmo" in messageReturn:
      await message.channel.send("I cannot be sad when I have friends like you!")
    elif "gizmo" in messageReturn:
      Question = messageReturn
      # Function to interact with ChatGPT
      def chat_with_gpt(prompt):
          prompt = prompt.replace("gizmo", "")
          response = openai.Completion.create(
              model='gpt-4',  # Use the davinci-codex model
              prompt=prompt,
              max_tokens=2000,  # Adjust the length of the response as needed
              temperature=0.7,  # Adjust the temperature for more or less randomness
              n=1,  # Generate a single response
              stop=None,  # Let ChatGPT decide when to stop
              timeout=5 # Set a timeout limit for the API call (in seconds)
          )
          answer = response.choices[0].text.strip()
          if check_second_line(answer) == "":
            answer = remove_first_two_lines(answer)
          return answer
      # Main conversation loop
    
      # Add the user input as a prompt and get the response from ChatGPT
      response = chat_with_gpt(Question)
      await message.channel.send(response)
keep_alive()
client.run(TokenID)
