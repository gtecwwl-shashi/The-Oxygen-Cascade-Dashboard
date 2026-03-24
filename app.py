import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade Quiz", layout="wide")

st.title("🫁 The Oxygen Cascade: Hidden Challenge")
st.markdown("""
**Instructions:** 1. Identify the physiological level from the dropdown.
2. Enter your predicted $P_{O_2}$ in kPa.
3. Click **'Submit & Reveal Reality'** to compare your curve to the real Oxygen Cascade.
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

# Input grid
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
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Submit & Reveal Reality"):
    st.session_state.submitted = True

fig = go.Figure()

# Plot User Prediction
fig.add_trace(go.Scatter(
    x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)],
    y=user_values,
    mode='lines+markers',
    name='Your Prediction',
    line=dict(color='#34495e', dash='dot', shape='hv'),
    marker=dict(size=10, symbol='x')
))

# Plot Reality ONLY if submitted
if st.session_state.submitted:
    fig.add_trace(go.Scatter(
        x=[f"{i+1}: {l}" for i, l in enumerate(user_labels)], # Keep same X-axis for direct comparison
        y=true_vals,
        mode='lines+markers+text',
        name='Physiological Reality',
        text=[f"{v} kPa" for v in true_vals],
        textposition="top right",
        line=dict(color='#e74c3c', width=5, shape='hv'),
        marker=dict(size=12, symbol='square')
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feedback Summary
    st.subheader("Analysis")
    score = 0
    for i in range(len(truth)):
        is_correct = (user_labels[i] == true_labels[i]) and (abs(user_values[i] - true_vals[i]) <= 0.8)
        if is_correct:
            score += 1
            st.success(f"✅ Step {i+1}: {true_labels[i]} is correct at {true_vals[i]} kPa")
        else:
            st.error(f"❌ Step {i+1}: Expected {true_labels[i]} ({true_vals[i]} kPa)")
    
    st.metric("Total Score", f"{score}/7")
    if score == 7:
        st.balloons()
else:
    fig.update_layout(title="Your Predicted Cascade (Submit to reveal Truth)")
    st.plotly_chart(fig, use_container_width=True)
    st.info("The red line is hidden. Finish your predictions and click Submit!")

if st.button("Reset Quiz"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
