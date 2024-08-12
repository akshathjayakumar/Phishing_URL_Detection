def get_prediction(url, model_path):
    model = load_model('/Users/akshathjayakumar/artificialintelligenceprojects/Phishing_URL_Detection/models/phishing_model.h5')

    features = prepare_features(url)
    raw_prediction = model.predict(features)

    print(f"Raw prediction value: {raw_prediction}")

    # Ensure the prediction is between 0 and 1
    if isinstance(raw_prediction, (list, np.ndarray)):
        prediction = raw_prediction[0]
    else:
        prediction = raw_prediction

    if not (0 <= prediction <= 1):
        raise ValueError(f"Prediction out of range: {prediction}")

    return prediction
