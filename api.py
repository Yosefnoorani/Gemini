import os
from PIL import Image
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

def generate_content(image_path):
    google_api_key = os.environ.get('GOOGLE_API_KEY')

    google_api_key = 'AIzaSyAPl3if3Qhr5i1dmSLD_RVyZT_p9nyTneM'


    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro-vision')

    img = Image.open(image_path)


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

    result = response.text
    # print(result)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Clean the Json
    result = result.rstrip("`")
    result = result[result.find('{'):]


    # result = result.lstrip(" ``` JSON")
    # result = result.lstrip("json")

    # print(result)
    result = validateJSON(result)
    if(result):
        return result
    else:
        return f"Unable to fix broken JSON"



def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        print(jsonData)
        print(err)

        # jsonData = """
        # {
        #     "companyName": "IWI",
        #     "productName": "Tavor X95",
        #     "about": "PlaceHolder"
        # }
        # """
        # jsonData = fix_broken_json(jsonData)
        print("EEEERRRRRRRRRRRRRRPORRRRR....")
        # print(jsonData)

    return jsonData


def fix_broken_json(broken_json):
    try:
        # Try parsing the JSON
        json.loads(broken_json)
        # If successful, return the original JSON
        return broken_json
    except json.JSONDecodeError as e:
        # If parsing fails, attempt to fix the JSON
        fixed_json = broken_json.replace("'", '"')  # Replace single quotes with double quotes
        fixed_json = fixed_json.replace("\\", "")  # Remove backslashes
        fixed_json = fixed_json.replace('\n', ' ')  # Remove newline characters
        fixed_json = fixed_json.replace('"\n"', '"Placeholder"')  # Replace empty string with placeholder
        # Try parsing the fixed JSON
        try:
            json.loads(fixed_json)
            return fixed_json
        except json.JSONDecodeError as e:
            # If still unsuccessful, return an error message
            return f"Unable to fix broken JSON: {e}"


@app.route('/', methods=['GET'])
def hello():
    return "Hello"


@app.route('/generate', methods=['POST'])
def generate_from_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    print("Start request")
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



    print("End response")
    print(generated_text)
    return generated_text


if __name__ == '__main__':
    #YoSeFAIzaSyAPl3if3Qhr5i1dmSLD_RVyZT_p9nyTneM
    app.run(debug=True)
