import sys

def get_valid_float(prompt):
    """
    Helper to get a valid float input.
    Returns 0.0 if user just presses Enter.
    """
    while True:
        user_input = input(prompt)
        if user_input.strip() == "":
            return 0.0
        try:
            val = float(user_input)
            if val < 0:
                print("    -> Please enter a positive number.")
                continue
            return val
        except ValueError:
            print("    -> Invalid input. Please enter a number.")

def get_category_selection():
    """
    Displays the numbered list of categories and returns the selected range.
    """
    # Format: ID: (Name, Min_Multiplier, Max_Multiplier)
    categories = {
        1: ("Alloyed Constructional Steel", 2.0, 2.6),
        2: ("Stainless Steel", 2.5, 3.5),
        3: ("Alloyed Heat Resistant Steel", 3.0, 4.5),
        4: ("Alloyed Tool Steel", 3.5, 5.5),
        5: ("High Speed Steels (HSS)", 6.0, 9.0)
    }

    print("\n--- SELECT STEEL CATEGORY ---")
    for key, (name, min_m, max_m) in categories.items():
        print(f"  [{key}] {name} (Multiplier: {min_m}x - {max_m}x)")
    
    while True:
        try:
            choice = input("\nEnter Category Number (1-5): ")
            choice_int = int(choice)
            if choice_int in categories:
                return categories[choice_int]
            else:
                print("    -> Invalid selection. Choose 1-5.")
        except ValueError:
            print("    -> Please enter a whole number.")

def calculate_steel_price_range():
    # --- 1. MARKET PRICES (USD/kg) - Feb 2026 Estimates ---
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

    print("\n==============================================")
    print("   STEEL RETAIL PRICE RANGE ESTIMATOR")
    print("==============================================")
    
    # 1. Get Name
    steel_name = input("Enter Steel Grade Name (e.g. 1.2714): ")
    
    # 2. Get Category immediately (as requested)
    cat_name, min_mult, max_mult = get_category_selection()
    
    # 3. Get Composition
    print(f"\n--- Enter Composition for {steel_name} ---")
    print("(Press [Enter] if element is 0%)")
    
    total_alloy_cost = 0.0
    total_percent = 0.0
    
    for element, price in PRICES.items():
        pct = get_valid_float(f"  % {element}: ")
        if pct > 0:
            total_alloy_cost += (pct / 100.0) * price
            total_percent += pct

    # 4. Calculate Iron Balance
    iron_percent = 100.0 - total_percent
    
    if iron_percent < 0:
        print(f"\n[!] ERROR: Total percentage is {total_percent}%. Max is 100%.")
        return

    iron_cost = (iron_percent / 100.0) * BASE_IRON_PRICE
    
    # 5. Final Calculations
    raw_material_cost = total_alloy_cost + iron_cost
    
    # Apply Range Multipliers
    min_retail = raw_material_cost * min_mult
    max_retail = raw_material_cost * max_mult

    # 6. Output Report
    print("\n" + "="*50)
    print(f"REPORT: {steel_name.upper()}")
    print(f"Category: {cat_name}")
    print("="*50)
    
    print(f"{'Cost Component':<25} | {'Value (USD/kg)'}")
    print("-" * 50)
    print(f"{'Raw Alloys + Iron Cost':<25} | ${raw_material_cost:.2f}")
    print("-" * 50)
    print(f"Retail Multiplier Applied     | {min_mult}x  to  {max_mult}x")
    print("-" * 50)
    
    print("\n>>> ESTIMATED RETAIL PRICE RANGE <<<")
    print(f"PER KG:    ${min_retail:.2f}  -  ${max_retail:.2f}")
    print(f"PER TONNE: ${min_retail * 1000:,.0f}  -  ${max_retail * 1000:,.0f}")
    print("="*50)

if __name__ == "__main__":
    calculate_steel_price_range()
