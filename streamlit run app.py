
import operator
import random
import matplotlib.pyplot as plt 
import numpy as np 
import csv
import streamlit as st
import pandas as pd
import git
from dotenv import load_dotenv
import openai

import pandas as pd

df = pd.read_csv("ventes.csv")  # <- créer df à partir du fichier


st.subheader("🏆 Pub la plus performante enregistrée")
best = df.sort_values("score", ascending=False).iloc[0]
st.markdown(f"""
**Texte :** {best['texte']}  
**Audience :** {best['audience']}  
**Score :** ⭐ {round(best['score'], 2)}
""")
st.set_page_config(page_title="SmartAdAI", page_icon="📈", layout="wide")

# 🖼️ Logo & design
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .main {
        background-color: #0e1117;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("logo_smartadai.png", width=200)
st.markdown("## Bienvenue sur SmartAdAI - ton assistant pub intelligent 🧠")

import requests

def publier_sur_facebook(ad_text, image_url, access_token, page_id):
    url = f"https://graph.facebook.com/v18.0/act_{page_id}/ads"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "name": "SmartAdAI Auto Ad",
        "adset_id": "TON_ADSET_ID",
        "creative": {
            "title": ad_text,
            "image_url": image_url
        },
        "status": "PAUSED"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

st.download_button("📥 Télécharger le top pub", best.to_csv().encode('utf-8'), "top_pub.csv")

import os

best = df.sort_values("score", ascending=False).iloc[0]
image_path = os.path.join("assets", best["visuel"])

st.subheader("🖼️ Visuel de la meilleure pub")
if os.path.exists(image_path):
    st.image(image_path, caption=best["visuel"], use_column_width=True)
else:
    st.warning("❌ Image introuvable : " + image_path)
