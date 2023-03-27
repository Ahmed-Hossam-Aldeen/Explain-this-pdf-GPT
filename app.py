from pdf2jpg import pdf2jpg
from glob import glob
import re
from PIL import Image
import easyocr

import openai
# Set up your API key
openai.api_key = " "

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

inputpath = "1.pdf"
outputpath = "output"

# to convert all pages
result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="ALL")
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

ocrs = []
explainations = []

for i in sorted_alphanumeric(glob(outputpath+f'/{inputpath}_dir/*')):
    result = reader.readtext(i,detail = 0)
    result = ' '.join(result)
    result = 'explain this: ' + result

    ocrs.append(result)

    # Set up the prompt you want to send to ChatGPT
    prompt = result

    # Send the API request
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=[{"role": "user", "content": prompt}])
    explainations.append(response['choices'][0]['message']['content'])

with open("ocr.txt", 'w') as output:
    for row in ocrs:
        output.write(str(row) + '\n'+ '--------------------------------'+ '\n')

with open("explainations.txt", 'w') as output:
    for row in explainations:
        output.write(str(row) + '\n'+ '--------------------------------'+ '\n')
