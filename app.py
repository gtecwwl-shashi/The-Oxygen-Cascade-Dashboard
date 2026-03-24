import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade Quiz", layout="wide")

st.title("🫁 The Oxygen Cascade: Strict Validation Challenge")
st.markdown("""
**The Rules:** 1. Enter your predicted $P_{O_2}$ for each level.
2. Click **'Submit'**.
3. **Only** the physiological values you guessed correctly (within **0.5 kPa**) will be revealed on the red line!
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

for i in range(len(truth)):
    cols = st.columns([2, 1])
    with cols[0]:
        u_label = st.selectbox(f"Level {i+1}", 
                              options=["[Select Level]", "Alveoli", "Artery", "Dry Air", "Capillary", "Mitochondria", "Trachea", "Vein"],
                              key=f"l_{i}")
        user_labels.append(u_label)
    with cols[1]:
        u_val = st.number_input(f"Guess PO2 (kPa)", min_value=0.0, max_value=25.0, value=0.0, step=0.1, key=f"v_{i}")
        user_values.append(u_val)

# --- 3. Comparison & Filter Logic ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Submit & Reveal Reality"):
    st.session_state.submitted = True

# Filter the "Truth" line based on accuracy
# We only keep the truth value if the user is within 0.5 kPa AND the label matches
revealed_vals = []
for i in range(len(truth)):
    is_accurate = (abs(user_values[i] - true_vals[i]) <= 0.5) and (user_labels[i] == true_labels[i])
    if is_accurate:
        revealed_vals.append(true_vals[i])
    else:
        revealed_vals.append(None) # Use None so Plotly leaves a gap or hides the point

# --- 4. Plotting ---
fig = go.Figure()

# Plot User Prediction (Always visible)
fig.add_trace(go.Scatter(
    x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)],
    y=user_values,
    mode='lines+markers',
    name='Your Guess',
    line=dict(color='#95a5a6', dash='dot', shape='hv'),
    marker=dict(size=8, symbol='x')
))

# Plot Reality (Only revealed if submitted AND accurate)
if st.session_state.submitted:
    fig.add_trace(go.Scatter(
        x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)],
        y=revealed_vals,
        mode='markers+text', # Markers only to highlight correct "hits"
        name='Correct Hits',
        text=[f"{v} kPa" if v is not None else "" for v in revealed_vals],
        textposition="top center",
        marker=dict(size=15, color='#27ae60', symbol='diamond'),
    ))
    
    # Add a phantom line for the full truth to show the gaps
    fig.add_trace(go.Scatter(
        x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)],
        y=true_vals,
        mode='lines',
        name='Full Physiological Path',
        line=dict(color='rgba(231, 76, 60, 0.2)', width=2, shape='hv'), # Light faded red
        hoverinfo='skip'
    ))

st.plotly_chart(fig, use_container_width=True)

# --- 5. Feedback ---
if st.session_state.submitted:
    score = sum(1 for v in revealed_vals if v is not None)
    st.subheader(f"Results: {score}/7 Steps Mastered")
    
    for i in range(len(truth)):
        if revealed_vals[i] is not None:
            st.success(f"✅ Step {i+1}: Perfect! {true_labels[i]} is exactly {true_vals[i]} kPa.")
        else:
            st.error(f"❌ Step {i+1}: Your guess for {true_labels[i]} was too far off to reveal.")

if st.button("Try Again"):
    st.session_state.submitted = False
    st.rerun()
