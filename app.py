from flask import Flask, render_template, request, send_file, jsonify
import openai
import os
import requests
from io import BytesIO

app = Flask(__name__)

# Load the API key from an environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        headline = request.form.get("headline")
        prompt = generate_prompt(headline)
        return f"{prompt}"
    return render_template("index.html")

def generate_prompt(headline):
    result = openai.Completion.create(
        engine="text-davinci-003",
         prompt=(
            f"Create a prompt based on the following news article headline: '{headline}'. "
            f"Provide detailed descriptions, including the following aspects: "
            f"subject, event, location, camera angle, etc. "
            f"150 words maximum."
            f"Use commas to separate the elements in the description. "
            f"No full stops or any other punctuation, only commas. "
            f"Location should always be a futuristic or space theme. "
            f"Include verbs, nouns, numbers and $ prices found in the headline."
            f"Always follow this template: Subject: [very long description], Mood: [description], "
            f"Event: [long description], Location: [long description], Camera Angle: [description]."
        ),
        max_tokens=3200,
        n=1,
        stop=None,
        temperature=0.4,
    )

    return result.choices[0].text.strip()

@app.route("/generate-image", methods=["POST"])
def generate_image():
    prompt = request.form.get("prompt")
    image_urls = generate_image_from_prompt(prompt)
    return jsonify(image_urls=image_urls)

def generate_image_from_prompt(prompt):
    headers = {"Authorization": "Bearer " + openai.api_key}
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json={
            "model": "image-alpha-001",
            # modern cartoon style
            # nickelodeon
            # adventure time
            # rick and morty
            # black outlines,
            "prompt": "minimal cel shading cartoon style, colorful, crypto," + prompt + ", high quality",
            "num_images": 4,
            "size": "512x512",
            "response_format": "url",
        },
    )

    response.raise_for_status()
    image_urls = [img["url"] for img in response.json()["data"]]

    return image_urls

if __name__ == "__main__":
    app.run(debug=True)
