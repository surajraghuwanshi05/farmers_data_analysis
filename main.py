import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.components.data_visualization import *
from src.components.data_transformation import *

# run pipeline to apply all the check 

df = pd.read_csv("artifacts/data.csv") # Input file
output_failed_path = "artifacts/failed_data.csv"
output_file_path = "artifacts/cleaned_data.csv"  # Output file for failed data
dq_checker = DataQuality(df,output_file_path, output_failed_path)
dq_checker.run_all_checks()



# Set page title
st.set_page_config(page_title="🌱 Field Manager Dashboard", layout="wide")

# Convert relevant columns to numeric
df["total_land_area_acre"] = pd.to_numeric(df["total_land_area_acre"], errors="coerce")
df["area_f4f_acre"] = pd.to_numeric(df["area_f4f_acre"], errors="coerce")

# Sidebar Filters
st.sidebar.header("📌 Filters")

st.sidebar.markdown(""" 
Use this dropdown to select a specific district and view its plantation data.  
- Selecting **"Total Area"** will display data for all districts combined.  
- Selecting a specific district will filter the data accordingly.
""")


df["District"] = "District " + df["District"]

# Create dropdown list with "Total Area" at the top
districts = ["Total Area"] + list(df["District"].unique())
selected_district = st.sidebar.selectbox("Select District", districts, index=0)

# Apply filter
if selected_district == "Total Area":
    df_filtered = df  # Use entire dataset
else:
    df_filtered = df[df["District"] == selected_district]

# Set plot style
sns.set_style("whitegrid")





# 📊 **1️  Bar Chart: Total Land Area vs. Plantation Area**
st.subheader(f"🏡 Total Land Area vs. Plantation Area ({selected_district})")
plot_total_land_vs_plantation_area(df_filtered)

# 💧 **2️ Pie Chart: Water and Electricity Availability Distribution**
st.subheader(f"💧 Water and Electricity Availability Distribution ({selected_district})")
plot_water_and_electricity_availability(df_filtered)


# 🌳**3  line Chart: Tree Plantation Trend Over Time*
st.subheader(f"🌱 Tree Plantation Trend Over Time ({selected_district})")
plot_plantation_trend(df_filtered)

# 🌳 **4  Stacked Bar Chart: Distribution of Top 5 Tree Species**
st.subheader(f"🌳 Distribution of Top 5 Tree Species Planted ({selected_district})")
plot_top_5_tree_species(df_filtered)

#  **5  Stacked Bar Chart: Distribution of Top 5 Tree Species**
st.subheader(f"💰 Farmers Payment Status({selected_district})")
plot_payment_distribution_bar(df_filtered)

#  **6  Stacked Bar Chart: Distribution of Top 5 Tree Species**
st.subheader(f"💰 Farmers Payment distribusion({selected_district})")
calculate_amount_by_mode(df_filtered)


# **7 Pie Chart: how many farmers took cc training 
st.subheader(f"📚 CC Training Distribution ({selected_district})")
plot_cc_training_distribution(df_filtered)



# 📋 **4️⃣ Display Data Table**
st.subheader(f"📋 Data Preview ({selected_district})")
display_data_table(df_filtered)
