# This is the training data for our custom NER model

# We define the entities and the text they're in.
# Format: (TEXT, {"entities": [(START_CHAR, END_CHAR, "LABEL")]})

TRAIN_DATA = [
    ("I'm looking for a textbook", {"entities": [(20, 28, "ITEM_TYPE")]}),
    ("Do you have any study guides?", {"entities": [(15, 27, "ITEM_TYPE")]}),
    ("I want to sell my calculator", {"entities": [(19, 29, "ITEM_TYPE")]}),
    ("Is anyone selling a laptop?", {"entities": [(19, 25, "ITEM_TYPE")]}),
    ("I need a notebook", {"entities": [(9, 17, "ITEM_TYPE")]}),

    # We can add course codes
    ("Looking for a CS 101 book", {"entities": [(15, 21, "COURSE_CODE"), (22, 26, "ITEM_TYPE")]}),
    ("Do you have the MATH 250 textbook?", {"entities": [(17, 26, "COURSE_CODE"), (27, 35, "ITEM_TYPE")]}),
    ("I'm selling my PHYS 110 lab coat", {"entities": [(16, 25, "COURSE_CODE"), (26, 34, "ITEM_TYPE")]}),

    # We can also add brand names
    ("I need a used Apple laptop", {"entities": [(14, 19, "BRAND"), (20, 26, "ITEM_TYPE")]}),
    ("Is there a Dell charger?", {"entities": [(11, 15, "BRAND"), (16, 23, "ITEM_TYPE")]})
]