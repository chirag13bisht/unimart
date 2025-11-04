from celery import shared_task
from .models import Listing
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import logging # <-- ADD THIS

# --- 1. Get a logger ---
logger = logging.getLogger(__name__)

# --- 2. Load the AI Model ---
try:
    model = tf.keras.applications.MobileNetV2(weights="imagenet")
    # --- CHANGED to logger.info ---
    logger.info("MobileNetV2 model loaded successfully.") 
except Exception as e:
    # --- CHANGED to logger.error ---
    logger.error(f"!!!!!!!! FAILED TO LOAD TENSORFLOW MODEL: {e} !!!!!!!!")
    model = None


def get_auto_description(label, product):
    # (This function is unchanged)
    label_to_category = {
        "notebook": "Stationery",
        "laptop": "Electronics",
        "headphone": "Electronics",
        "textbook": "Books",
        "book_jacket": "Books",
        "calculator": "Electronics",
        "mouse": "Electronics",
    }
    
    category = "Others"
    for key, cat in label_to_category.items():
        if key in label:
            category = cat
            break
    
    name = label.replace("_", " ").capitalize()
    description = f"Auto-generated description: A {name} in [Condition] condition. Add more details!"
    
    return name, description, category


@shared_task
def process_product_image(product_id):
    if model is None:
        # --- CHANGED to logger.warning ---
        logger.warning("Model not loaded, skipping task.")
        return
        
    try:
        product = Listing.objects.get(id=product_id)
    except Listing.DoesNotExist:
        logger.warning(f"Listing {product_id} not found.")
        return

    if not product.image:
        logger.warning(f"Listing {product_id} has no image.")
        return
        
    image_path = os.path.join('F:/afcat/unimart', product.image.url.lstrip('/'))
    
    try:
        img = Image.open(image_path).resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        preprocessed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_batch)

        predictions = model.predict(preprocessed_img)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0][0]
        label = decoded[1]
        score = decoded[2]
        
        logger.info(f"Prediction for Listing {product_id}: {label} (Score: {score})")
        
        if score > 0.3:
            name, description, category = get_auto_description(label, product)
            
            product.name = name
            product.description = description
            product.category = category
        
        product.status = 'active'
        product.save()
        logger.info(f"Listing {product_id} updated and set to active.")
        
    except Exception as e:
        logger.error(f"Error processing listing {product_id}: {e}")