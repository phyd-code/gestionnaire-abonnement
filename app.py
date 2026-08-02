import json
import os
import streamlit as st
from datetime import datetime

FICHIER_DONNEES = "abonnements_web.json"

def charger_donnees():
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def sauvegarder_donnees(abonnements):
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(abonnements, f, indent=4, ensure_ascii=False)

st.set_page_config(page_title="Gestionnaire d'Abonnements Pro", page_icon="⚡", layout="centered")

# Gestion de l'état de navigation (Landing Page vs Application)
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ================= PAGE 1 : LA LANDING PAGE =================
if st.session_state.page == "landing":
    st.title("⚡ Reprenez le contrôle de vos abonnements")
    st.subheader("Ne payez plus jamais pour des services que vous n'utilisez plus.")
    
    st.write("")
    
    # Bouton d'appel à l'action (CTA) principal
    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        if st.button("🚀 Lancer l'application gratuitement", use_container_width=True, type="primary"):
            st.session_state.page = "app"
            st.rerun()

    st.divider()

    # Section des fonctionnalités phares
    st.markdown("### ✨ Pourquoi utiliser notre gestionnaire ?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📊 Vue d'ensemble**")
        st.write("Calculez instantanément vos dépenses mensuelles et annuelles en un clin d'œil.")
    with col2:
        st.markdown("**🔔 Zéro Oubli**")
        st.write("Suivez vos dates de prélèvement pour éviter les mauvaises surprises sur votre compte.")
    with col3:
        st.markdown("**🏷️ Organisation**")
        st.write("Classez vos services par catégories (Streaming, Logement, Logiciels, etc.).")

    st.divider()
    
    st.markdown("### 💡 Prêt à faire des économies ?")
    st.write("Rejoignez les utilisateurs qui maîtrisent enfin leur budget récurrent.")
    
    if st.button("Commencer dès maintenant"):
        st.session_state.page = "app"
        st.rerun()

# ================= PAGE 2 : L'APPLICATION PRINCIPALE =================
elif st.session_state.page == "app":
    # Bouton pour revenir à la landing page
    if st.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "landing"
        st.rerun()

    st.title("⚡ Votre Tableau de Bord")
    st.write("Gérez et suivez toutes vos dépenses récurrentes.")

    abonnements = charger_donnees()

    # --- FORMULAIRE D'AJOUT DANS LA BARRE LATÉRALE ---
    st.sidebar.header("➕ Ajouter un service")

    with st.sidebar.form("form_abo"):
        nom = st.text_input("Nom du service (ex: Netflix)")
        prix = st.number_input("Prix (€)", min_value=0.0, format="%.2f")
        categorie = st.selectbox("Catégorie", ["Streaming", "Logiciel", "Logement", "Loisirs", "Autre"])
        frequence = st.selectbox("Fréquence", ["Mensuel", "Annuel"])
        date_prelevement = st.date_input("Date du prochain prélèvement", datetime.now())
        
        valider = st.form_submit_button("Ajouter l'abonnement")

        if valider:
            if nom.strip() == "":
                st.sidebar.error("Veuillez entrer un nom de service valide.")
            else:
                nouveau = {
                    "nom": nom,
                    "prix": prix,
                    "cat": categorie,
                    "frequence": frequence,
                    "date": date_prelevement.strftime("%d/%m/%Y")
                }
                abonnements.append(nouveau)
                sauvegarder_donnees(abonnements)
                st.sidebar.success(f"'{nom}' a bien été ajouté !")
                st.rerun()

    # --- CALCULS ET TABLEAU DE BORD ---
    if abonnements:
        total_mensuel = 0
        total_annuel = 0

        for abo in abonnements:
            if abo["frequence"] == "Mensuel":
                total_mensuel += abo["prix"]
                total_annuel += abo["prix"] * 12
            else:
                total_annuel += abo["prix"]
                total_mensuel += abo["prix"] / 12

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Mensuel", f"{total_mensuel:.2f} €")
        col2.metric("Total Annuel", f"{total_annuel:.2f} €")
        col3.metric("Abonnements actifs", len(abonnements))

        st.divider()

        recherche = st.text_input("🔍 Rechercher un abonnement", "")
        
        st.subheader("Vos abonnements enregistrés")
        
        for i, abo in enumerate(abonnements):
            if recherche.lower() in abo["nom"].lower() or recherche.lower() in abo["cat"].lower():
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.write(f"**{abo['nom']}** ({abo['cat']}) — **{abo['prix']:.2f} €** / {abo['frequence'].lower()} — Prélèvement le : *{abo['date']}*")
                with col_btn:
                    if st.button("🗑️ Supprimer", key=f"supp_{i}"):
                        abonnements.pop(i)
                        sauvegarder_donnees(abonnements)
                        st.rerun()
    else:
        st.info("Aucun abonnement pour le moment. Utilisez le panneau à gauche pour en ajouter un !")