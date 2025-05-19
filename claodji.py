import streamlit as st
import hashlib
import os
import time

st.set_page_config(page_title="Emoji Login", layout="centered")

# Base emojis
emoji_list = [
    '😀','😁','😂','🤣','😃','😄','😅','😆',
    '😉','😊','😋','😎','😍','😘','😗','😙',
    '😚','🙂','🤗','🤩','🤔','🤨','😐','😑',
    '😶','🙄','😏','😣','😥','😮','🤐','😯',
    '😪','😫','🥱','😴','😌','😛','😜','😝',
    '🤤','😒','😓','😔','😕','🙃','🤑','😲',
    '☹️','🙁','😖','😞','😟','😤','😢','😭',
    '😦','😧','😨','😩','🤯','😬','😰','😱',
]

# Initialisation
if 'stored_password' not in st.session_state:
    st.session_state['stored_password'] = None
    st.session_state['stored_salt'] = None
if 'selected_emojis' not in st.session_state:
    st.session_state['selected_emojis'] = []
if 'connected' not in st.session_state:
    st.session_state['connected'] = False

def hash_emoji_sequence(emoji_sequence, salt=None):
    raw = ''.join(emoji_sequence)
    if salt is None:
        salt = os.urandom(16)
    data = raw.encode('utf-8') + salt
    hashed = hashlib.sha256(data).hexdigest()
    return hashed, salt

# Titre
st.markdown("##  Connexion avec Emoji - Secure & Fun")
st.markdown("### Choisis tes emojis pour te connecter ou créer un mot de passe !")

# Affichage "champ emoji"
st.markdown("####  Champ emoji :")
st.text_input("Ta sélection :", value=''.join(st.session_state['selected_emojis']), label_visibility="collapsed", disabled=True)

# Clavier Emoji 8x8
st.markdown("#### Clavier emoji (clique pour les ajouter)")
cols = st.columns(8)
for i, emoji in enumerate(emoji_list):
    if cols[i % 8].button(emoji, key=f"emoji_{i}"):
        st.session_state['selected_emojis'].append(emoji)
        st.rerun()

# Boutons d'action
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧠 Créer mot de passe"):
        if not st.session_state['selected_emojis']:
            st.error("⚠️ Mot de passe vide, choisis au moins un emoji !")
        else:
            hashed, salt = hash_emoji_sequence(st.session_state['selected_emojis'])
            st.session_state['stored_password'] = hashed
            st.session_state['stored_salt'] = salt
            st.success("Mot de passe enregistré avec succès !")

with col2:
    if st.button(" Se connecter"):
        if st.session_state['stored_password'] is None:
            st.error("Aucun mot de passe enregistré.")
        elif not st.session_state['selected_emojis']:
            st.error("Mot de passe vide.")
        else:
            hashed_input, _ = hash_emoji_sequence(st.session_state['selected_emojis'], st.session_state['stored_salt'])
            if hashed_input == st.session_state['stored_password']:
                st.session_state['connected'] = True
                st.success("Connexion réussie ! Redirection...")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error(" Mot de passe incorrect !")

with col3:
    if st.button("Effacer"):
        st.session_state['selected_emojis'] = []
        st.rerun()

# 🎉 Redirection si connecté
if st.session_state['connected']:
    st.markdown("""<div style='text-align:center; font-size:48px;'>🎉 Bienvenue à toi ! 🎊</div>""", unsafe_allow_html=True)
    st.balloons()
    st.markdown("---")
    st.markdown("### Voici ta page d’accueil amusante ")
    st.markdown("""
    - Joue avec les emojis
    - Dashboard à venir
    - Sécurité max
    - Tu es prêt pour le fun !
    """)

    # Bouton pour se déconnecter
    if st.button("Se déconnecter"):
        st.session_state['connected'] = False
        st.session_state['selected_emojis'] = []
        st.experimental_rerun()
st.markdown("---")
feedback = st.text_area("💬 Laisse un avis ou une idée !")
if st.button("Envoyer le feedback"):
    with open("feedbacks.txt", "a") as f:
        f.write(feedback + "\n----\n")
    st.success("Merci pour ton retour ! 💖")

