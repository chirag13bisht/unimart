import joblib
import numpy as np
from mart.models import Listing
from rental.models import Rental_Listing
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix
import logging

logger = logging.getLogger(__name__)

# --- 1. Load all models and mappings (once, on server start) ---
try:
    als_model = joblib.load('recommender_als_model.pkl')
    tfidf_data = joblib.load('recommender_tfidf_model.pkl')
    mappings = joblib.load('recommender_mappings.pkl')
    
    # --- THIS IS THE FIX ---
    # Load the matrix of who interacted with what
    interactions_matrix = joblib.load('recommender_interactions.pkl')
    # We need the transpose (users x items) for the recommend function
    user_item_interactions = interactions_matrix.T.tocsr()
    # -----------------------

    tfidf_matrix, tfidf_vectorizer = tfidf_data
    
    user_id_to_index = mappings['user_id_to_index']
    item_id_to_index = mappings['item_id_to_index']
    index_to_item_id = mappings['index_to_item_id']
    all_item_ids = mappings['all_item_ids']

    logger.info("Recommender models loaded successfully.")

except FileNotFoundError:
    logger.error("Recommender model files not found. Run 'python manage.py train_recommender'.")
    als_model = None
except Exception as e:
    logger.error(f"Error loading recommender models: {e}")
    als_model = None

# --- 2. Function to get Collaborative (ALS) Recommendations ---

def get_recommendations_for_user(user_id, num_recs=10):
    """
    Gets personalized recommendations for a specific user.
    """
    if als_model is None:
        logger.warning("ALS model not loaded. Skipping recommendation.")
        return []

    user_index = user_id_to_index.get(user_id)
    if user_index is None:
        logger.warning(f"User {user_id} not in model. Cannot recommend.")
        return [] # This is a cold-start user

    # --- THIS IS THE FIX ---
    # Get recommendations from the ALS model
    # We pass the user_index and the matrix of all user interactions
    recommendations = als_model.recommend(
        user_index,
        user_item_interactions, # This filters out items the user already interacted with
        N=num_recs
    )
    # -----------------------
    
    recommended_item_indices = recommendations[0]
    
    recommended_ids = [index_to_item_id.get(idx) for idx in recommended_item_indices]
    
    return [rec_id for rec_id in recommended_ids if rec_id is not None]

# --- 3. Function to get Content-Based (Similar) Recommendations ---

def get_similar_items(item_id_str, num_recs=5):
    """
    Finds items that are textually similar to a given item.
    """
    if tfidf_matrix is None:
        logger.warning("TF-IDF model not loaded. Skipping similar items.")
        return []

    item_index = item_id_to_index.get(item_id_str)
    if item_index is None:
        logger.warning(f"Item {item_id_str} not in model. Cannot find similars.")
        return []

    item_vector = tfidf_matrix[item_index]
    cosine_similarities = cosine_similarity(item_vector, tfidf_matrix).flatten()
    similar_indices = cosine_similarities.argsort()[-(num_recs + 1):][::-1]
    similar_indices = [idx for idx in similar_indices if idx != item_index]
    similar_item_ids = [index_to_item_id.get(idx) for idx in similar_indices[:num_recs]]
    
    return [sim_id for sim_id in similar_item_ids if sim_id is not None]

# --- 4. Helper function to parse our Item IDs ---

def parse_and_fetch_items(item_id_list):
    """
    Takes a list like ['mart_5', 'rental_2'] and fetches the
    actual objects from the database.
    """
    mart_ids = []
    rental_ids = []
    
    for item_id in item_id_list:
        try:
            model_type, db_id = item_id.split('_')
            if model_type == 'mart':
                mart_ids.append(int(db_id))
            elif model_type == 'rental':
                rental_ids.append(int(db_id))
        except:
            continue
            
    mart_listings = list(Listing.objects.filter(id__in=mart_ids))
    rental_listings = list(Rental_Listing.objects.filter(id__in=rental_ids))
    
    return mart_listings + rental_listings