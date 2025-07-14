import streamlit as st
from modules import image_generator, slogan_generator, video_generator, analyzer, ab_tester, targeting_ai

st.set_page_config(page_title="SmartAdAI", layout="centered")
st.title("🎯 SmartAdAI - Générateur de Pubs IA pour Affiliation")

option = st.selectbox("Choisis un module IA :", [
    "🎨 Générer une image publicitaire",
    "📢 Générer un slogan convaincant",
    "🎞️ Créer une vidéo IA",
    "📈 Analyse des performances",
    "🧪 Test A/B intelligent",
    "👥 Recommandation de ciblage"
])

if option == "🎨 Générer une image publicitaire":
    image_generator.run()
elif option == "📢 Générer un slogan convaincant":
    slogan_generator.run()
elif option == "🎞️ Créer une vidéo IA":
    video_generator.run()
elif option == "📈 Analyse des performances":
    analyzer.run()
elif option == "🧪 Test A/B intelligent":
    ab_tester.run()
elif option == "👥 Recommandation de ciblage":
    targeting_ai.run()
# modules/targeting_ai.py
import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def run():
    st.subheader("👥 Ciblage IA - Trouve ton audience idéale")

    produit = st.text_input("Produit à promouvoir :", "Collagène+ Beauté")
    type_produit = st.text_input("Type de produit (santé, fitness, tech...) :", "santé")
    objectif = st.selectbox("Objectif marketing :", ["Vente directe", "Génération de leads", "Trafic vers site", "Abonnement"])

    if st.button("Générer recommandation IA"):
        with st.spinner("Analyse en cours..."):
            prompt = f"Tu es une IA de marketing digital. Recommande un ciblage précis (pays, tranche d'âge, genre, centres d’intérêt Facebook) pour un produit '{produit}' ({type_produit}). Objectif : {objectif}."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            ciblage = response.choices[0].message.content.strip()
            st.success("🎯 Ciblage IA recommandé :")
            st.write(ciblage)

