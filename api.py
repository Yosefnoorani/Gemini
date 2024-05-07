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

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro-vision')

    img = Image.open(image_path)

    content = """
    The secret of success is -YKVK
    """
    response = model.generate_content([
                                          content,
                                          img], stream=True)
    response.resolve()
    print(model.count_tokens(response.text))
    print(response.text)

    return validateJSON(response)




def validateJSON(response):

    # STOP (1): Natural stop point of the model or provided stop sequence
    # https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform_v1.types.Candidate.FinishReason
    if (response.candidates[0].finish_reason == 1):
        result = response.text
        result = result.rstrip("`")
        result = result[result.find('{'):]

        parsed_data = json.loads(result)

        # Add the "success" key as the first key
        updated_data = {'success': True}

        # Add the original JSON data under the "data" key
        updated_data['data'] = parsed_data

        # Convert the updated data back to JSON
        updated_json = json.dumps(updated_data)
        # print("Success")
        print(updated_json)
        return updated_json


    else:
        # print("Error")
        updated_data = {
            "success": False,
            "data": str(response.candidates[0].safety_ratings)
        }

        # Convert the updated data to JSON
        updated_json = json.dumps(updated_data)

        print(updated_json)
        return updated_json



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
    # print(generated_text)
    return generated_text


if __name__ == '__main__':
    app.run(debug=True)
