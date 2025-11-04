import pandas as pd
import joblib
from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import coo_matrix, vstack, csc_matrix

# --- NEW LIBRARY ---
import implicit.als
# -------------------

from recommender.models import UserEvent
from mart.models import Listing
from rental.models import Rental_Listing
from users.models import User
from django.contrib.contenttypes.models import ContentType
import numpy as np

# Define a consistent way to create unique item IDs
def get_item_id(item, model_type):
    return f"{model_type}_{item.id}"

class Command(BaseCommand):
    help = 'Trains the recommender system using the Implicit library'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting recommender training...'))

        # --- 1. Fetch All Data ---
        self.stdout.write('Fetching data from database...')
        
        events = UserEvent.objects.all().values('user_id', 'event_type', 'content_type_id', 'object_id')
        events_df = pd.DataFrame(list(events))

        mart_items = list(Listing.objects.filter(status='active'))
        rental_items = list(Rental_Listing.objects.filter(status='Active'))
        all_items = mart_items + rental_items
        
        all_user_ids = list(User.objects.values_list('id', flat=True))

        if events_df.empty or not all_items:
            self.stdout.write(self.style.ERROR('No event data or items found. Aborting.'))
            return

        # --- 2. Create Mappings ---
        self.stdout.write('Creating mappings...')
        user_id_to_index = {user_id: i for i, user_id in enumerate(all_user_ids)}
        
        item_id_map = {get_item_id(item, 'mart'): item for item in mart_items}
        item_id_map.update({get_item_id(item, 'rental'): item for item in rental_items})
        all_item_ids = list(item_id_map.keys())
        
        item_id_to_index = {item_id: i for i, item_id in enumerate(all_item_ids)}

        # --- 3. Build Interactions Matrix ---
        self.stdout.write('Building interactions matrix...')
        
        event_weights = {'view': 1.0, 'inquire': 5.0} # 'inquire' is 5x more important
        
        events_df['item_id_str'] = events_df.apply(
            lambda row: f"{'mart' if 'listing' in ContentType.objects.get_for_id(row['content_type_id']).model else 'rental'}_{row['object_id']}",
            axis=1
        )
        
        events_df = events_df[events_df['item_id_str'].isin(item_id_to_index)]
        events_df = events_df[events_df['user_id'].isin(user_id_to_index)]
        
        if events_df.empty:
            self.stdout.write(self.style.ERROR('No valid events to train on after filtering. Aborting.'))
            return

        user_indices = events_df['user_id'].map(user_id_to_index).values
        item_indices = events_df['item_id_str'].map(item_id_to_index).values
        weights = events_df['event_type'].map(event_weights).values
        
        interactions_matrix = coo_matrix((weights, (item_indices, user_indices)), 
                                         shape=(len(all_item_ids), len(all_user_ids)))

        # --- 4. Train the Collaborative Model ---
        self.stdout.write('Training the Implicit (ALS) collaborative model...')
        
        model = implicit.als.AlternatingLeastSquares(factors=50, regularization=0.01, iterations=20)
        
        model.fit(interactions_matrix)
        
        # --- 5. Train the Content-Based Model (Separate) ---
        self.stdout.write('Training the (TF-IDF) content-based model...')
        item_descriptions = [f"{item.name} {item.description} {item.category} {item.condition}" for item in all_items]
        
        vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
        item_features_matrix = vectorizer.fit_transform(item_descriptions)
        
       # --- 6. Save All Models and Mappings ---
        self.stdout.write('Saving models and mappings to disk...')
        
        mappings = {
            'user_id_to_index': user_id_to_index,
            'item_id_to_index': item_id_to_index,
            'all_item_ids': all_item_ids,
            'index_to_item_id': {i: item_id for item_id, i in item_id_to_index.items()}
        }
        
        joblib.dump(model, 'recommender_als_model.pkl') # Collaborative model
        joblib.dump((item_features_matrix, vectorizer), 'recommender_tfidf_model.pkl') # Content model
        joblib.dump(mappings, 'recommender_mappings.pkl')
        
        # --- ADD THIS LINE ---
        joblib.dump(interactions_matrix, 'recommender_interactions.pkl') # User-Item interactions
        # ---------------------

        self.stdout.write(self.style.SUCCESS('Recommender training complete!'))