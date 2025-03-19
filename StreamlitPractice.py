import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Luis Torroba ")

def load_data():
    df = pd.read_csv("airbnb.csv")  # Ensure this file is in the same directory as the script
    df = df.rename(columns={"room_type": "listing_type", "neighbourhood": "neighborhood"})
    df.dropna(subset=["price"], inplace=True)  # Remove rows without price
    return df

df = load_data()

st.sidebar.header("Filters")
listing_types = st.sidebar.multiselect("Select listing types", df["listing_type"].unique(), default=df["listing_type"].unique())
neighborhoods = st.sidebar.multiselect("Select neighborhoods", df["neighborhood"].unique(), default=df["neighborhood"].unique())

filtered_df = df[(df["listing_type"].isin(listing_types)) & (df["neighborhood"].isin(neighborhoods))]

tab1, tab2 = st.tabs(["Analysis", "Simulator"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.box(filtered_df, x="listing_type", y="minimum_nights", title="Minimum nights by listing type", color_discrete_sequence=["#3498DB"])
        st.plotly_chart(fig1)
    with col2:
        fig2 = px.box(filtered_df, x="listing_type", y="price", title="Price by listing type", color_discrete_sequence=["#3498DB"])
        st.plotly_chart(fig2)
    
    top_reviews = filtered_df.groupby(["neighborhood", "listing_type"]).agg({"reviews_per_month": "sum"}).reset_index()
    fig3 = px.bar(top_reviews, x="neighborhood", y="reviews_per_month", color="listing_type", title="Most reviewed apartments per month by neighborhood", color_discrete_map={listing_type: "#3498DB" for listing_type in listing_types})
    st.plotly_chart(fig3)
    
    fig4 = px.box(filtered_df, x="listing_type", y="reviews_per_month", title="Reviews per Month by Listing Type", color_discrete_sequence=["#3498DB"])
    st.plotly_chart(fig4)

    fig5 = px.histogram(filtered_df, x="price", title="Price Distribution", color_discrete_sequence=["#1ABC9C"])
    st.plotly_chart(fig5)
    
    fig6 = px.scatter(filtered_df, x="price", y="reviews_per_month", color="listing_type", title="Price vs Reviews per Month", color_discrete_sequence=["#F39C12"])
    st.plotly_chart(fig6)
    
    fig7 = px.histogram(filtered_df, x="minimum_nights", title="Minimum Nights Distribution", color_discrete_sequence=["#E74C3C"])
    st.plotly_chart(fig7)
    
    fig8 = px.scatter(filtered_df, x="reviews_per_month", y="minimum_nights", color="neighborhood", title="Reviews per Month vs Minimum Nights", color_discrete_sequence=["#9B59B6"])
    st.plotly_chart(fig8)

with tab2:
    st.header("Price Simulator")
    selected_neighborhood = st.selectbox("Select a neighborhood", df["neighborhood"].unique())
    selected_type = st.selectbox("Select listing type", df["listing_type"].unique())
    num_nights = st.slider("Number of nights", 1, 30, 2)
    
    similar_listings = df[(df["neighborhood"] == selected_neighborhood) & (df["listing_type"] == selected_type) & (df["minimum_nights"] >= num_nights)]
    price_range = (similar_listings["price"].quantile(0.25), similar_listings["price"].quantile(0.75))
    st.write(f"Recommended price range: ${price_range[0]:.2f} - ${price_range[1]:.2f}")

st.sidebar.markdown("## Instructions")
st.sidebar.info("Upload this code to Streamlit Cloud and submit the link on Moodle.")
