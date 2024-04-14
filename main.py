import pathlib
import textwrap
from PIL import Image

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown



def to_markdown(text):
  text = text.replace('•', '  *')
  print(text)
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    GOOGLE_API_KEY = 'AIzaSyAPl3if3Qhr5i1dmSLD_RVyZT_p9nyTneM'

    genai.configure(api_key=GOOGLE_API_KEY)

    #for m in genai.list_models():
    #    if 'generateContent' in m.supported_generation_methods:
    #        print(m.name)

    # model = genai.GenerativeModel('gemini-pro-vision')
    model = genai.GenerativeModel('gemini-pro')


    img = Image.open('C:\\Users\\yosef\\Downloads\\photo_2024-04-09_16-08-24.jpg')

    #%%time
    # response = model.generate_content(["Describe the item on the picture and where i can buy it and give me other suggestion in similar product lower price", img], stream=True)
    response = model.generate_content(["Hi! Please provide a list of supported real devices on BrowserStack platform Please include the following devices in your list: Galaxy S24, Ultra Galaxy S24+, Galaxy S24, Galaxy Z Fold 5, Galaxy Z Flip 5, iPhone 15, Pro iPhone 15, iPhone 14, Pro  iPhone 14,iPhone SE (3rd), Pixel 5a, Pixel 6, Pixel 6 Pro, Pixel 6a, Pixel 7, Pixel 7 Pro, Pixel 7a, Pixel Fold Pixel 8, Pixel 8 Pro"], stream=True)

    response.resolve()

    #print(response)
    to_markdown(response.text)


