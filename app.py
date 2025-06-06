from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Load the trained model
model = load_model('model/potato.keras')
class_labels = ['Early Blight', 'Late Blight', 'Healthy']

# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    # Render the home page
    return render_template('index.html')

@app.route('/predictionPage')
def predictionPage():
    # Render a form for input
    return render_template('predictionPage.html', predicted_class=None, uploaded_image_path="")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    file_size = os.path.getsize(file_path) / 1024  # File size in KB
    return jsonify({"message": "File uploaded successfully", "file_size": f"{file_size:.2f} KB"})
    

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess the image
        img = load_img(filepath, target_size=(256, 256, 3))  # Adjust size as per your model input
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        predictions = model.predict(img_array)
        print("Predictions:", predictions)
        predicted_class = class_labels[np.argmax(predictions)]
        print("Predicted Class:", predicted_class)

        # Pass the predicted class and uploaded image path to the template
        uploaded_image_path = f'static/uploads/{filename}'
        return render_template('predictionPage.html', predicted_class=predicted_class, uploaded_image_path=uploaded_image_path)
    return redirect(request.url)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

