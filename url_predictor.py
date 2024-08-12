
from tensorflow import keras
from Feature_Extractor import extract_features


def get_prediction(url, model_path):
    model = keras.models.load_model(model_path)

    url_features = extract_features(url)

    prediction = model.predict([url_features])

    i = prediction[0][0] * 100
    i = round(i,3)

    return i
