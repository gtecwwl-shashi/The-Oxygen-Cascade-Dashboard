import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade Tutor", layout="wide")

# Custom Styling for a Clinical Dashboard
st.markdown("""
    <style>
    .stNumberInput { border: 2px solid #2c3e50; border-radius: 5px; }
    .main { background-color: #fcfcfc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🫁 Interactive Oxygen Cascade Challenge")
st.write("Sea Level ($P_B$ 101.3 kPa) | $F_iO_2$ 21% | Normal Metabolism")

# --- 1. Define the Physiological Truth ---
# Based on your provided Stockport NHS and Textbook diagrams
truth_data = [
    {"stage": "Dry Air", "pao2": 21.2, "label": "Initial FiO2"},
    {"stage": "Trachea", "pao2": 19.8, "label": "Humidification (-6.3 kPa H2O)"},
    {"stage": "Alveoli", "pao2": 14.0, "label": "Alveolar Gas Equation"},
    {"stage": "Artery", "pao2": 13.0, "label": "Physiological Shunt"},
    {"stage": "Capillary", "pao2": 7.0, "label": "Tissue Diffusion"},
    {"stage": "Vein", "pao2": 5.3, "label": "Mixed Venous O2"},
    {"stage": "Mitochondria", "pao2": 1.2, "label": "Cellular Respiration"}
]

stages = [d["stage"] for d in truth_data]
correct_vals = [d["pao2"] for d in truth_data]

# --- 2. Student Input Section ---
st.subheader("Step 1: Predict the $P_{O_2}$ at each level (kPa)")
cols = st.columns(len(stages))
user_guesses = []

for i, stage in enumerate(stages):
    with cols[i]:
        guess = st.number_input(f"{stage}", min_value=0.0, max_value=22.0, value=0.0, step=0.1, key=f"input_{i}")
        user_guesses.append(guess)

# --- 3. Reveal and Visualize ---
if st.button("🚀 Submit & Reveal Physiological Reality"):
    
    fig = go.Figure()

    # User's Prediction (Dashed Line)
    fig.add_trace(go.Scatter(
        x=stages, y=user_guesses,
        mode='lines+markers',
        name='Your Prediction',
        line=dict(color='gray', dash='dot', shape='hv'),
        marker=dict(size=8, symbol='x')
    ))

    # Physiological Reality (Solid Staircase Line)
    fig.add_trace(go.Scatter(
        x=stages, y=correct_vals,
        mode='lines+markers+text',
        name='Physiological Reality',
        text=[f"{v} kPa" for v in correct_vals],
        textposition="top right",
        line=dict(color='#004a99', width=6, shape='hv'), # 'hv' creates the staircase effect
        marker=dict(size=12, symbol='square')
    ))

    # Add annotations for the 'Drops' (Matching your diagrams)
    for i in range(len(truth_data)):
        fig.add_annotation(
            x=stages[i], y=correct_vals[i],
            text=truth_data[i]["label"],
            showarrow=True, arrowhead=2, ay=-40, ax=20,
            font=dict(size=10, color="#d9534f")
        )

    fig.update_layout(
        title="<b>Oxygen Cascade: Partial Pressure of O2 (kPa)</b>",
        yaxis_title="PO2 (kPa)",
        template="plotly_white",
        yaxis=dict(range=[0, 25], gridcolor='#eee'),
        height=600,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- 4. Scoring & Feedback ---
    # Calculate score based on 1.0 kPa tolerance
    score = sum(1 for u, t in zip(user_guesses, correct_vals) if abs(u - t) < 1.0)
    
    if score == len(stages):
        st.balloons()
        st.success(f"Perfect! Score: {score}/{len(stages)}. You have mastered the cascade.")
    else:
        st.info(f"You identified {score} out of {len(stages)} levels accurately. Review the red labels to see why the pressure drops at each stage.")

st.markdown("---")
st.caption("Developed for Medical Education | Based on the Infection Sciences & NHS Foundation Trust Models")
