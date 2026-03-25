import streamlit as st
import numpy as np
from scipy.stats import poisson

# Configuration de la page
st.set_page_config(page_title="AI ULTRA-SNIPER v24.0", layout="wide")

# تصميم CSS مخصص لواجهة احترافية
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .advice-box { background-color: #238636; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; border: 2px solid #2ea043; }
    .prediction-card { background-color: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 AI ULTRA-SNIPER PRO v24.0")
st.write("Analyse Algorithmique Avancée - Basé sur la Distribution de Poisson & Goal Expectancy")

# --- Sidebar: Input des données ---
with st.sidebar:
    st.header("📋 Paramètres du Match")
    st.info("Saisissez les statistiques de saison pour les deux équipes.")
    
    with st.expander("🏠 Équipe Domicile", expanded=True):
        home_name = st.text_input("Nom Domicile", "Altglienicke")
        home_scored = st.number_input("Buts marqués (Moy)", value=1.42, step=0.1)
        home_conceded = st.number_input("Buts encaissés (Moy)", value=1.19, step=0.1)

    with st.expander("🚀 Équipe Extérieur", expanded=True):
        away_name = st.text_input("Nom Extérieur", "Eilenburg")
        away_scored = st.number_input("Buts marqués (Moy) ", value=0.96, step=0.1)
        away_conceded = st.number_input("Buts encaissés (Moy) ", value=1.74, step=0.1)

# --- Calculs Algorithmiques ---
# Goal Expectancy (Force Attaque A * Faiblesse Défense B)
exp_home = (home_scored + away_conceded) / 2
exp_away = (away_scored + home_conceded) / 2

# Génération de la matrice de Poisson (jusqu'à 6 goals)
h_probs = [poisson.pmf(i, exp_home) for i in range(7)]
a_probs = [poisson.pmf(i, exp_away) for i in range(7)]
matrix = np.outer(h_probs, a_probs)

# Probabilités 1X2
p_home = np.sum(np.tril(matrix, -1)) * 100
p_draw = np.sum(np.diag(matrix)) * 100
p_away = np.sum(np.triu(matrix, 1)) * 100

# Probabilités Over/Under
over_1_5 = (1 - (matrix[0,0] + matrix[0,1] + matrix[1,0])) * 100
over_2_5 = (1 - np.sum([matrix[i,j] for i in range(3) for j in range(3-i)])) * 100
over_3_5 = (1 - np.sum([matrix[i,j] for i in range(4) for j in range(4-i)])) * 100
over_4_5 = (1 - np.sum([matrix[i,j] for i in range(5) for j in range(5-i)])) * 100

# BTTS
btts_yes = (1 - (h_probs[0] + a_probs[0] - (h_probs[0] * a_probs[0]))) * 100

# --- Affichage des Résultats ---
if st.button("📊 LANCER L'ANALYSE PROFONDE"):
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Probabilités de Match (1X2)")
        c1, c2, c3 = st.columns(3)
        c1.metric(f"🏠 {home_name}", f"{p_home:.1f}%", f"Odd: {100/p_home:.2f}")
        c2.metric("🤝 Nul", f"{p_draw:.1f}%", f"Odd: {100/p_draw:.2f}")
        c3.metric(f"🚀 {away_name}", f"{p_away:.1f}%", f"Odd: {100/p_away:.2f}")

        st.subheader("⚽ Analyse des Buts (Plus/Moins)")
        st.write(f"✅ **Plus de 1.5 Goals:** {over_1_5:.1f}% | **Plus de 2.5 Goals:** {over_2_5:.1f}%")
        st.write(f"✅ **Plus de 3.5 Goals:** {over_3_5:.1f}% | **Plus de 4.5 Goals:** {over_4_5:.1f}%")
        st.write(f"🔥 **Les deux équipes marquent (BTTS):** {'OUI' if btts_yes > 55 else 'NON'} ({btts_yes:.1f}%)")

    with col2:
        st.subheader("📍 Scores Corrects")
        # Top 3 scores
        scores = []
        for i in range(4):
            for j in range(4):
                scores.append((i, j, matrix[i,j]))
        top_scores = sorted(scores, key=lambda x: x[2], reverse=True)[:2]
        for s in top_scores:
            st.info(f"Score: {s[0]} - {s[1]} | Prob: {s[2]*100:.1f}%")

    # --- LE CONSEIL GOLD (L'Algorithme choisit le meilleur rهان) ---
    st.markdown("---")
    st.subheader("💎 CONSEIL ULTRA-SNIPER DU JOUR")
    
    # Logic de sélection de la meilleure option
    options = {
        f"Victoire {home_name}": p_home,
        f"Victoire {away_name}": p_away,
        "Double Chance 1X": p_home + p_draw,
        "Double Chance X2": p_away + p_draw,
        "Plus de 1.5 Goals": over_1_5,
        "Plus de 2.5 Goals": over_2_5,
        "BTTS - OUI": btts_yes
    }
    
    best_option = max(options, key=options.get)
    
    st.markdown(f"""
        <div class="advice-box">
            🚀 RÈHAN CONSEILLÉ : {best_option.upper()} <br>
            <span style="font-size: 16px; font-weight: normal;">Indice de confiance : {options[best_option]:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 ABDEALI NIFALI - Predict Nifali | Système d'analyse algorithmique v24.0")
