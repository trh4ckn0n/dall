import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Customisation UI
st.set_page_config(page_title="Avatar 3D Generator", layout="wide")

st.markdown("<h1 style='text-align: center;'>🎨 Générateur d'Avatars 3D</h1>", unsafe_allow_html=True)
st.write("🚀 Personnalise ton avatar avec des options avancées et génère une image 3D unique.")

# 🔹 Personnalisation avancée
col1, col2 = st.columns(2)

with col1:
    nom_hacker = st.text_input("💾 Nom/Pseudo à afficher", "TRHACKNON")
    style = st.selectbox("🎭 Style du personnage", ["Hacker", "Cyberpunk", "Rapeur", "Anonymous", "Deal", "Dark"])
    accessoires = st.multiselect("🛠 Accessoires", ["Smartphone Kali NetHunter", "Laptop", "Lunettes futuristes", "Sac à dos tech", "Casque audio"], ["Smartphone Kali NetHunter"])
    expression = st.selectbox("😎 Expression du visage", ["Furieux", "Souriant", "Menaçant", "Mystérieux"])
    genre = st.radio("🧑 Genre", ["Masculin", "Féminin", "Androgyne"], index=0)

with col2:
    ambiance = st.selectbox("🌆 Ambiance", ["Ruelle sombre", "Ville futuriste", "Bureau high-tech", "Forêt cyberpunk", "Bunker secret"])
    couleur_veste = st.color_picker("🎨 Couleur de la veste", "#000000")
    lumiere = st.slider("🔆 Intensité de la lumière", 1, 10, 5)
    fumee = st.checkbox("🌫 Ajouter de la fumée", value=True)

# Génération du prompt amélioré avec intelligence
accessoires_str = ", ".join(accessoires) if accessoires else "aucun accessoire"
fumee_str = "with a mysterious fog in the background" if fumee else "with a clear background"

prompt = (
    f"A street life 3D character of a {style.lower()} with a {genre.lower()} appearance, with the name of hacker :'{nom_hacker}' correctly spelled and clearly displayed on the image, standing in a {ambiance.lower()}. "
    f"The character wears a {couleur_veste} hoodie with 'guy fawkes mask logo' clearly displayed. "
    f"They hold {accessoires_str}. Their facial expression is {expression.lower()}. "
    f"The environment is detailed, featuring cinematic lighting at intensity {lumiere}. {fumee_str}."
)

st.write(f"📜 **Prompt utilisé :** {prompt}")

# Bouton de génération
if st.button("🚀 Générer l'Avatar"):
    with st.spinner("Génération en cours... ⏳"):
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response["data"][0]["url"]
    
    st.image(image_url, caption=f"Avatar généré pour {nom_hacker}", use_container_width=True)

    # Ajout d'un bouton de téléchargement
    st.download_button(label="📥 Télécharger l'image", data=image_url, file_name=f"{nom_hacker}_avatar.png")
