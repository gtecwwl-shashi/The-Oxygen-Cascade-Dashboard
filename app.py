import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade Quiz", layout="wide")

st.title("🫁 The Oxygen Cascade: Hidden Challenge")
st.markdown("""
**Instructions:** 1. Identify the physiological level from the dropdown.
2. Enter your predicted $P_{O_2}$ in kPa.
3. Click 'Submit' to reveal how your curve compares to the real Oxygen Cascade.
""")

# --- 1. Internal Data (The Truth) ---
truth = [
    {"label": "Dry Air", "val": 21.2},
    {"label": "Trachea", "val": 19.8},
    {"label": "Alveoli", "val": 14.0},
    {"label": "Artery", "val": 13.0},
    {"label": "Capillary", "val": 7.0},
    {"label": "Vein", "val": 5.3},
    {"label": "Mitochondria", "val": 1.2}
]

true_labels = [t["label"] for t in truth]
true_vals = [t["val"] for t in truth]

# --- 2. Student Input Area ---
st.subheader("Step 1: Build Your Cascade")

user_labels = []
user_values = []

# Use columns for a clean input interface
for i in range(len(truth)):
    cols = st.columns([2, 1])
    with cols[0]:
        u_label = st.selectbox(f"Level {i+1} Name", 
                              options=["[Select Level]", "Alveoli", "Artery", "Dry Air", "Capillary", "Mitochondria", "Trachea", "Vein"],
                              key=f"l_{i}")
        user_labels.append(u_label)
    with cols[1]:
        u_val = st.number_input(f"Predicted PO2 (kPa)", min_value=0.0, max_value=25.0, value=0.0, step=0.1, key=f"v_{i}")
        user_values.append(u_val)

# --- 3. Graphing & Reveal Logic ---
# We use Session State to keep the "Truth" hidden until the button is pressed
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Submit & Reveal Reality"):
    st.session_state.submitted = True

fig = go.Figure()

# ALWAYS show the User's Prediction (if they've entered data)
# We map the X-axis to their selected labels
fig.add_trace(go.Scatter(
    x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)],
    y=user_values,
    mode='lines+markers',
    name='Your Prediction',
    line=dict(color='#34495e', dash='dot', shape='hv'),
    marker=dict(size=10, symbol='x')
))

# ONLY show the Physiological Reality if the button was clicked
if st.session_state.submitted:
    fig.add_trace(go.Scatter(
        x=[f"{i+1}: {l}" for i, l in enumerate(true_labels)],
        y=true_vals,
        mode='lines+markers+text',
        name='Physiological Reality',
        text=[f"{v} kPa" for v in true_vals],
        textposition="top right",
        line=dict(color='#e74c3c', width=5, shape='hv'),
