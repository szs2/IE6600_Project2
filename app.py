import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import altair as alt
import plotly.express as px
import numpy as np

# Page Configuration
st.set_page_config(page_title="Global Homelessness Dashboard", layout="wide")

# ------------------------------------------------------------------------------------------------
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

     geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-125.0, 48.0],
                                [-125.0, 35.0],
                                [-100.0, 35.0],
                                [-100.0, 48.0],
                                [-125.0, 48.0],
                            ]
                        ],
                    },
                    "properties": {
                        "country": "United States",
                        "total": 553742,
                        "individuals": 369081,
                        "family_households": 184661,
                    },
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [10.0, 45.0],
                                [10.0, 40.0],
                                [15.0, 40.0],
                                [15.0, 45.0],
                                [10.0, 45.0],
                            ]
                        ],
                    },
                    "properties": {
                        "country": "Italy",
                        "total": 50000,
                        "individuals": 32000,
                        "family_households": 18000,
                    },
                },
            ],
        }

        # Create a Pydeck Layer for GeoJSON
        geojson_layer = pdk.Layer(
            "GeoJsonLayer",
            data=geojson_data,
            get_fill_color="[255, (properties.total / 10000) * 50, 150]",
            get_line_color=[255, 255, 255],
            pickable=True,
            stroked=True,
        )


    </style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------------------------------------------

# Title and Introduction
with st.container():
    left_margin, content, right_margin = st.columns([1, 6, 1])
    with content:
        st.title("Global Homelessness Dashboard")
        st.markdown("""
            Welcome to the **Global Homelessness Dashboard**!  
            Created by: **Senuri Kahandugoda**

            This interactive web application is designed to provide a comprehensive overview of homelessness trends and statistics across various regions worldwide. 
            By leveraging the latest data from the [Global Homelessness Dataset](https://github.com/szs2/IE6600_Project2/blob/main/Data/Homelessness.csv), 
            the dashboard empowers users to explore key insights through interactive charts and filters.

            With this tool, you can:
            - Visualize the distribution of homelessness by region and country.
            - Analyze demographic details, including individuals, families, veterans, and unaccompanied youth.
            - Compare homelessness statistics between countries and continents.
            - Gain actionable insights to support awareness and decision-making.

            The **Global Homelessness Dashboard** is designed for policymakers, researchers, and individuals interested in understanding the global challenges of homelessness.  
            Dive in, interact with the visuals, and explore the data to uncover stories behind the numbers!
            """)


# ------------------------------------------------------------------------------------------------

# Load Dataset Function
@st.cache_data
def load_data():

    url = "https://raw.githubusercontent.com/szs2/IE6600Project2/59286a675c19ad67bf0dfc1da0df756c37b1fe40/Data/Homelessness.csv"
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()  # Clean column names
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if loading fails


data = load_data()
# ------------------------------------------------------------------------------------------------

# Sidebar Filters
st.sidebar.title("🔍 Filter Options")
st.sidebar.markdown("Use these options to filter the data and customize visualizations.")

