import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade Master Quiz", layout="wide")

st.title("🎯 The Oxygen Cascade Master Challenge")
st.write("Scenario: Sea Level ($P_B$ 101.3 kPa) | $F_iO_2$ 21%")

# --- 1. The Physiological Database ---
truth = [
    {"label": "Dry Air", "val": 21.2, "desc": "Atmospheric Oxygen"},
    {"label": "Trachea", "val": 19.8, "desc": "Humidification Drop"},
    {"label": "Alveoli", "val": 14.0, "desc": "Alveolar Gas Equation Drop"},
    {"label": "Artery", "val": 13.0, "desc": "Physiological Shunt Drop"},
    {"label": "Capillary", "val": 7.0, "desc": "Tissue Extraction Drop"},
    {"label": "Vein", "val": 5.3, "desc": "Mixed Venous Return"},
    {"label": "Mitochondria", "val": 1.2, "desc": "Cellular Respiration (The 'End')"}
]

# --- 2. Quiz Interface ---
st.subheader("Step 1: Identify the Locations & Predict Values")
st.info("Fill in the labels and the partial pressures (kPa) for the cascade below.")

user_labels = []
user_values = []

# Create a grid for inputs
for i in range(len(truth)):
    c1, c2 = st.columns([2, 1])
    with c1:
        u_label = st.selectbox(f"Level {i+1} Identification", 
                              options=["---", "Alveoli", "Artery", "Atmosphere/Dry Air", "Capillary", "Mitochondria", "Trachea", "Vein"],
                              key=f"label_{i}")
        user_labels.append(u_label)
    with c2:
        u_val = st.number_input(f"PO2 (kPa) for Level {i+1}", min_value=0.0, max_value=25.0, value=0.0, step=0.1, key=f"val_{i}")
        user_values.append(u_val)

# --- 3. Evaluation Logic ---
if st.button("Submit and Compare with Physiology"):
    
    # Check Accuracy
    label_score = 0
    value_score = 0
    
    # We map the sorted true labels to compare
    true_labels = [t["label"] for t in truth]
    true_vals = [t["val"] for t in truth]

    # Visualization
    fig = go.Figure()

    # User's Staircase
    fig.add_trace(go.Scatter(
        x=list(range(len(truth))),
        y=user_values,
        mode='lines+markers',
        name='Your Prediction',
        line=dict(color='#95a5a6', dash='dot', shape='hv'),
        marker=dict(size=10)
    ))

    # Actual Physiological Staircase
    fig.add_trace(go.Scatter(
        x=list(range(len(truth))),
        y=true_vals,
        mode='lines+markers+text',
        name='Physiological Reality',
        text=[f"{v} kPa" for v in true_vals],
        textposition="top center",
        line=dict(color='#e74c3c', width=6, shape='hv'),
        marker=dict(size=12, symbol='square')
    ))

    fig.update_layout(
        title="<b>Oxygen Cascade: Predicted vs. Actual</b>",
        xaxis=dict(tickmode='array', tickvals=list(range(len(truth))), ticktext=true_labels),
        yaxis_title="PO2 (kPa)",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display Results Table
    st.subheader("Detailed Feedback")
    for i in range(len(truth)):
        # Check label (simple string match, ignoring 'Atmosphere/Dry Air' quirk)
        is_label_correct = user_labels[i] in true_labels[i] or (user_labels[i] == "Atmosphere/Dry Air" and true_labels[i] == "Dry Air")
        # Check value (within 0.5 kPa tolerance)
        is_val_correct = abs(user_values[i] - true_vals[i]) <= 0.5
        
        col_a, col_b, col_c = st.columns(3)
        col_a.write(f"**Step {i+1}:** {true_labels[i]}")
        col_b.write(f"Label: {'✅' if is_label_correct else '❌'}")
        col_c.write(f"Value: {'✅' if is_val_correct else '❌'} (Target: {true_vals[i]} kPa)")

    if all(abs(user_values[i] - true_vals[i]) <= 0.5 for i in range(len(truth))):
        st.balloons()
        st.success("You have a perfect understanding of the Oxygen Cascade!")
