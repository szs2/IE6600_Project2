import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# Page Configuration
st.set_page_config(page_title="Global Homelessness Dashboard", page_icon="🌍", layout="wide")

# Apply Theme Styling
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
        color: #2c2c2c;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        color: #2c2c2c;
    }
    .stHeader {
        color: #333333;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
    }
    .stButton > button {
        background-color: #333333;
        color: #ffffff;
        border: none;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Introduction with 1/8 Margin
with st.container():
    left_margin, content, right_margin = st.columns([1, 6, 1])
    with content:
        st.title("🌍 Global Homelessness Dashboard")
        st.markdown("""
        Welcome to the **Global Homelessness Dashboard**!  
        This platform provides insights into homelessness across various countries.  
        Discover trends, distributions, and geographic disparities through interactive charts and maps.
        """)

# Load Dataset Function
@st.cache_data
def load_data():
    url = "https://github.com/szs2/IE6600_Project2/blob/25645b9458f83077637edadc8048de71e6a754f3/Data/Homelessness.csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()  # Remove leading/trailing spaces
    return data

# Load the data
data = load_data()

# Ensure required columns exist
required_columns = [
    'country', 'total', 'individuals', 'family_households',
    'veterans', 'unaccompanied_youth', 'latitude', 'longitude'
]
if not all(col in data.columns for col in required_columns):
    st.error(f"Dataset must contain the following columns: {required_columns}")
    st.stop()

# Sidebar Filters
st.sidebar.title("🔍 Filter Options")
st.sidebar.markdown("Use these options to filter the data and customize visualizations.")

# Slider for Total Homeless Count Range
homeless_range = st.sidebar.slider(
    "Select Homeless Count Range:",
    int(data['total'].min()),
    int(data['total'].max()),
    (50000, 500000)
)

# Multi-select for Countries with "All" Option
all_countries = ["All"] + data['country'].unique().tolist()
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=all_countries,
    default="All"
)

# Filter the data
if "All" in selected_countries:
    filtered_data = data[data['total'].between(homeless_range[0], homeless_range[1])]
else:
    filtered_data = data[
        (data['total'].between(homeless_range[0], homeless_range[1])) &
        (data['country'].isin(selected_countries))
    ]

# Bar Chart: Total Homeless by Country with 1.5/8 Margins
with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("📊 Total Homeless by Country")
        st.markdown("""
        This bar chart shows the total number of homeless individuals in each country.  
        Use the sidebar filters to refine your analysis.
        """)
        homeless_by_country = filtered_data.groupby('country')['total'].sum().sort_values(ascending=False)
        st.bar_chart(homeless_by_country)

# Pie Chart: Homeless Composition by Country
with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("👥 Percentage of Homeless Population by Country")
        st.markdown("""
        This pie chart illustrates the percentage distribution of homelessness across different countries.  
        Hover over the chart to see precise percentages.
        """)
        country_totals = filtered_data.groupby('country')['total'].sum()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(country_totals, labels=country_totals.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Percentage of Homeless Population by Country", color='#2c2c2c')
        fig.patch.set_facecolor('#f4f4f4')  # Set background
        plt.setp(ax.texts, color="#333333")  # Set text color
        st.pyplot(fig)

# Histogram: Distribution of Homeless Counts
with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("📊 Distribution of Homeless Counts")
        st.markdown("""
        This histogram shows the distribution of total homeless counts across countries.  
        The density curve overlays the histogram to provide additional insights.
        """)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.set_theme(style="whitegrid")
        sns.histplot(filtered_data['total'], bins=10, kde=True, ax=ax, color="#333333")
        ax.set_title("Distribution of Homeless Counts", color='#2c2c2c')
        ax.set_facecolor('#f4f4f4')  # Set background for the plot
        st.pyplot(fig)

# Map: Global Homelessness with 1.5/8 Margins
with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("🗺️ Map of Global Homelessness")
        st.markdown("""
        This map visualizes the total homeless count geographically.  
        Each point represents a country, with the size of the point proportional to the homeless count.  
        Hover over a point to see detailed values.
        """)
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",  # Light-themed map
            initial_view_state=pdk.ViewState(
                latitude=0,
                longitude=0,
                zoom=1.5,
                pitch=50,
            ),
            tooltip={"html": "<b>Country:</b> {country}<br><b>Homeless Count:</b> {total}"},
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_data,
                    get_position=["longitude", "latitude"],
                    get_radius="total / 10000",
                    get_fill_color="[200, 100, 200, 160]",  # Pastel Pink
                    pickable=True,
                ),
            ],
        ))

# Footer with 1/8 Margins
with st.container():
    left_margin, content, right_margin = st.columns([1, 6, 1])
    with content:
        st.markdown("""
        ---
        **Data Source**: [Global Homelessness Dataset](https://raw.githubusercontent.com/szs2/IE6600Project2/519d0a8d74f02d9c84f96a84cd6cd8d447ff7a08/Data/Homelessness.csv)  
        Created with ❤️ using [Streamlit](https://streamlit.io/).
        """)
