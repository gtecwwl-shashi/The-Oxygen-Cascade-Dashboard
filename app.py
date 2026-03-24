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
fio2 = st.sidebar.slider("FiO2 (%)", 21, 100, 21)
pb = st.sidebar.number_input("Barometric Pressure (kPa)", value=101.3) # Sea level
pco2 = st.sidebar.slider("PaCO2 (kPa)", 2.0, 12.0, 5.3) # Normal is 5.3

# --- Physiological Calculations ---
# 1. Dry Atmospheric Air
p_dry = (fio2 / 100) * pb

# 2. Humidified Tracheal Air (Subtract saturated water vapor pressure at 37°C)
p_tracheal = (fio2 / 100) * (pb - 6.3)

# 3. Alveolar Gas (Simplified Alveolar Gas Equation, RQ = 0.8)
p_alveolar = p_tracheal - (p_pco2 / 0.8) if 'p_pco2' not in locals() else p_tracheal - (pco2 / 0.8)

# 4. Arterial Blood (Normal A-a gradient ~1-2 kPa)
p_arterial = p_alveolar - 1.5

# 5. Capillary/Tissue level
p_capillary = 5.3

# 6. Mitochondria (The 'Pasteur Point' is approx 0.1-1 kPa)
p_mito = 1.0

# --- Data Visualization ---
stages = ["Atmosphere", "Trachea", "Alveoli", "Arteries", "Capillaries", "Mitochondria"]
pressures = [p_dry, p_tracheal, p_alveolar, p_arterial, p_capillary, p_mito]

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
    yaxis=dict(range=[0, max(pressures) + 5], gridcolor='#f0f0f0'),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# --- Teaching Breakdown ---
col1, col2 = st.columns(2)

with col1:
    st.info("### 🧬 Key Barriers")
    st.write(f"**1. Humidification:** Air is warmed and saturated in the trachea ($P_{{H_2O}} = 6.3$ kPa).")
    st.write(f"**2. Alveolar Ventilation:** $O_2$ is diluted by $CO_2$ entering the alveoli.")
    st.write(f"**3. Diffusion & Shunt:** Creates the **A-a gradient** ($P_A O_2 - P_a O_2$).")

with col2:
    st.success("### 📊 Current Values (kPa)")
    data = {"Stage": stages, "PO2 (kPa)": [round(p, 1) for p in pressures]}
    st.table(data)
