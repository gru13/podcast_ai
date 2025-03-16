import gradio as gr
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"

def fetch_data():
    response = requests.get(API_URL)
    return response.json().get("message", "Error")

iface = gr.Interface(fn=fetch_data, inputs=[], outputs="text")
iface.launch()
