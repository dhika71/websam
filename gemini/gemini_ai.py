import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def explain_signal(input_features):
    prompt = f"""
    Saya punya fitur saham: {input_features}
    Berikan analisa teknikal & makro ekonomi sederhana, apakah ini sinyal BELI/JUAL?
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
