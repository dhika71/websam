import joblib

def load_model(path='models/xgb_model.pkl'):
    # placeholder: return None atau model dummy
    try:
        return joblib.load(path)
    except FileNotFoundError:
        return None

def predict_signal(model, X):
    # placeholder: selalu return 'HOLD'
    if model is None:
        return 'No model'
    return model.predict(X)
