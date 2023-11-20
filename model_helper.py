"""
Incharge of loading the features dictionary and predicting a caption for an image.
"""
from enum import Enum
from pathlib import Path

import numpy as np

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from caption import idx_to_word

class ModelName(Enum):
    """
    Enum for the model names.
    """
    LESS_TRAINED_MODEL = "model.h5"
    EARLY_STOPPED_MODEL = "model (1).h5"

# def load_features_dict() -> dict:
#     """
#     Load the features dictionary from the file.
#     """
#     features_dict_path: Path = Path("./saves/features.pickle")
#     with open(features_dict_path, "rb") as handle:
#         features_dict: dict = pickle.load(handle)
#     return features_dict

def load_captioning_model(model_name: ModelName):
    """
    Load the model from the file.
    """
    model_path = Path(f"./saves/{model_name.value}")
    model = load_model(model_path)
    return model

def predict_caption_with_loop_handle(
        model,
        img_features: np.ndarray,
        tokenizer: Tokenizer,
        max_length: int,
        mut_in_text: str,
) -> str | None:
    """
    Given a model, an image, a tokenizer, and a dictionary of features,
    The default value for in_text is "startseq"
    Returns: 
    ---- 
    True if the caption is finished, False otherwise.
    """
    for _ in range(1):
        sequence = tokenizer.texts_to_sequences([mut_in_text])[0]
        sequence = pad_sequences([sequence], max_length)

        y_pred = model.predict([img_features, sequence])
        y_pred = np.argmax(y_pred)

        word = idx_to_word(int(y_pred), tokenizer)

        if word is None:
            return None

        mut_in_text += " " + word

        if word == "endseq":
            return None

    return mut_in_text

def predict_caption(
    model,
    img_features: np.ndarray,
    tokenizer: Tokenizer,
    max_length: int,
):
    """
    Given a model, an image, a tokenizer, a max length, and a dictionary of features, 
    return a caption for the image.
    """
    # check if all the values in the array are normalized

    in_text = "startseq"
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], max_length)

        y_pred = model.predict([img_features, sequence])
        y_pred = np.argmax(y_pred)

        word = idx_to_word(int(y_pred), tokenizer)

        if word is None:
            break

        in_text += " " + word

        if word == "endseq":
            break

    return in_text
