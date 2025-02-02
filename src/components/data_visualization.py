
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function for Total Land Area vs Plantation Area
def plot_total_land_vs_plantation_area(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=["Total Land Area", "Plantation Area"], 
                y=[df_filtered["total_land_area_acre"].sum(), df_filtered["area_f4f_acre"].sum()], 
                palette="Blues", ax=ax)
    ax.set_ylabel("Total Acres")
    st.pyplot(fig)


# Function for Water Availability Distribution Pie Chart
def plot_water_and_electricity_availability(df_filtered):
    # Ensure the values are only "Yes" and "No"
    water_counts = df_filtered["water_available"].value_counts().reindex(["Yes", "No"], fill_value=0)
    electricity_counts = df_filtered["electricity_available"].value_counts().reindex(["Yes", "No"], fill_value=0)

    # Create the figure and axes for two pie charts in one row
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))  # Adjust figure size

    # Plot for Water Availability
    ax1.pie(water_counts, labels=water_counts.index, autopct="%1.1f%%",
            colors=["lightblue", "lightgreen"], startangle=90)
    ax1.set_title("Water Availability")
    ax1.set_ylabel("")  # Hide y-label

    # Plot for Electricity Availability
    ax2.pie(electricity_counts, labels=electricity_counts.index, autopct="%1.1f%%",
            colors=["orange", "yellow"], startangle=90)
    ax2.set_title("Electricity Availability")
    ax2.set_ylabel("")  # Hide y-label

    # Display the pie charts
    st.pyplot(fig)


def plot_plantation_trend(df_filtered):
    # Ensure the plantation date column is in datetime format
    df_filtered["plantation_date"] = pd.to_datetime(df_filtered["plantation_date"], errors="coerce")

    # Aggregate tree plantation count by date
    df_plantation_trend = df_filtered.groupby("plantation_date")["trees_planted"].sum().reset_index()

    # Plot the trend
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_plantation_trend["plantation_date"], df_plantation_trend["trees_planted"], 
            marker="o", linestyle="-", color="green", label="Trees Planted")
    
    ax.set_title("Trend of Trees Planted Over Time")
    ax.set_xlabel("Plantation Date")
    ax.set_ylabel("Total Trees Planted")
    ax.legend()
    ax.grid(True)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the plot in Streamlit
    st.pyplot(fig)




def calculate_amount_by_mode(df_filtered):
    # Group by the mode of collection and sum the amount collected
    amount_by_mode = df_filtered.groupby('mode_of_collection')['amount_collected'].sum().reset_index()

    # Sort the values in descending order for better visualization
    amount_by_mode_sorted = amount_by_mode.sort_values(by='amount_collected', ascending=False)

    # Plot the result
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='mode_of_collection', y='amount_collected', data=amount_by_mode_sorted, palette="viridis", ax=ax)
    ax.set_title("Amount Collected by Each Mode")
    ax.set_ylabel("Amount Collected")
    ax.set_xlabel("Mode of Collection")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    return amount_by_mode_sorted  # Optional: return the dataframe if needed




def plot_top_5_tree_species(df_filtered):
    species_cols =  [
        "mango_native", "mango_grafted_kesar", "lemon_sai_sharbati", "sitaphal_native", 
        "sitaphal_golden", "sitaphal _balanagar", "awala", "awala_grafted", "peru", 
        "peru_sardar", "chincha", "chincha_grafted", "Jamun", "Jamun_bhardoli", 
        "chikku", "orange", "mosambi", "dalimb", "ramphal", "drumstick_Koimb", 
        "bamboo", "karwand", "arjun", "katesawar", "karanj", "kaduneem", "kanchan", 
        "kadamb", "bhendi", "shirish", "ain", "pimpal", "vad", "tamhan", "waval", 
        "palas", "babhul", "bakul"
    ]
    df_species_counts = df_filtered[species_cols].sum().sort_values(ascending=False).head(5)

    # Plot bar chart
    fig, ax2 = plt.subplots(figsize=(10, 5))
    bars = df_species_counts.plot(kind="bar", color=["orange", "yellow", "green", "brown", "red"], ax=ax2)
    ax2.set_ylabel("Number of Trees Planted")
    plt.xticks(rotation=45)

    # Add values above bars
    for bar in bars.patches:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height + 0.5,  # Positioning above the bar
                 f'{height}', ha='center', va='bottom', fontsize=10, color='black')

    st.pyplot(fig)



def plot_cc_training_distribution(df_filtered):
    # Count the number of "Yes" and "No" values in the cc_training_uploaded column
    cc_training_counts = df_filtered["cc_training_uploaded?"].value_counts().reindex(["Yes", "No"], fill_value=0)

    # Create a pie chart for the distribution
    fig, ax = plt.subplots(figsize=(7, 7))  # Adjust figure size
    ax.pie(cc_training_counts, labels=cc_training_counts.index, autopct="%1.1f%%",
           colors=["lightblue", "lightgreen"], startangle=90, radius=0.8)
    ax.set_title("CC Training Distribution")
    ax.set_ylabel("")  # Hide y-label

    # Display the pie chart
    st.pyplot(fig)







# Function for Displaying Data Table
def display_data_table(df_filtered):
    st.dataframe(df_filtered.head(10))
