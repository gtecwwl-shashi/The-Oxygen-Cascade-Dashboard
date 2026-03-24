import streamlit as st
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Oxygen Cascade Tutor", layout="wide")

st.title("🫁 The Oxygen Cascade")
st.markdown("""
The **Oxygen Cascade** describes the step-wise decrease in the partial pressure of oxygen ($P_{O_2}$) 
as it moves from the environment to the mitochondria.
""")

# --- Sidebar Controls ---
st.sidebar.header("Clinical Inputs")
fio2_pct = st.sidebar.slider("FiO2 (%)", 21, 100, 21)
pb = st.sidebar.number_input("Barometric Pressure (kPa)", value=101.3) # Sea level
paco2 = st.sidebar.slider("PaCO2 (kPa)", 2.0, 12.0, 5.3) # Normal is 5.3
rq = 0.8 # Respiratory Quotient

# --- Physiological Calculations ---
fio2_dec = fio2_pct / 100

# 1. Dry Atmospheric Air
p_dry = fio2_dec * pb

# 2. Humidified Tracheal Air (Subtract water vapor pressure at 37°C which is 6.3 kPa)
p_tracheal = fio2_dec * (pb - 6.3)

# 3. Alveolar Gas (Alveolar Gas Equation)
p_alveolar = p_tracheal - (paco2 / rq)

# 4. Arterial Blood (Normal A-a gradient ~1-2 kPa)
p_arterial = p_alveolar - 1.5

# 5. Capillary/Tissue level (Approximate)
p_capillary = 5.3

# 6. Mitochondria (The Pasteur Point)
p_mito = 1.0

# Ensure values don't go below zero (physiologically impossible)
pressures = [max(0, p) for p in [p_dry, p_tracheal, p_alveolar, p_arterial, p_capillary, p_mito]]
stages = ["Atmosphere", "Trachea", "Alveoli", "Arteries", "Capillaries", "Mitochondria"]

# --- Data Visualization ---
fig = go.Figure()

# Add the "Staircase" Line
fig.add_trace(go.Scatter(
    x=stages, 
    y=pressures,
    mode='lines+markers+text',
    text=[f"{p:.1f}" for p in pressures],
    textposition="top center",
    line=dict(color='#e74c3c', width=5),
    marker=dict(size=12, symbol='square'),
    name="Oxygen Pressure"
))

fig.update_layout(
    title="Partial Pressure of Oxygen (kPa) through the Cascade",
    yaxis_title="PO2 (kPa)",
    xaxis_title="Physiological Compartment",
    template="plotly_white",
    yaxis=dict(range=[0, max(pressures) + 10], gridcolor='#f0f0f0'),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# --- Teaching Breakdown ---
col1, col2 = st.columns(2)

with col1:
    st.info("### 🧬 Key Barriers")
    st.write(f"**1. Humidification:** Air is saturated in the trachea ($P_{{H_2O}} = 6.3$ kPa).")
    st.write(f"**2. Alveolar Ventilation:** $O_2$ is diluted by $CO_2$ entering the alveoli.")
    st.write(f"**3. Diffusion & Shunt:** Creates the **A-a gradient**.")

with col2:
    st.success("### 📊 Current Values (kPa)")
    data = {"Stage": stages, "PO2 (kPa)": [round(p, 1) for p in pressures]}
    st.table(data)