# Slider for Total Homeless Count Range
homeless_range = st.sidebar.slider(
    "Select Homeless Count Range:",
    int(data['total'].min()),
    int(data['total'].max()),
    (int(data['total'].min()), int(data['total'].max()))
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

# ------------------------------------------------------------------------------------------------

# Static data for predefined region mapping
data = pd.DataFrame({
    'country': [
        'India', 'Japan', 'United Kingdom', 'Germany',
        'Canada', 'Mexico', 'Brazil', 'South Africa', 'Australia'
    ],
    'region': [
        'Asia', 'Asia', 'Europe', 'Europe',
        'North America', 'North America', 'South America', 'Africa', 'Oceania'
    ]
})

# Treemap: Countries grouped by Regions
with st.container():
    left_margin, content, right_margin = st.columns([1, 6, 1])
    with content:
        st.header("Dividing Countries According to Regions in the World")
        st.markdown("""
                **This treemap provides a visual representation of countries grouped by their respective world regions.**  
                The hierarchical structure is defined as **Region → Country**, enabling viewers to explore how different countries are distributed across continents such as **Asia, Europe, North America, South America, Africa,** and **Oceania**.  
                Each region is represented as a parent category, with countries displayed as nested elements.  
                This chart helps in understanding the global geographic classification of countries and their association with specific regions, offering a clear and organized overview for comparative and analytical purposes.
                """)

        if data.empty:
            st.warning("No data available for the specified regions and countries.")
        else:
            # Create a Treemap using Plotly
            fig = px.treemap(
                data,
                path=['region', 'country'],  # Hierarchy: Region -> Country
                title='Dividing Countries According to Regions in the World'
            )

            st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------------------------------------------
# Bar Chart: Total Homeless by Country with 1.5/8 Margins
with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("Total Homeless by Country")
        st.markdown("""
                **This bar chart highlights the total number of homeless individuals in each country, providing a comparative view across nations.**  
                The **X-axis** represents the **countries**, while the **Y-axis** shows the **total homeless population** for each country.  
                By utilizing sidebar filters, viewers can refine the dataset to focus on specific countries or regions, facilitating detailed analysis.  
                The chart's interactive features enable easy exploration of trends and patterns, supporting informed decision-making and targeted interventions.
                """)

        # Group data and sort by total
        homeless_by_country = filtered_data.groupby('country')['total'].sum().sort_values(ascending=False).reset_index()

        # Create a bar chart using Plotly
        fig = px.bar(
            homeless_by_country,
            x='country',
            y='total',
            labels={'country': 'Country', 'total': 'Total Homeless Individuals'},
            title="Total Homeless by Country",
        )

        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="Total Homeless Individuals",
            title_x=0.5,  # Center the title
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------------------------------------------

# Pie Chart: Homeless Composition by Country
selected_countries_data = filtered_data[filtered_data['country'].isin(['United States', 'Australia', 'Japan'])]

with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("Population Percentage in Pacific Countries")
        st.markdown("""
                **This pie chart displays the percentage distribution of homelessness among selected Pacific countries:  
                United States, Australia, and Japan.**  
                Each segment represents a country, with its size proportional to the total number of homeless individuals relative to the group.  
                Hover over the chart to view precise percentages, offering a clear understanding of how homelessness is distributed across these nations.  
                The visualization provides insights into regional disparities, emphasizing the scale of homelessness in each country.
                """)

        # Filter data for specific countries
        selected_countries_data = filtered_data[filtered_data['country'].isin(['United States', 'Australia', 'Japan'])]

        # Check if there is data to display
        if selected_countries_data.empty:
            st.warning("No data available for the selected countries in the current filters.")
        else:
            # Group data and calculate percentages
            selected_totals = selected_countries_data.groupby('country')['total'].sum()
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(
                selected_totals,
                labels=selected_totals.index,
                autopct='%1.1f%%',
                startangle=90
            )
            ax.set_title("Homelessness Percentage in Selected Countries", color='#2c2c2c')
            fig.patch.set_facecolor('#f4f4f4')  # Set background
            plt.setp(ax.texts, color="#333333")  # Set text color
            st.pyplot(fig)

# ------------------------------------------------------------------------------------------------

# Histogram: Distribution of Homeless Counts
with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("Enhanced Distribution of Homeless Counts")
        st.markdown("""
        This enhanced histogram shows the distribution of total homeless counts across countries.  
        The KDE (kernel density estimation) curve overlays the histogram to provide a smooth approximation of the data's distribution.  
        Different colors distinguish the histogram bars from the KDE curve, and detailed axis labels enhance readability.
        """)

        # Clean the data to ensure no NaN or invalid values
        clean_data = filtered_data['total'].dropna()
        clean_data = clean_data[np.isfinite(clean_data)]  # Remove infinities

        if clean_data.empty:
            st.warning("No valid data available to plot the histogram.")
        else:
            # Plot configuration
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.set_theme(style="whitegrid")

            # Create the histogram with KDE
            sns.histplot(
                clean_data,
                bins=15,  # Increase bin count for more detail
                kde=True,
                ax=ax,
                color="#1f77b4",
            )

            # Customize KDE curve separately
            if len(ax.lines) > 0:  # Ensure the KDE curve exists
                ax.lines[0].set_color("#ff7f0e")  # Set KDE curve color to orange
                ax.lines[0].set_linewidth(2)  # Set KDE curve line width

            # Add titles and labels
            ax.set_title("Enhanced Distribution of Homeless Counts", fontsize=16, color="#333333", weight='bold')
            ax.set_xlabel("Total Homeless Counts", fontsize=12, color="#333333")
            ax.set_ylabel("Frequency", fontsize=12, color="#333333")

            # Add gridlines
            ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

            # Add a legend
            ax.legend(["KDE Curve", "Histogram"], loc="upper right", fontsize=10, frameon=True)

            # Adjust background for the plot
            ax.set_facecolor('#f9f9f9')
            fig.patch.set_facecolor('#f4f4f4')

            st.pyplot(fig)

# ------------------------------------------------------------------------------------------------

# Scatter Plot: Interactive Homeless Population by Geographic Location
with st.container():
    left_margin, content, right_margin = st.columns([1.5, 5, 1.5])
    with content:
        st.header("Interactive Scatter Plot: Homeless Population by Geographic Location")
        st.markdown("""
                **This scatter plot provides an interactive visualization of the geographic locations (latitude and longitude) of countries and their corresponding total homeless population.**  
                Each point on the chart represents a country, with the **size of the point indicating the scale of homelessness** and its **color reflecting population density** using a viridis color scale.  
                Users can click on a point to view detailed information about a specific country, including its **name, homeless population, latitude, and longitude**, enabling an insightful geographic analysis of homelessness trends.
                """)

        # Check if there is data to display
        if filtered_data.empty:
            st.warning("No data available for the selected filters.")
        else:
            # Create an Altair scatter plot
            scatter_chart = alt.Chart(filtered_data).mark_circle(size=100).encode(
                x=alt.X('longitude:Q', title='Longitude'),
                y=alt.Y('latitude:Q', title='Latitude'),
                size=alt.Size('total:Q', scale=alt.Scale(range=[50, 500]), title='Homeless Population'),
                color=alt.Color('total:Q', scale=alt.Scale(scheme='viridis'), title='Homeless Population'),
                tooltip=['country:N', 'total:Q', 'latitude:Q', 'longitude:Q']  # Tooltip to show values
            ).interactive()

            st.altair_chart(scatter_chart, use_container_width=True)
# ------------------------------------------------------------------------------------------------

# Footer with 
with st.container():
    left_margin, content, right_margin = st.columns([1, 6, 1])
    with content:
        st.markdown("""
          ### Conclusion  
          *The Global Homelessness Dashboard provides a data-driven perspective on the pressing issue of homelessness across regions.*  
          *Through interactive visualizations, we aim to foster a deeper understanding of the trends, disparities, and underlying factors.*  
          *Together, insights from data can inspire impactful solutions to create a world where everyone has a place to call home.*  

          **Data Source**: [Global Homelessness Dataset](https://github.com/szs2/IE6600_Project2/blob/main/Data/Homelessness.csv)  
          Created with using [Streamlit](https://streamlit.io/).
          """)
