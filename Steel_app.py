import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Steel Price Estimator", layout="centered")

# --- PRICES (USD/kg) - Feb 2026 ---
PRICES = {
    'Carbon (C)':       0.15,
    'Silicon (Si)':     1.50,
    'Manganese (Mn)':   1.40,
    'Chromium (Cr)':    3.00,
    'Nickel (Ni)':      16.80,
    'Molybdenum (Mo)':  48.00,
    'Vanadium (V)':     32.50,
    'Tungsten (W)':     42.00,
    'Cobalt (Co)':      31.00,
    'Copper (Cu)':      9.20,
    'Aluminum (Al)':    2.40,
    'Niobium (Nb)':     45.00
}
BASE_IRON_PRICE = 0.55

# --- CATEGORIES ---
CATEGORIES = {
    "1. Alloyed Constructional Steel": (2.0, 2.6),
    "2. Stainless Steel":              (2.5, 3.5),
    "3. Alloyed Heat Resistant Steel": (3.0, 4.5),
    "4. Alloyed Tool Steel":           (3.5, 5.5),
    "5. High Speed Steels (HSS)":      (6.0, 9.0)
}

# --- APP UI ---
st.title("🏭 Steel Retail Price Estimator")
st.markdown("Calculate **Raw Material Cost** and estimated **Retail Price Range**.")

# 1. Inputs
col1, col2 = st.columns([2, 2])
with col1:
    steel_name = st.text_input("Steel Grade Name", placeholder="e.g. 1.2714")
with col2:
    cat_selection = st.selectbox("Select Steel Category", options=list(CATEGORIES.keys()))

# Get multipliers based on selection
min_mult, max_mult = CATEGORIES[cat_selection]

st.divider()

# 2. Composition Inputs
st.subheader("Chemical Composition (%)")
st.caption("Enter the percentage for each element. Iron (Fe) is calculated automatically.")

# Create 3 columns for inputs to make it look like an app
c1, c2, c3 = st.columns(3)
input_cols = [c1, c2, c3]

elements_inputs = {}
i = 0
for element, price in PRICES.items():
    # Rotate through columns
    with input_cols[i % 3]:
        val = st.number_input(f"{element}", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
        elements_inputs[element] = val
    i += 1

# --- CALCULATIONS ---
total_percent = sum(elements_inputs.values())
iron_percent = 100.0 - total_percent

# Calculate Costs
total_alloy_cost = sum((pct/100) * PRICES[el] for el, pct in elements_inputs.items())

if iron_percent < 0:
    st.error(f"⚠️ Total percentage is {total_percent:.2f}%! (Must be ≤ 100)")
else:
    iron_cost = (iron_percent / 100) * BASE_IRON_PRICE
    raw_cost_kg = total_alloy_cost + iron_cost
    
    # Retail Range
    retail_min = raw_cost_kg * min_mult
    retail_max = raw_cost_kg * max_mult

    # --- DISPLAY RESULTS ---
    st.divider()
    st.header(f"Results for: {steel_name if steel_name else 'Custom Grade'}")

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Iron Balance", f"{iron_percent:.2f}%")
    m2.metric("Raw Melt Cost", f"${raw_cost_kg:.2f} /kg")
    m3.metric("Multiplier", f"{min_mult}x - {max_mult}x")

    # Big Price Display
    st.success(f"### 💰 Estimated Retail Price:  ${retail_min:.2f}  —  ${retail_max:.2f} / kg")
    st.caption(f"Per Tonne: ${retail_min*1000:,.0f} - ${retail_max*1000:,.0f}")

    # Cost Breakdown Chart
    st.subheader("Cost Drivers")
    
    # Prepare data for chart
    chart_data = {k: (v/100)*PRICES[k] for k, v in elements_inputs.items() if v > 0}
    chart_data['Iron'] = iron_cost
    
    df = pd.DataFrame(list(chart_data.items()), columns=['Element', 'Cost Contribution ($)'])
    st.bar_chart(df.set_index('Element'))

    # Detailed Table inside an expander
    with st.expander("See Detailed Cost Breakdown"):
        st.table(df)
