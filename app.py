import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade Interactive", layout="wide")

# Custom CSS for that clinical feel
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stNumberInput label { font-weight: bold; color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 Interactive Oxygen Cascade Tutor")
st.write("Predict the partial pressure of oxygen (PO2) at each physiological step.")

# --- Physiological Constants (The 'Truth') ---
# Based on sea level, FiO2 21%, PaCO2 5.3kPa
truth = {
    "Atmosphere": 21.2,
    "Trachea": 19.8,
    "Alveoli": 14.0,
    "Artery": 13.0,
    "Capillary": 7.0,
    "Vein": 5.3,
    "Mitochondria": 1.2
}
stages = list(truth.keys())

# --- Interactive Sidebar: Set the Scenario ---
st.sidebar.header("Scenario Settings")
mode = st.sidebar.radio("Mode", ["Learning Mode (Reveal All)", "Quiz Mode (Test Yourself)"])
st.sidebar.info("Standard conditions: Sea Level, FiO2 21%")

# --- User Input Section ---
guesses = []
st.subheader("Enter your predicted PO2 (kPa):")
cols = st.columns(len(stages))

for i, stage in enumerate(stages):
    with cols[i]:
        # If in learning mode, we pre-fill. If in quiz mode, we leave at 0.0.
        val = truth[stage] if mode == "Learning Mode (Reveal All)" else 0.0
        guess = st.number_input(f"{stage}", value=val, step=0.1, key=f"g_{stage}")
        guesses.append(guess)

# --- The Visualization Engine ---
def create_cascade_plot(user_data, actual_data, show_truth):
    fig = go.Figure()

    # User's Guess (Step plot to match your 1st image)
    fig.add_trace(go.Scatter(
        x=stages, y=user_data,
        mode='lines+markers',
        name='Your Prediction',
        line=dict(color='#34495e', width=3, shape='hv'),
        marker=dict(size=10, symbol='circle-open')
    ))

    if show_truth:
        # Actual Reality (Step plot)
        fig.add_trace(go.Scatter(
            x=stages, y=actual_data,
            mode='lines+markers+text',
            name='Physiological Reality',
            text=[f"{v} kPa" for v in actual_data],
            textposition="top right",
            line=dict(color='#e74c3c', width=5, shape='hv'),
            marker=dict(size=12)
        ))
        
        # Annotations for the drops (Matching your 1st image labels)
        annotations = [
            ("Humidification", 0.5, 20.5),
            ("Alveolar Gas Eq.", 1.5, 17.0),
            ("Shunt/Diffusion", 2.5, 13.5),
            ("Tissue Extraction", 4.5, 6.0)
        ]
        for txt, x, y in annotations:
            fig.add_annotation(x=x, y=y, text=txt, showarrow=False, font=dict(color="blue"))

    fig.update_layout(
        yaxis_title="PO2 (kPa)",
        xaxis_title="Location in the Cascade",
        template="plotly_white",
        yaxis=dict(range=[0, 25], gridcolor="#eee"),
        height=600,
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    return fig

# --- Action and Feedback ---
if mode == "Quiz Mode (Test Yourself)":
    if st.button("Submit Predictions & Check Results"):
        st.plotly_chart(create_cascade_plot(guesses, list(truth.values()), True), use_container_width=True)
        
        # Logic for feedback
        correct_count = sum(1 for g, t in zip(guesses, truth.values()) if abs(g - t) < 0.5)
        if correct_count == len(stages):
            st.balloons()
            st.success("Clinical Master! All values are accurate.")
        else:
            st.warning(f"You got {correct_count}/{len(stages)} stages correct (within 0.5 kPa). Study the red steps!")
else:
    st.plotly_chart(create_cascade_plot(guesses, list(truth.values()), True), use_container_width=True)

# --- Clinical Explainers ---
with st.expander("Why does the pressure drop? (Click to expand)"):
    st.write("""
    - **Atmosphere to Trachea:** Drop due to **Humidification** (adding water vapor).
    - **Trachea to Alveoli:** Drop due to **Alveolar Gas Equation** (CO2 displacing O2).
    - **Alveoli to Artery:** Drop due to **A-a gradient** (Physiological shunt and diffusion limit).
    - **Artery to Vein:** Drop due to **Oxygen Extraction** by tissues.
    """)
