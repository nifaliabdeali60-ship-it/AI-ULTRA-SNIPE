import streamlit as st
import numpy as np
from scipy.stats import poisson

# Configuration AI ULTRA-SNIPER v24.0 (Full Engine)
st.set_page_config(page_title="AI ULTRA-SNIPER v24.0", layout="wide")

st.title("🎯 AI ULTRA-SNIPER v24.0")
st.markdown("---")

# 1. إدخال البيانات - Entrée des données
with st.sidebar:
    st.header("📋 Données des Équipes")
    home_name = st.text_input("Équipe Domicile", "Home Team")
    home_scored = st.number_input(f"Buteurs {home_name} (Moyenne)", value=1.5)
    home_conceded = st.number_input(f"Encaissés {home_name} (Moyenne)", value=1.0)
    
    st.divider()
    
    away_name = st.text_input("Équipe Extérieur", "Away Team")
    away_scored = st.number_input(f"Buteurs {away_name} (Moyenne)", value=1.2)
    away_conceded = st.number_input(f"Encaissés {away_name} (Moyenne)", value=1.3)

# 2. الخوارزمية - Algorithme
# حساب الأهداف المتوقعة بناءً على القوة الهجومية والدفاعية
exp_home = (home_scored + away_conceded) / 2
exp_away = (away_scored + home_conceded) / 2

if st.button("🚀 ANALYSER LE MATCH"):
    # مصفوفة الاحتمالات (Poisson Matrix)
    h_probs = [poisson.pmf(i, exp_home) for i in range(7)]
    a_probs = [poisson.pmf(i, exp_away) for i in range(7)]
    matrix = np.outer(h_probs, a_probs)

    # حساب الاحتمالات الأساسية
    win_h = np.sum(np.tril(matrix, -1)) * 100
    draw = np.sum(np.diag(matrix)) * 100
    win_a = np.sum(np.triu(matrix, 1)) * 100

    # حساب Over/Under
    over_1_5 = (1 - (matrix[0,0] + matrix[0,1] + matrix[1,0])) * 100
    over_2_5 = (1 - np.sum([matrix[i,j] for i in range(3) for j in range(3-i)])) * 100
    
    # حساب BTTS (Yes)
    btts_yes = (1 - (h_probs[0] + a_probs[0] - (h_probs[0] * a_probs[0]))) * 100

    # العرض التنظيمي (UI Layout)
    colA, colB, colC = st.columns(3)
    
    with colA:
        st.subheader("📊 Marché 1X2")
        st.write(f"🏠 {home_name}: **{win_h:.1f}%** (Odd: {100/win_h:.2f})")
        st.write(f"🤝 Nul: **{draw:.1f}%** (Odd: {100/draw:.2f})")
        st.write(f"🚀 {away_name}: **{win_a:.1f}%** (Odd: {100/win_a:.2f})")

    with colB:
        st.subheader("⚽ Buts (Plus/Moins)")
        st.write(f"➕ 1.5 Goals: **{over_1_5:.1f}%**")
        st.write(f"➕ 2.5 Goals: **{over_2_5:.1f}%**")
        st.write(f"🔥 BTTS (Yes): **{btts_yes:.1f}%**")

    with colC:
        st.subheader("🔢 Scores Corrects")
        # البحث عن أعلى قيمتين في المصفوفة
        flat_indices = np.argsort(matrix.ravel())[-2:][::-1]
        for idx in flat_indices:
            h, a = np.unravel_index(idx, matrix.shape)
            st.write(f"📍 Score: **{h} - {a}** (Prob: {matrix[h,a]*100:.1f}%)")

    # 3. النصيحة الذهبية الموثوقة - CONSEIL UNIQUE ET RENTABLE
    st.divider()
    st.subheader("💎 CONSEIL GOLD (ULTRA-SNIPER)")
    
    # منطق اختيار أفضل رهان بناءً على أعلى نسبة نجاح
    predictions = {
        f"Victoire {home_name}": win_h,
        f"Victoire {away_name}": win_a,
        "Double Chance 1X": win_h + draw,
        "Double Chance X2": win_a + draw,
        "Plus de 1.5 Buts": over_1_5,
        "Plus de 2.5 Buts": over_2_5,
        "Both Teams to Score": btts_yes
    }
    
    best_bet = max(predictions, key=predictions.get)
    st.success(f"**LE MEILLEUR CHOIX : {best_bet}** | Fiabilité : {predictions[best_bet]:.1f}%")
    st.info("💡 Ce conseil est généré après filtrage de 49 probabilités différentes.")

st.markdown("---")
st.caption("Copyright © 2026 ABDEALI NIFALI - Predict Nifali")
