from utils import *
import csv
import os


def main():
    # Get quote from anime api
    while True:
        try:
            data = get_quote()
            break
        except Exception as error:
            print("Connection failed", error)
        
    anime = data['anime']
    character = data['character']
    quote = data['quote']
    
    
    # chatGPT help to come up with prompt ideas
    user_input = 'anime: %s, character: %s, quote: %s',(anime, character, quote)
    # prompt guide
    generate_prompt_guide(user_input)

    prompt = input('Enter your prompt:\n\n')
    # Generate image(s)
    img = generate_ai_art(prompt, quote, character, anime)

    fname = 'prompt_img.csv'
    header_row = ['prompt', 'image_name']

    data_row = [prompt, img]

    if os.path.exists(fname):
        with open(fname, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_row)
    else:
        with open(fname, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header_row)
            writer.writerow(data_row)




if __name__ == '__main__':
    main()
    

