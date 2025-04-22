#for testing the model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

model = load_model('./model/potato.keras')
class_labels = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

img_path =  "PlantVillage/Potato___healthy/ff700844-68ad-4e99-8427-58a39c07f817___RS_HL 1860.JPG"
img = load_img(img_path, target_size=(256, 256, 3)) # Adjust size as per your model input
img_array = img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

predictions = model.predict(img_array)
print("Predictions:", predictions)
predicted_class = class_labels[np.argmax(predictions)]
print("Predicted Class:", predicted_class)