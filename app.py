import streamlit as st
import numpy as np
from scipy.stats import poisson

# Configuration
st.set_page_config(page_title="AI ULTRA-SNIPER v26.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b1117; color: #e6edf3; }
    .gold-box { background: linear-gradient(135deg, #1c2128, #2d333b); border: 2px solid #f1c40f; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px; }
    .yes-tag { color: #2ecc71; font-weight: bold; border: 1px solid #2ecc71; padding: 2px 8px; border-radius: 5px; margin-right: 5px; }
    .no-tag { color: #e74c3c; font-weight: bold; border: 1px solid #e74c3c; padding: 2px 8px; border-radius: 5px; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 AI ULTRA-SNIPER PRO v26.0")

with st.sidebar:
    st.header("📋 Input Data")
    h_name = st.text_input("🏠 Domicile", "Équipe A")
    h_att = st.number_input("Attaque A", value=1.5, step=0.1)
    h_def = st.number_input("Défense A", value=1.2, step=0.1)
    st.markdown("---")
    a_name = st.text_input("🚀 Extérieur", "Équipe B")
    a_att = st.number_input("Attaque B", value=1.3, step=0.1)
    a_def = st.number_input("Défense B", value=1.7, step=0.1)

# الحسابات
exp_h = (h_att + a_def) / 2
exp_a = (a_att + h_def) / 2

h_probs = [poisson.pmf(i, exp_h) for i in range(7)]
a_probs = [poisson.pmf(i, exp_a) for i in range(7)]
matrix = np.outer(h_probs, a_probs)

win_h = np.sum(np.tril(matrix, -1)) * 100
draw = np.sum(np.diag(matrix)) * 100
win_a = np.sum(np.triu(matrix, 1)) * 100
over_2_5 = (1 - np.sum([matrix[i,j] for i in range(3) for j in range(3-i)])) * 100
btts = (1 - (h_probs[0] + a_probs[0] - (h_probs[0] * a_probs[0]))) * 100

if st.button("🚀 LANCER L'ANALYSE"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Probabilités 1X2")
        st.write(f"🏠 {h_name}: {win_h:.1f}%")
        st.write(f"🤝 Nul: {draw:.1f}%")
        st.write(f"🚀 {a_name}: {win_a:.1f}%")

        st.subheader("🔮 Scores Corrects Top 2")
        scores = sorted([(i, j, matrix[i,j]) for i in range(4) for j in range(4)], key=lambda x: x[2], reverse=True)
        for s in scores[:2]:
            st.info(f"Score: {s[0]} - {s[1]} ({s[2]*100:.1f}%)")

    with col2:
        st.subheader("⚽ Marché des Buts")
        # Over 2.5
        tag_25 = "<span class='yes-tag'>OUI</span>" if over_2_5 > 50 else "<span class='no-tag'>NON</span>"
        st.markdown(f"{tag_25} **Plus de 2.5 Goals:** {over_2_5:.1f}%", unsafe_allow_html=True)
        
        # BTTS
        tag_btts = "<span class='yes-tag'>OUI</span>" if btts > 52 else "<span class='no-tag'>NON</span>"
        st.markdown(f"{tag_btts} **BTTS:** {btts:.1f}%", unsafe_allow_html=True)

    # --- منطق النصيحة الموحدة الجريئة ---
    st.markdown("<div class='gold-box'>", unsafe_allow_html=True)
    st.markdown("### 💎 CONSEIL UNIQUE DE L'ALGORITHME")
    
    # تحسين المنطق لاختيار الفوز المباشر أو الأهداف بدلاً من DC دائماً
    if win_h > 50:
        res = f"VICTOIRE DIRECTE : {h_name.upper()}"
        conf = win_h
    elif win_a > 50:
        res = f"VICTOIRE DIRECTE : {a_name.upper()}"
        conf = win_a
    elif over_2_5 > 55:
        res = "PLUS DE 2.5 GOALS (OVER)"
        conf = over_2_5
    elif btts > 60:
        res = "LES DEUX ÉQUIPES MARQUENT (BTTS)"
        conf = btts
    else:
        # إذا كانت المباراة مغلقة جداً نلجأ للفرصة المزدوجة كخيار أخير
        if win_h >= win_a:
            res = f"DOUBLE CHANCE : 1X ({h_name})"
            conf = win_h + draw
        else:
            res = f"DOUBLE CHANCE : X2 ({a_name})"
            conf = win_a + draw

    st.markdown(f"<h2 style='color:#f1c40f;'>{res}</h2>", unsafe_allow_html=True)
    st.write(f"**Indice de Précision : {conf:.1f}%**")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 ABDEALI NIFALI | Predict Nifali v26.0")
