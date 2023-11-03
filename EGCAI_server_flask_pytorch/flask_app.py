"""
Created on 16/Jul/2023

@author: Liaorl
"""

import os
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from nn.networks import *
from nn.utils import *
import torch
from torchvision import transforms
from PIL import Image

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = 'cpu'

##################### Neural Network Model Initialization ##############################
print("Loading stain_A2B_model model...")


def load_model(path_to_model):
    model = ResnetGenerator(input_nc=3, output_nc=3, ngf=64, n_blocks=4, img_size=256,
                            light=True).to(device)
    filename = os.path.join(path_to_model)
    map_location = device
    params = torch.load(filename, map_location=map_location)
    model.load_state_dict(params['genA2B'])
    model.eval()
    return model


def preprocess(image_path, transform, device):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    return image.to(device)


def postprocess(tensor):
    tensor = tensor.detach().cpu().squeeze(0)
    tensor = 0.5 * (tensor + 1.0)
    tensor = tensor.clamp(0.0, 1.0)
    return tensor.permute(1, 2, 0).numpy()


def predict(image_path, model):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])

    image = preprocess(image_path, transform, device)
    with torch.no_grad():
        output = model(image)
    output = output[0]

    return postprocess(output)


stain_A2B_model = load_model('./nn/params.pt')

print('Load Model Success!')

##################### Neural Network Model Initialization ##############################

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the folder for uploading if not exist
if not os.path.exists(UPLOAD_FOLDER):
    print("Creating folder for saving uploaded images...")
    os.mkdir(UPLOAD_FOLDER)
    print("<" + UPLOAD_FOLDER + "> created.")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploadedFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploadedFile)

        try:
            output_image = predict(uploadedFile, stain_A2B_model)
            # Convert the numpy array image to PIL image
            output_image_pil = Image.fromarray((output_image * 255).astype(np.uint8))

            # Define the directory for saving the output images
            output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the output image
            output_image_path = os.path.join(output_dir, 'output_' + filename)
            output_image_pil.save(output_image_path)

            # Construct the URL for the output image
            output_image_url = request.url_root + os.path.relpath(output_image_path, start=os.getcwd())

            return jsonify({"msg": "success", "image_url": output_image_url})

        except Exception as e:
            print(e)
            return jsonify({"msg": "error"})

    return jsonify({"msg": "Invalid file. Please upload a valid image file."})


@app.route('/upload/output/<filename>')
def send_image(filename):
    return send_from_directory('upload/output', filename)
    
@app.route('/')
def welcome():
    return 'Welcome to the Flask App!'


if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0', port=9999)
