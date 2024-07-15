from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

data = open('dados.json', "r")
characters_dict = json.load(data)["Champions"]

# Directory where images are stored
image_dir = os.path.join(app.root_path, 'Nova pasta')

@app.route('/champion')
def get_champion():
    name = request.args.get('name')
    
    if name:
        champion_info = characters_dict.get(name)
        if champion_info:
            # Add image URL to the champion info
            image_filename = champion_info.get("Image")
            if image_filename:
                champion_info["image_url"] = request.url_root + 'static/images/' + image_filename
            
            return jsonify({name: champion_info})
        else:
            return jsonify({"Message": "Champion not found!"}), 4
        
@app.route('/static/images/<filename>')
def get_image(filename):
    return send_from_directory(image_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
