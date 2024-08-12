def get_prediction(url, model_path):
    # Load your model
    model = load_model('/Users/akshathjayakumar/artificialintelligenceprojects/Phishing_URL_Detection/models/phishing_model.h5')

    # Prepare the URL for prediction
    features = prepare_features(url)
    # Predict
    raw_prediction = model.predict(features)

    # Debug output
    print(f"Raw prediction value: {raw_prediction}")

    # Ensure the prediction is between 0 and 1
    if isinstance(raw_prediction, (list, np.ndarray)):
        prediction = raw_prediction[0]  # Adjust based on your output shape
    else:
        prediction = raw_prediction

    # Ensure prediction is in range
    if not (0 <= prediction <= 1):
        raise ValueError(f"Prediction out of range: {prediction}")

    return prediction
