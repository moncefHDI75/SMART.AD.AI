# 🔌 Étape 1 : Construire un moteur de scoring simple
# But : attribuer un score à chaque campagne pub selon ses résultats (CTR + conversions)


# Tu auras besoin de modules standards
import operator
import random
import matplotlib.pyplot as plt 
import numpy as np 
import csv
import streamlit as st
import pandas as pd
import git
from dotenv import load_dotenv
import os
import openai


load_dotenv()
st.image("assets/logo_smartadai.png", width=200)


# 📌 Listes de textes publicitaires (accroches)
textes = [
    "🔥 Brûle ta graisse comme un volcan",
    "🌿 Minceur naturelle, énergie pure",
    "💥 Active ton métabolisme en 7 jours",
    "✨ Silhouette & confiance retrouvées",
]

# 🎯 Cibles d’audience
audiences = [
    "Femmes 18-25",
    "Femmes 25-45",
    "Hommes 20-40",
    "Personnes 40+",
]

# 🖼️ Simuler des visuels/images
visuels = [
    "visuel_slim_volcan.jpg",
    "visuel_detox_vert.jpg",
    "visuel_confiance_femme.jpg",
    "visuel_energie_café.jpg",
]

# 🧠 Générer automatiquement toutes les combinaisons
publicites = []
for texte in textes:
    for audience in audiences:
        for visuel in visuels:
            publicites.append({
                "texte": texte,
                "audience": audience,
                "visuel": visuel,
                "ctr": round(random.uniform(0.01, 0.08), 3),  # CTR simulé
                "conversion": random.randint(0, 5),            # conversions simulées
            })

# 🧮 Ajouter un score de performance pour chaque pub
def score_pub(pub):
    return round(pub["ctr"] * 100 + pub["conversion"] * 10, 2)

# Appliquer le score
for pub in publicites:
    pub["score"] = score_pub(pub)

# 🏆 Trier par meilleur score
publicites = sorted(publicites, key=lambda x: x["score"], reverse=True)

# 🖨️ Afficher les 5 meilleures pubs à relancer
print("\n🔝 Top 5 pubs à relancer :\n")
for i in range(5):
    p = publicites[i]
    print(f"{i+1}. [{p['audience']}] '{p['texte']}' avec {p['visuel']} | Score: {p['score']} | CTR: {p['ctr']} | Conversions: {p['conversion']}")




# 📁 Nom du fichier CSV
nom_fichier = "publicites.csv"

# 📝 En-têtes du fichier
entetes = ["texte", "audience", "visuel", "ctr", "conversion", "score"]

# 💾 Enregistrement dans le fichier CSV
with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=entetes)
    writer.writeheader()
    for pub in publicites:
        writer.writerow(pub)

print(f"\n✅ Toutes les publicités ont été enregistrées dans : {nom_fichier}")

# 📥 Chargement du fichier
df = pd.read_csv("publicites.csv")

# 📊 Analyse simple
print("\n🎯 Score moyen par audience :")
print(df.groupby("audience")["score"].mean().round(2))

print("\n🔥 Top 3 publicités par score :")
print(df.sort_values(by="score", ascending=False).head(3)[["texte", "audience", "score"]])

print("\n📈 CTR moyen par texte :")
print(df.groupby("texte")["ctr"].mean().round(3))

print("\n🧠 Visuel le plus performant :")
best_visuel = df.groupby("visuel")["score"].mean().idxmax()
print(f"🏆 {best_visuel}")


df = pd.read_csv("publicites.csv")

st.title("🧠 SmartAdAI - Analyse de Publicités IA")

st.subheader("📊 Analyse des campagnes")
st.dataframe(df.sort_values("score", ascending=False).reset_index(drop=True))

st.subheader("🏆 Pub la plus performante")
best = df.sort_values("score", ascending=False).iloc[0]
st.success(f"Texte : {best['texte']}\n\nAudience : {best['audience']}\n\nScore : {best['score']}")

st.subheader("📈 Moyennes générales")
st.write(df.groupby("audience")[["score", "ctr", "conversion"]].mean().round(2))

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Chargement du fichier de pubs
df = pd.read_csv("publicites.csv")

st.title("🎯 SmartAdAI - Booster d'Affiliation IA")

st.subheader("🧾 1. Tableau des publicités enregistrées")
st.dataframe(df.sort_values("score", ascending=False), use_container_width=True)

# Entraînement du modèle IA
features = df[["texte", "audience", "visuel"]]
target = df["score"]
encoder = OneHotEncoder()
features_encoded = encoder.fit_transform(features).toarray()

model = LinearRegression()
model.fit(features_encoded, target)

# 🧠 2. Prédire une nouvelle pub
st.subheader("🧠 2. Tester une nouvelle publicité")
with st.form("form_pub"):
    texte = st.selectbox("Texte :", df["texte"].unique())
    audience = st.selectbox("Audience :", df["audience"].unique())
    visuel = st.selectbox("Visuel :", df["visuel"].unique())
    submitted = st.form_submit_button("Prédire le score IA")

    if submitted:
        nouvelle_pub = pd.DataFrame([[texte, audience, visuel]], columns=["texte", "audience", "visuel"])
        nouvelle_encoded = encoder.transform(nouvelle_pub).toarray()
        prediction = model.predict(nouvelle_encoded)[0]
        st.success(f"🔮 Score prédit pour cette pub : **{round(prediction, 2)}**")

# ⚙️ 3. Génération automatique de pubs avec prédiction
st.subheader("⚙️ 3. Générer 3 pubs automatiquement")

textes = df["texte"].unique()
audiences = df["audience"].unique()
visuels = df["visuel"].unique()

if st.button("🚀 Générer maintenant"):
    pubs_auto = []
    for _ in range(3):
        t = np.random.choice(textes)
        a = np.random.choice(audiences)
        v = np.random.choice(visuels)
        enc = encoder.transform([[t, a, v]]).toarray()
        pred = model.predict(enc)[0]
        pubs_auto.append({"Texte": t, "Audience": a, "Visuel": v, "Score IA": round(pred, 2)})

    st.write("🔎 Résultat des pubs générées avec IA :")
    st.dataframe(pd.DataFrame(pubs_auto), use_container_width=True)

# 🏆 4. Affichage pub gagnante


import requests

access_token = "EAAZAlsxoMVwABPP61YBJqPRX9ElWmAu7Byp1kjMg0qoBzWd2mrekS7W23mJHArsKZCdDKA91e1YS5C6jxGYOpKZBiOgeRBD4aBZByOufNtIdLsvxEHfqFLi9dJA1ENywxXt0jyAeQoCpEBsjB5D49LjwZCGvYhVWv0kZCivs4UKh7dEF8ulggocnLfaKf6xaZBh1deZA"
ad_account_id = "act_2878155125719207"
url = f"https://graph.facebook.com/v18.0/{61578534715230}/campaigns"

params = {
    "access_token": access_token,
    "fields": "name,status,effective_status,daily_budget"
}

response = requests.get(url, params=params)
print(response.json())







