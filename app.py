import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade Quiz", layout="wide")

st.title("🎯 Challenge: Predict the Oxygen Cascade")
st.markdown("Test your knowledge of the partial pressure of oxygen ($P_{O_2}$) at sea level ($F_iO_2$ 21%).")

# --- Hidden Physiological Truths ---
pb = 101.3
fio2 = 0.21
rq = 0.8
paco2 = 5.3

# Calculated correct values
true_vals = {
    "Atmosphere": round(fio2 * pb, 1),
    "Trachea": round(fio2 * (pb - 6.3), 1),
    "Alveoli": round((fio2 * (pb - 6.3)) - (paco2 / rq), 1),
    "Arteries": round(((fio2 * (pb - 6.3)) - (paco2 / rq)) - 1.5, 1),
    "Mitochondria": 1.0
}

# --- Student Input Section ---
st.subheader("Enter your predictions (in kPa):")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    g_atm = st.number_input("Atmosphere", value=0.0, step=0.1)
with col2:
    g_trach = st.number_input("Trachea", value=0.0, step=0.1)
with col3:
    g_alv = st.number_input("Alveoli", value=0.0, step=0.1)
with col4:
    g_art = st.number_input("Arteries", value=0.0, step=0.1)
with col5:
    g_mito = st.number_input("Mitochondria", value=0.0, step=0.1)

user_guesses = [g_atm, g_trach, g_alv, g_art, g_mito]
stages = ["Atmosphere", "Trachea", "Alveoli", "Arteries", "Mitochondria"]
correct_list = [true_vals[s] for s in stages]

# --- Reveal Results ---
if st.button("Check My Answers"):
    fig = go.Figure()

    # User's Guess Line
    fig.add_trace(go.Scatter(
        x=stages, y=user_guesses, name="Your Prediction",
        line=dict(color='gray', dash='dash'), marker=dict(size=10)
    ))

    # Actual Physiological Line
    fig.add_trace(go.Scatter(
        x=stages, y=correct_list, name="Physiological Reality",
        line=dict(color='#e74c3c', width=4), marker=dict(size=12)
    ))

    fig.update_layout(title="Your Prediction vs. Reality", yaxis_title="PO2 (kPa)", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # Score feedback
    score = 0
    for g, c in zip(user_guesses, correct_list):
        if abs(g - c) < 1.0: # 1 kPa tolerance
            score += 1
    
    if score == 5:
        st.balloons()
        st.success(f"Perfect! Score: {score}/5. You're a physiology pro!")
    else:
        st.info(f"You got {score}/5 steps within 1 kPa of the correct value. Look at the red line to see the gaps!")

st.sidebar.markdown("""
### 🧠 Cheat Sheet (Don't look yet!)
1. **Atmosphere:** $0.21 \\times P_B$
2. **Trachea:** $0.21 \\times (P_B - 6.3)$
3. **Alveoli:** Uses Alveolar Gas Equation
4. **Arteries:** Alveolar $O_2$ minus A-a gradient
""")
