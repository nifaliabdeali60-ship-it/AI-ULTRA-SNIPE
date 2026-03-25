import streamlit as st
import numpy as np
from scipy.stats import poisson

# Configuration
st.set_page_config(page_title="AI ULTRA-SNIPER v25.0", layout="wide")

# CSS لإعطاء مظهر احترافي جداً
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e6edf3; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(45deg, #238636, #2ea043); color: white; font-weight: bold; border: none; padding: 10px; }
    .gold-box { background: linear-gradient(145deg, #1f242c, #161b22); border: 2px solid #f1c40f; padding: 25px; border-radius: 15px; text-align: center; }
    .status-win { color: #2ecc71; font-weight: bold; }
    .status-risk { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 AI ULTRA-SNIPER PRO v25.0")
st.subheader("Système d'Analyse Prédictive de Haute Précision")

with st.sidebar:
    st.header("⚙️ Configuration")
    with st.expander("🏠 DOMICILE", expanded=True):
        h_name = st.text_input("Nom", "Équipe A")
        h_att = st.number_input("Attaque (Buts marqués)", value=1.5, step=0.1)
        h_def = st.number_input("Défense (Buts encaissés)", value=1.0, step=0.1)
    
    with st.expander("🚀 EXTÉRIEUR", expanded=True):
        a_name = st.text_input("Nom ", "Équipe B")
        a_att = st.number_input("Attaque (Buts marqués) ", value=1.2, step=0.1)
        a_def = st.number_input("Défense (Buts encaissés) ", value=1.8, step=0.1)

# --- محرك الحسابات المطور ---
exp_h = (h_att + a_def) / 2
exp_a = (a_att + h_def) / 2

h_probs = [poisson.pmf(i, exp_h) for i in range(6)]
a_probs = [poisson.pmf(i, exp_a) for i in range(6)]
matrix = np.outer(h_probs, a_probs)

win_h = np.sum(np.tril(matrix, -1)) * 100
draw = np.sum(np.diag(matrix)) * 100
win_a = np.sum(np.triu(matrix, 1)) * 100

over_2_5 = (1 - np.sum([matrix[i,j] for i in range(3) for j in range(3-i)])) * 100
btts = (1 - (h_probs[0] + a_probs[0] - (h_probs[0] * a_probs[0]))) * 100

if st.button("⚡ ANALYSE SNIPER"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🏟️ {h_name} vs {a_name}")
        st.write(f"📊 **Probabilités 1X2:**")
        st.write(f"🏠 Victoire: {win_h:.1f}% | 🤝 Nul: {draw:.1f}% | 🚀 Défaite: {win_a:.1f}%")
        
    with col2:
        st.markdown("### ⚽ Marché des Buts")
        st.write(f"🔥 **Over 2.5:** {over_2_5:.1f}%")
        st.write(f"📧 **BTTS (Les deux marquent):** {btts:.1f}%")

    st.markdown("---")
    
    # --- منطق النصيحة الموثوقة الواحدة (The Sniper Choice) ---
    st.markdown("<div class='gold-box'>", unsafe_allow_html=True)
    st.markdown("### 💎 CONSEIL UNIQUE DE L'ALGORITHME")
    
    prediction = ""
    confidence = 0
    
    # منطق الفوز المباشر (القوي)
    if win_h > win_a + 25:
        prediction = f"VICTOIRE DIRECTE : {h_name}"
        confidence = win_h
    elif win_a > win_h + 25:
        prediction = f"VICTOIRE DIRECTE : {a_name}"
        confidence = win_a
    # منطق الأهداف (إذا كانت المباراة مفتوحة)
    elif over_2_5 > 58:
        prediction = "PLUS DE 2.5 GOALS (OVER)"
        confidence = over_2_5
    # منطق الـ BTTS
    elif btts > 65:
        prediction = "LES DEUX ÉQUIPES MARQUENT (BTTS)"
        confidence = btts
    # الخيار الأخير (فرصة مزدوجة)
    else:
        if win_h > win_a:
            prediction = f"DOUBLE CHANCE : 1X ({h_name})"
            confidence = win_h + draw
        else:
            prediction = f"DOUBLE CHANCE : X2 ({a_name})"
            confidence = win_a + draw

    st.markdown(f"<h2 style='color:#f1c40f;'>{prediction}</h2>", unsafe_allow_html=True)
    st.markdown(f"**Indice de Précision : {confidence:.1f}%**", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 ABDEALI NIFALI - Predict Nifali | Version 25.0 Aggressive Sniper")
