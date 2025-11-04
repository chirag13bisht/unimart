from celery import shared_task
from .models import Rental_Listing  # <-- CHANGED to Rental_Listing
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

# --- 1. Load the AI Model ---
try:
    model = tf.keras.applications.MobileNetV2(weights="imagenet")
    logger.info("MobileNetV2 model loaded successfully.") 
except Exception as e:
    logger.error(f"!!!!!!!! FAILED TO LOAD TENSORFLOW MODEL: {e} !!!!!!!!")
    model = None


def get_auto_description(label, product):
    """
    This is our simple "NLG" (Natural Language Generation).
    It's the same as the mart app.
    """
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
def process_rental_image(product_id):
    """
    This is the main Celery task that runs in the background.
    """
    if model is None:
        logger.warning("Model not loaded, skipping task.")
        return
        
    try:
        # --- CHANGED to Rental_Listing ---
        product = Rental_Listing.objects.get(id=product_id)
    except Rental_Listing.DoesNotExist:
        logger.warning(f"Rental_Listing {product_id} not found.")
        return

    if not product.image:
        logger.warning(f"Rental_Listing {product_id} has no image.")
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
        
        logger.info(f"Prediction for Rental_Listing {product_id}: {label} (Score: {score})")
        
        if score > 0.3:
            name, description, category = get_auto_description(label, product)
            
            product.name = name
            product.description = description
            product.category = category
        
        product.status = 'Active' # Set to 'Active' (matching your model choice)
        product.save()
        logger.info(f"Rental_Listing {product_id} updated and set to active.")
        
    except Exception as e:
        logger.error(f"Error processing rental_listing {product_id}: {e}")