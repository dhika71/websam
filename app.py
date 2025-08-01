import streamlit as st
from utils.features import load_data, create_features
from utils.model import load_model, predict_signal
from gemini.gemini_ai import explain_signal

st.title("📈 Hybrid Stock Analysis App (XGBoost + Gemini AI)")

ticker = st.text_input("Masukkan kode saham (Contoh: BBCA.JK)", value="BBCA.JK")
if st.button("Analisa"):
    df = load_data(ticker)
    features = create_features(df)
    model = load_model()
    signal, result = predict_signal(model, features)
    st.metric(label="📊 Prediksi Sinyal", value=signal)
    explanation = explain_signal(result)
    st.write("💡 Penjelasan AI:")
    st.info(explanation)
