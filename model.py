import joblib

def load_model(path="model/xgboost_model.pkl"):
    return joblib.load(path)

def predict_signal(model, features):
    last_row = features.iloc[-1:]
    prediction = model.predict(last_row)
    signal = "Buy" if prediction > 0.03 else "Sell" if prediction < -0.03 else "Hold"
    return signal, last_row.to_dict()
