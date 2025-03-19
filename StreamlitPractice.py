import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the dashboard
st.title("Luis Torroba Airbnb Dashboard")

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv(r"C:\Users\Luis Torroba\Desktop\airbnb.csv")  # Replace with your dataset file
    data['accommodates'] = pd.to_numeric(data['accommodates'], errors='coerce')  # Ensure accommodates is numeric
    data['price'] = pd.to_numeric(data['price'], errors='coerce')  # Ensure price is numeric
    return data.dropna(subset=['accommodates', 'price'])  # Drop missing values

data = load_data()

# Sidebar for filters
st.sidebar.header("Filters")
neighborhood_filter = st.sidebar.multiselect("Select Neighbourhood", data['neighbourhood'].unique())
listing_type_filter = st.sidebar.multiselect("Select Listing Type", data['room_type'].unique())
min_price, max_price = st.sidebar.slider(
    "Select Price Range", 
    float(data['price'].min()), float(data['price'].max()), 
    (float(data['price'].min()), float(data['price'].max()))
)

# Apply filters correctly
filtered_data = data[
    ((data['neighbourhood'].isin(neighborhood_filter)) if neighborhood_filter else True) &
    ((data['room_type'].isin(listing_type_filter)) if listing_type_filter else True) &
    (data['price'] >= min_price) & 
    (data['price'] <= max_price)
]

# Display filtered data
st.write("Filtered Data:")
st.dataframe(filtered_data)

# Create two tabs
tab1, tab2 = st.tabs(["Graphs", "Simulator"])

# Tab 1: Graphs
with tab1:
    st.header("Data Visualization")

    # Graph 1: Relationship between listing type and number of people
    st.subheader("Listing Type vs Number of People")
    if not filtered_data.empty:
        fig1, ax1 = plt.subplots()
        sns.barplot(x='room_type', y='accommodates', data=filtered_data, ax=ax1)
        ax1.set_xlabel("Listing Type")
        ax1.set_ylabel("Number of People")
        st.pyplot(fig1)
    else:
        st.warning("No data available for the selected filters.")

    # Graph 2: Price by listing type
    st.subheader("Price by Listing Type")
    if not filtered_data.empty:
        fig2, ax2 = plt.subplots()
        sns.boxplot(x='room_type', y='price', data=filtered_data, ax=ax2)
        ax2.set_xlabel("Listing Type")
        ax2.set_ylabel("Price")
        st.pyplot(fig2)
    else:
        st.warning("No data available for the selected filters.")

    # Graph 3: Apartments with the highest number of reviews per month by neighborhood
    st.subheader("Top Apartments by Reviews per Month")
    if 'reviews_per_month' in filtered_data.columns and not filtered_data.empty:
        top_reviews = filtered_data.nlargest(10, 'reviews_per_month')
        fig3, ax3 = plt.subplots()
        sns.barplot(x='reviews_per_month', y='neighbourhood', data=top_reviews, ax=ax3)
        ax3.set_xlabel("Reviews per Month")
        ax3.set_ylabel("Neighbourhood")
        st.pyplot(fig3)
    else:
        st.warning("No data available for the selected filters.")
