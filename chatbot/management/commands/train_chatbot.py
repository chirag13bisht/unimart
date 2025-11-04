import spacy
import random
from django.core.management.base import BaseCommand
from spacy.training.example import Example

# Import our training data from the file we just created
from chatbot.training_data import TRAIN_DATA

class Command(BaseCommand):
    help = 'Trains the spaCy NER model for the chatbot'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting chatbot training...'))

        # Create a blank English model
        nlp = spacy.blank("en")

        # --- 1. Set up the NER pipeline ---
        if "ner" not in nlp.pipe_names:
            ner = nlp.add_pipe("ner", last=True)
        else:
            ner = nlp.get_pipe("ner")

        # Add all our custom labels (ITEM_TYPE, COURSE_CODE, etc.)
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2]) # Adds the label (e.g., "ITEM_TYPE")

        self.stdout.write(self.style.SUCCESS(f'Added labels: {ner.labels}'))

        # --- 2. Run the training ---
        # We want to disable other pipes (like 'tagger', 'parser') during training
        # This makes training faster and more focused on NER
        pipe_exceptions = ["ner"]
        unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

        # Start the training
        with nlp.disable_pipes(*unaffected_pipes):
            optimizer = nlp.begin_training()

            # Train for 10 iterations (or "epochs")
            for itn in range(10):
                random.shuffle(TRAIN_DATA)
                losses = {}

                for text, annotations in TRAIN_DATA:
                    try:
                        doc = nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
                    except Exception as e:
                        print(f"Error with data: {text} - {e}")

                self.stdout.write(self.style.SUCCESS(f'Iteration {itn+1}/10, Losses: {losses}'))

        # --- 3. Save the new model ---
        # We'll save it to a new folder called 'chatbot_model'
        model_dir = "chatbot_model"
        nlp.to_disk(model_dir)

        self.stdout.write(self.style.SUCCESS(f'Successfully trained and saved model to "{model_dir}"'))