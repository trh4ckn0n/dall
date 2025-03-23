import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

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
    nom_hacker = st.text_input("💾 Nom/Pseudo à afficher", "TRKN")
    style = st.selectbox("🎭 Style du personnage", ["Hacker", "Cyberpunk", "Rapeur", "Anonymous", "Deal", "Dark", "Street Art"])
    accessoires = st.multiselect("🛠 Accessoires", ["Smartphone Kali NetHunter", "His gun", "Laptop", "Lunettes futuristes", "Sac à dos tech", "Casque audio"], ["Smartphone Kali NetHunter"])
    expression = st.selectbox("😎 Expression du visage", ["Furieux", "Souriant", "Menaçant", "Mystérieux"])
    genre = st.radio("🧑 Genre", ["Masculin", "Féminin", "Androgyne"], index=0)

with col2:
    ambiance = st.selectbox("🌆 Ambiance", ["Ruelle sombre", "Ville futuriste", "Bureau high-tech", "Forêt cyberpunk", "Bunker secret", "Mur de graffitis"])
    couleur_veste = st.color_picker("🎨 Couleur de la veste", "#000000")
    lumiere = st.slider("🔆 Intensité de la lumière", 1, 10, 5)
    fumee = st.checkbox("🌫 Ajouter de la fumée", value=True)

# Génération du prompt amélioré avec intelligence
accessoires_str = ", ".join(accessoires) if accessoires else "aucun accessoire"
fumee_str = "with a mysterious fog in the background" if fumee else "with a clear background"

# Ajout d'éléments typiques du style "Street Art"
if style == "Street Art":
    style_description = "in a vibrant street art style, featuring graffiti, splashes of color, and urban textures such as concrete walls and spray-painted art."
else:
    style_description = f"in a {style.lower()} style"

# Prompt plus précis pour éviter les masses informes
prompt = (
    f"A realistic character of a {style.lower()} with a {genre.lower()} appearance, standing in a {ambiance.lower()}. "
    f"The character has a clear human face with distinct features, and a {couleur_veste} jogging jacket. "
    f"Add the name {nom_hacker} clearly displayed on the picture. "
    f"The character is holding {accessoires_str}. Their facial expression is {expression.lower()}. "
    f"The environment is detailed, featuring cinematic lighting at intensity {lumiere}. {fumee_str}. "
    f"The character is {style_description}. The face should be realistic with no distortions, and the character should appear human and young."
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

    # Télécharger l'image générée
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Ajouter le masque Anonymous (exemple)
    # Assurez-vous d'avoir un fichier local du masque ou une URL de celui-ci
    mask_url = "https://d.top4top.io/p_33694elrz0.png"  # Remplacez par l'URL de votre masque
    mask_response = requests.get(mask_url)
    mask = Image.open(BytesIO(mask_response.content))

    # Redimensionner le masque pour qu'il s'adapte à l'image
    mask_size = (img.width // 5, img.height // 4)  # Taille ajustée en fonction de l'image
    mask = mask.resize(mask_size)

    # Positionner le masque sur l'image
    mask_position = (img.width // 8, img.height // 6)  # Positionner à une position centrale
    img.paste(mask, mask_position, mask)  # Appliquer le masque avec transparence

    # Afficher l'image modifiée
    st.image(img, caption=f"Avatar avec masque Anonymous pour {nom_hacker}", use_container_width=True)

    # Ajouter un bouton de téléchargement pour l'image modifiée
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    st.download_button(label="📥 Télécharger l'image avec masque", data=img_byte_arr, file_name=f"{nom_hacker}_avatar_with_mask.png")
