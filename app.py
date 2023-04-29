import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import ast
import plotly.express as px


file = "/Users/julianballetshofer/Desktop/Makeathon/Team_Oek/bayern-roof-info-scored.csv"

def app():
    st.set_page_config(layout="wide")
    # Create the sidebar
    st.sidebar.subheader("Settings")
    user_type = ["Single", "Global"]
    plot_type = st.sidebar.selectbox(
            "Select User Type",
            user_type,
        )

    if plot_type == "Single":
        show_single_info()
    elif plot_type == "Global":
        show_global_info()

def filter_data(df, num_houses, value):
    df.sort_values(by=value, ascending=False)
    return df.head(num_houses)

def search_location(lat, long):

    return 0

def create_cum_sum(df, col = 'radiantion'):
    # Calculate the cumulative sum of energy consumption for each house
    # Generate some sample data
    data = np.random.randint(1, 10, 10) #df[col].to_numpy()

    # Calculate the cumulative sum
    cumulative_sum = np.cumsum(data)

    # Plot the cumulative sum using Streamlit
    st.line_chart(cumulative_sum)

def compute_total_energy(df, col='roof_annual_radiance'):

    sum_energy = df[col].sum()

    return sum_energy

def get_max_houses(df):
    return df.shape[0]

def get_num_to_reach(df, threshold, col='roof_annual_radiance'):

    it = 1
    sum_value = 0
    sorted = df.sort_values(by=col)

    for value in sorted[col]:
        sum_value += value
        if sum_value > threshold:
            return it
        it += 1

    return it

def compute_lat(x):
    x = ast.literal_eval(x)
    lat = x[0] + x[2] + x[4] + x[6]
    lat = lat/4
    return lat

def compute_long(x):
    x = ast.literal_eval(x)
    long = x[1] + x[3] + x[5] + x[7]
    long = long/4
    return long

def add_column_to_df(df):
    df['latitude'] = df['mrr'].apply(lambda x: compute_lat(x))
    df['longitude'] = df['mrr'].apply(lambda x: compute_long(x))
    return df

def convert_radiation(df):
    df['roof_annual_radiance_sqm'] = df['roof_annual_radiance'].div(df['width_meters']).div(df['length_meters'])
    return df

def apply_efficiency(df):
    df['roof_annual_radiance_sqm'] = df['roof_annual_radiance_sqm'].apply(lambda x: x * 0.2)
    df['roof_annual_radiance_sqm'] = df['roof_annual_radiance_sqm'].apply(lambda x: x * 0.2)
    return df

def create_df(file):
    df_total = pd.read_csv(file)
    df_total = add_column_to_df(df_total)
    df_total = convert_radiation(df_total)
    df_total = apply_efficiency(df_total)
    return df_total

def show_global_info():
    total_energie_bavaria = 87 * 10**9 #kWh/year bavaria
    st.title("Solar Potential in Bavaria")

    # get daframe
    df_total = create_df(file)

    st.sidebar.subheader("Visualize Solar Potential in Germany")
    types = ["Heatmap", "Scatter Plot"]
    plot_type = st.sidebar.selectbox(
            "Select plot type",
            types,
        )
    
    # Create the number input box
    num_houses_selected = st.sidebar.number_input("Number of Houses to Consider", min_value=1)
    max_houses = get_max_houses(df_total)

    # Add the option to use all
    use_all = st.sidebar.checkbox("Consider All Houses", value=False)

    num_houses_selected = max_houses if use_all else num_houses_selected
    num_houses_selected = max_houses if num_houses_selected > max_houses else num_houses_selected

    num_houses = get_num_to_reach(df_total, threshold = total_energie_bavaria, col='roof_annual_radiance')
    st.markdown(f"Number of houses needed to power Germany: {num_houses} houses")

    normalizer = ["per roof", "per sqm"]
    normalize = st.sidebar.selectbox(
            "Consider Roof Area",
            normalizer,
        )
    
    if normalize == "per roof":
        value = "roof_annual_radiance"
        df = filter_data(df_total, num_houses_selected, value)

    elif normalize == "per sqm":
        value = "roof_annual_radiance_sqm"
        df = filter_data(df_total, num_houses_selected, value)  

    percentage_fosil = round(compute_total_energy(df, col=value)/total_energie_bavaria * 100)

    st.markdown(f"Selcted number of houses can cover {percentage_fosil}% of fosil energy in Germany")

    if plot_type == "Heatmap":
        m = leafmap.Map(center=[48.777500,11.43111], zoom=7, tiles="stamentoner")
        m.add_heatmap(
            df,
            latitude="latitude",
            longitude="longitude",
            value=value,
            name="Heat map",
            radius=20,
        )
        m.to_streamlit(height=700)

    else:
        st.map(df)
    
    st.subheader('Cumulative Energy Potential')

    create_cum_sum(df, col='roof_annual_radiance')
    
    st.markdown(df[value].max())


def show_single_info():
    def_pc = "10115"
    def_street = "Chausseestraße"
    def_number = "1"

    postal_code = st.sidebar.text_input("Postal Code")
    street = st.sidebar.text_input("Street")
    number = st.sidebar.text_input("Number")
    clicked2 = st.sidebar.button("Search")
    if clicked2:
        if not postal_code or not street or not number:
            st.sidebar.error("Please fill in all fields.")
        else:
            # find location
            def_pc = postal_code
            def_street = street
            def_number = number
    st.title("Solar Potential Information")
    st.markdown(f"Solar Potential at location {def_street} {def_number}, {def_pc}")

app()  




