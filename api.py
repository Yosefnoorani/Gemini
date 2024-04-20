import os
from PIL import Image
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate_content(image_path):
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro-vision')

    img = Image.open(image_path)
    # content = """I am looking for such a product. Can you provide me 1. What is the name of
    # the manufacturer of the product (Only the name)2. What is the name of the product
    # 3. Describe and expand knowledge about the product 4. Give me a technical specification
    # about the product 5. Offer me cheaper similar products with prices 6.
    # URL to the store to purchase the original product"""

    content = """I am looking for such a product. Can you provide me (Response in JSON format): 
                    "companyName": What is the name of the manufacturer of the product (Only the name), 
                    "productName": What is the name of the product,
                    "about": Describe and expand knowledge about the product, 
                    "techSpecs": Give me a technical specification about the product, 
                    "similarItem": Offer me cheaper similar products with prices, 
                    "purchaseURL": URL to the store to purchase the original product
                    """
    response = model.generate_content([
                                          content,
                                          img], stream=True)
    response.resolve()
    print(model.count_tokens(response.text))
    return response.text


@app.route('/', methods=['GET'])
def hello():
    return "hello"


@app.route('/generate', methods=['POST'])
def generate_from_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image = request.files['image']
    # print(image)
    if image.filename == '':
        return jsonify({'error': 'No selected image file'})

    # Save the image to a temporary location
    temp_image_path = 'temp_image.jpg'
    image.save(temp_image_path)

    # Generate content from the image
    generated_text = generate_content(temp_image_path)
    # generated_text = generate_content(image)
    # print(generated_text)
    os.remove(temp_image_path)
    return generated_text


if __name__ == '__main__':
    #YoSeFAIzaSyAPl3if3Qhr5i1dmSLD_RVyZT_p9nyTneM
    app.run(debug=True)
