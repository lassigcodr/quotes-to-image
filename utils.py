import os
import openai
import base64
import time
import requests
from PIL import Image, ImageFont, ImageDraw
import textwrap

# Initiate openai api key and the chat message history
openai.api_key = os.getenv("OPENAI_API_KEY")
message_history = [
    {"role": "user", "content": f"Here is a formula: <emotion>,<mood>,<facial expression>,<pose>,<scenario>,<character reference>,<extra character>. What to do with it will be given later."},
    {"role": "assistant", "content": f"Sure."},
    {"role": "user", "content": f"A quote, character, anime series will be given later. "},
    {"role": "assistant", "content": f"I understand."},
    {"role": "user", "content": f"Use the quote to get the emotion, mood, facial expression, scenario, etc. Also use the quote to get a camera shot more suitable in the scenario. Use the anime series to get extra character if needed."},
    {"role": "assistant", "content": f"Sure."}
]

# Generate chatGPT response
def generate_prompt_guide(inp):
    global message_history
    message_history.append({"role": "user", "content":inp})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
    )
    reply_content = completion.choices[0].message.content
    #print(reply_content)
    message_history.append({"role": "assistant", "content": reply_content})
    return reply_content

# Get random anime quote from animechan api
def get_quote(url = 'https://animechan.vercel.app/api/random'):
    data = requests.get(url).json()
    return data

# Generate ai art
def generate_ai_art(prompt, quote, character, anime):
    # Parse generated prompt to make dall-e resquest 
    response = openai.Image.create(
        prompt = prompt,
        n=1,
        size="512x512",
        response_format="b64_json"
    )

    # Save generated image into system memory
    for i in range(0, len(response['data'])):
        b64 = response['data'][i]['b64_json']
        filename = f'image_{int(time.time())}_{i}.png'
        print('Saving file ' + filename)
        with open(f'images/{filename}', 'wb') as f:
            f.write(base64.urlsafe_b64decode(b64))
   
        # Add quote as the subtitle
        add_subtitle(filename, quote, character, anime)

    return filename
        


        
def add_subtitle(filename, quote, character, anime):
    # Load the image
    image_path = f"images/{filename}"
    image = Image.open(image_path)
    w = image.width
    h = image.height

    # Define the text to add
    text = f"{quote}" + f"\n---{character}, {anime}"
    wrapper = textwrap.TextWrapper(width=50)
    word_list = wrapper.wrap(text=text)
    subtitle = ""
    for i in word_list[:-1]:
        subtitle = subtitle + i + '\n'
    subtitle += word_list[-1]

    # Define the font and font size
    font_path = "fonts/roboto-v30-latin-regular.ttf"
    font_size = 16
    font = ImageFont.truetype(font_path, font_size)

    
    draw = ImageDraw.Draw(image, 'RGBA')
    text_w, text_h = draw.textsize(subtitle, font=font)
    draw.text(xy=((w-text_w)/2,(h-text_h-40)), text=subtitle, fill=(255, 255, 255), font=font, align="center")


    # Save the new image
    image.save(image_path)

