from flask import Flask, request, jsonify
import os
import asyncio
from telegram_bot import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/upload', methods=['POST'])
async def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_path = "betting_card.png"
    image_file.save(image_path)

    # Run the Telegram bot asynchronously
    asyncio.create_task(main(image_path))

    return jsonify({"message": "Image processed and sent to Telegram"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use dynamic port for Render
    app.run(host="0.0.0.0", port=port)
