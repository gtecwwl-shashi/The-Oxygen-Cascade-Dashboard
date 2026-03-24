import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade: Blackout Challenge", layout="wide")

st.title("🫁 Oxygen Cascade: The Blackout Challenge")
st.markdown("""
**Zero Clues Mode:** 1. Identify the level and predict the $P_{O_2}$ (kPa).
2. Click **'Submit'**.
3. Only the points you got **exactly right** (within 0.5 kPa) will appear. The rest remains a mystery.
""")

# --- 1. Physiological Truth ---
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

# --- 2. Input Section ---
user_labels = []
user_values = []

st.subheader("Enter your predictions:")
for i in range(len(truth)):
    cols = st.columns([2, 1])
    with cols[0]:
        u_label = st.selectbox(f"Step {i+1} Identification", 
                              options=["[Select Level]", "Alveoli", "Artery", "Dry Air", "Capillary", "Mitochondria", "Trachea", "Vein"],
                              key=f"l_{i}")
        user_labels.append(u_label)
    with cols[1]:
        u_val = st.number_input(f"Predict PO2 (kPa)", min_value=0.0, max_value=25.0, value=0.0, step=0.1, key=f"v_{i}")
        user_values.append(u_val)

# --- 3. Comparison Logic ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Submit & Reveal Hits"):
    st.session_state.submitted = True

# We only populate the 'Revealed' list with values that meet the strict 0.5 criteria
revealed_vals = []
for i in range(len(truth)):
    is_accurate = (abs(user_values[i] - true_vals[i]) <= 0.5) and (user_labels[i] == true_labels[i])
    revealed_vals.append(true_vals[i] if is_accurate else None)

# --- 4. Plotting ---
fig = go.Figure()

# Plot User's Guess Line (Gray and dashed)
fig.add_trace(go.Scatter(
    x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)],
    y=user_values,
    mode='lines+markers',
    name='Your Attempt',
    line=dict(color='#bdc3c7', dash='dot', shape='hv'),
    marker=dict(size=8, symbol='x')
))

# Plot ONLY the accurate hits (No connecting lines, just the points)
if st.session_state.submitted:
    fig.add_trace(go.Scatter(
        x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)],
        y=revealed_vals,
        mode='markers+text',
        name='Correct Points',
        text=[f"{v} kPa" if v is not None else "" for v in revealed_vals],
        textposition="top center",
        marker=dict(size=18, color='#27ae60', symbol='diamond-tall'),
    ))

fig.update_layout
