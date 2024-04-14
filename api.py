import os
import textwrap

import markdown
from PIL import Image
import google.generativeai as genai
from flask import Flask, request, jsonify
# from IPython.display import Markdown

app = Flask(__name__)


def generate_content(image_path):
    GOOGLE_API_KEY = 'AIzaSyAPl3if3Qhr5i1dmSLD_RVyZT_p9nyTneM'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision')

    img = Image.open(image_path)
    content = "I am looking for such a product. Can you provide me 1. What is the name of the manufacturer of the product (Only the name)2. What is the name of the product 3. Describe and expand knowledge about the product 4. Give me a technical specification about the product 5. Offer me cheaper similar products with prices 6. URL to the store to purchase the original product"
    response = model.generate_content([
                                        # ,
                                          # "Describe the item on the picture and where I can buy it and give me other suggestions for similar products at a lower price",
                                          # "give me other suggestions for similar products at a lower price",
                                        content,
                                          img], stream=True)
    response.resolve()
    print(model.count_tokens(response.text))
    return response.text


# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


@app.route('/', methods=['GET'])
def hello():
    return ("hello")


@app.route('/generate', methods=['POST'])
def generate_from_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image = request.files['image']
    print(image)
    if image.filename == '':
        return jsonify({'error': 'No selected image file'})

    # Save the image to a temporary location
    temp_image_path = 'temp_image.jpg'
    image.save(temp_image_path)

    # Generate content from the image
    generated_text = generate_content(temp_image_path)
    # generated_text = generate_content(image)
    print(generated_text)
    os.remove(temp_image_path)
    return generated_text

    # Delete the temporary image file
    # os.remove(temp_image_path)

    # markdown_text = to_markdown(generated_text)

    # Convert Markdown to HTML
    # html_content = markdown.markdown(generated_text)

    # Delete the temporary image file


    # return html_content

    # return markdown_text


if __name__ == '__main__':
    app.run(debug=True)
