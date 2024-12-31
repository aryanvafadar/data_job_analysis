import config
import functions
import folium
import folium.map
import pandas as pd
import plotly.express as px

from folium.plugins import HeatMap
from shiny import reactive
from shiny.express import render, ui
from shinywidgets import render_plotly

ui.tags.style(
    """
    * {
        font-family: Arial;
    }
    
    body {
        background-color: #F7FAFC;
    }
    
    h1 {
        color: #1C435A;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        font-weight: 600;`
    }
    
    .modebar {
        display: none;
    }
    
    .card {
        color: #1C435A;
        border-color: #37A6A5;
    }
    
    .card-header {
        color: #1C435A;
        border-color: #37A6A5;
    }
    
    """
)


ui.h1("Data Analytics Job Postings Analysis")  


# Column wrap for most important skills by career level and associated chart 
with ui.layout_column_wrap(width=1/2):
    
    # Card for Query 3
    with ui.card():
    
        ui.card_header("Most Important Skills To Learn By Career Level")
        
        @render.data_frame
        def display_query_3():
            frame = query_3_frame()
            
            return frame

    # Card for query 2
    with ui.card():
        
        ui.card_header("Relationship Between Salary & Career Level")
        
        @render_plotly
        def career_level_visualization():
            
            starting_frame =  query_3_frame() # dataframe for the bar chart
            
            figure = px.bar(data_frame=starting_frame, # creating our figure
                            x='job_category',
                            y=['min_salary', 'avg_salary', 'max_salary'],
                            color_discrete_sequence=px.colors.qualitative.Prism
                            )
            
            # Update the title, axises and bar mode
            figure.update_layout(
                title={
                    'text': 'Salary Comparisons Across Career Levels',
                    'x': 0.4, # adjust the horizontal position of the title
                    'xanchor': 'center'}, # Update title
                xaxis_title='Career Level', # Update x axis title
                yaxis_title='Salary ($)', # Update y axis title
                barmode='group', # Set bar mode option
                plot_bgcolor='#F8FAFC',
                xaxis=dict(showgrid=True, gridcolor='#e1edf5'),
                yaxis=dict(showgrid=True, gridcolor='#e1edf5'),
                font=dict(
                    size=12,
                    color='black' 
                ),
                
            )
            
            return figure
        
# Column wrap for top 3 skills in demand for remote jobs and associated chart
with ui.layout_column_wrap(width=1/2):
    
    with ui.card():
        
        ui.card_header("Top 3 Skills in Demand for Remote Jobs")
        
        @render.data_frame
        def display_query_2():
            query = query_2_frame()
            
            new_frame = query.drop(columns=['position'])
            
            return render.DataGrid(data=new_frame, summary=True, editable=True, filters=True)
    
    with ui.card():
        
        ui.card_header("Most Common Programming Languages & Their Salaries")
        
        @render_plotly
        def display_query_4():
            
            frame = query_1_frame()
            print(frame)
            
            figure = px.scatter(
                data_frame=frame,
                x='skills',
                y='salary_year_avg',
                color='salary_year_avg',
                color_continuous_scale='Tempo'
            )
            
            figure.update_layout(
                plot_bgcolor='#F8FAFC',
                xaxis=dict(showgrid=True, gridcolor='#e1edf5'),
                yaxis=dict(showgrid=True, gridcolor='#e1edf5'),
                width=650,
                height=550 
            )
            
            return figure
            
# Column wrap for parrallel relationship chart
with ui.layout_column_wrap(width=1/1):
    
    with ui.card():
        
        ui.card_header("Relationship Between Positions, Skills, and Salaries")
        
        @render_plotly
        def most_important_skills_visualization():
            
            frame = query_2_frame()
            
            fig = px.parallel_categories(
                frame,
                dimensions=["position", "top_skills"],
                color="avg_salary",
                color_continuous_scale=px.colors.sequential.ice,
                title="Relationship Between Positions, Skills, and Salaries"
            )
            
            fig.update_layout(
                title=dict(),
                margin=dict(l=250, r=100, t=50, b=50),
                width=1150,
                height= 600,
                coloraxis_colorbar=dict(
                    orientation='h',
                    x=0.4,
                    y=-0.2,
                    xanchor='center',
                    title='Average Salary ($)'
                )
            )
            
            return fig
        
# Column wrap for heat map with job postings by country
with ui.layout_column_wrap(width=1/1):
    
    with ui.card():
        
        ui.card_header('Heatmap of All Job Positings for Data Analytics Positions')
        
        @render.ui
        def create_job_posting_heatmap():
            
            frame = total_postings_by_country()
            
            heat_map_frame = frame[['lat', 'lon', 'total_jobs']].values.tolist()
            
            map = folium.Map(
                location=[37.0902, -95.7129],
                max_zoom=10,
                min_zoom=2,
                zoom_start=5,
            )
            
            HeatMap(data=heat_map_frame,
                    radius=15,
                    blur=17.5).add_to(map)
            
            return map      


# All of our reactive calcs
@reactive.calc # Dataframe  for Query 2
def query_2_frame() -> pd.DataFrame:
    
    frame = functions.sql_query_to_dataframe(file_1=config.sql_3b, db_params=config.db_parameters)
    
    return frame

@reactive.calc # Dataframe for Query 3
def query_3_frame() -> pd.DataFrame:
    
    frame = functions.sql_query_to_dataframe(file_1=config.sql_4, db_params=config.db_parameters)
    
    return frame

@reactive.calc # Dataframe for Query 4
def query_1_frame() -> pd.DataFrame:
    
    frame = functions.sql_query_to_dataframe(file_1=config.sql_5, db_params=config.db_parameters)
    
    return frame

@reactive.calc # Dataframe for Query 5
def total_postings_by_country() -> pd.DataFrame:
    
    # create frame
    country_frame = functions.sql_query_to_dataframe(file_1=config.sql_6, db_params=config.db_parameters)
    print(country_frame.head(5))
    
    
    # add placeholder values for lat and long
    country_frame['lat'] = 'N/A'
    country_frame['lon'] = 'N/A'
    
    # dictionary for our coordinates
    country_coordinates = {
    "United States": {"lat": 37.0902, "lon": -95.7129},
    "India": {"lat": 20.5937, "lon": 78.9629},
    "United Kingdom": {"lat": 55.3781, "lon": -3.4360},
    "Sudan": {"lat": 15.5007, "lon": 32.5599},
    "Germany": {"lat": 51.1657, "lon": 10.4515},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "France": {"lat": 46.6034, "lon": 1.8883},
    "Spain": {"lat": 40.4637, "lon": -3.7492},
    "Portugal": {"lat": 39.3999, "lon": -8.2245},
    "Netherlands": {"lat": 52.3676, "lon": 4.9041},
    "Canada": {"lat": 56.1304, "lon": -106.3468},
    "Poland": {"lat": 51.9194, "lon": 19.1451},
    "Italy": {"lat": 41.8719, "lon": 12.5674},
    "Ireland": {"lat": 53.1424, "lon": -7.6921},
    "Belgium": {"lat": 50.8503, "lon": 4.3517},
    "Austria": {"lat": 47.5162, "lon": 14.5501},
    "Mexico": {"lat": 23.6345, "lon": -102.5528},
    "Denmark": {"lat": 56.2639, "lon": 9.5018},
    "Switzerland": {"lat": 46.8182, "lon": 8.2275},
    "United Arab Emirates": {"lat": 23.4241, "lon": 53.8478},
    "South Africa": {"lat": -30.5595, "lon": 22.9375},
    "Hong Kong": {"lat": 22.3193, "lon": 114.1694},
    "Australia": {"lat": -25.2744, "lon": 133.7751},
    "Philippines": {"lat": 12.8797, "lon": 121.7740},
    "Chile": {"lat": -35.6751, "lon": -71.5430},
    "Thailand": {"lat": 15.8700, "lon": 100.9925},
    "Saudi Arabia": {"lat": 23.8859, "lon": 45.0792},
    "Colombia": {"lat": 4.5709, "lon": -74.2973},
    "Brazil": {"lat": -14.2350, "lon": -51.9253},
    "Sweden": {"lat": 60.1282, "lon": 18.6435},
    "Malaysia": {"lat": 4.2105, "lon": 101.9758},
    "Argentina": {"lat": -38.4161, "lon": -63.6167},
    "Finland": {"lat": 61.9241, "lon": 25.7482},
    "Czechia": {"lat": 49.8175, "lon": 15.4730},
    "Costa Rica": {"lat": 9.7489, "lon": -83.7534},
    "Kenya": {"lat": -1.286389, "lon": 36.817223},
    "Pakistan": {"lat": 30.3753, "lon": 69.3451},
    "Israel": {"lat": 31.0461, "lon": 34.8516},
    "Ukraine": {"lat": 48.3794, "lon": 31.1656},
    "Peru": {"lat": -9.1900, "lon": -75.0152},
    "Luxembourg": {"lat": 49.8153, "lon": 6.1296},
    "Indonesia": {"lat": -0.7893, "lon": 113.9213},
    "Romania": {"lat": 45.9432, "lon": 24.9668},
    "Hungary": {"lat": 47.1625, "lon": 19.5033},
    "Russia": {"lat": 61.5240, "lon": 105.3188},
    "Qatar": {"lat": 25.276987, "lon": 51.520008},
    "Puerto Rico": {"lat": 18.2208, "lon": -66.5901},
    "Egypt": {"lat": 26.8206, "lon": 30.8025},
    "China": {"lat": 35.8617, "lon": 104.1954},
    "Tunisia": {"lat": 33.8869, "lon": 9.5375},
    "Norway": {"lat": 60.4720, "lon": 8.4689},
    "Nigeria": {"lat": 9.0820, "lon": 8.6753},
    "Uruguay": {"lat": -32.5228, "lon": -55.7658},
    "Vietnam": {"lat": 14.0583, "lon": 108.2772},
    "Greece": {"lat": 39.0742, "lon": 21.8243},
    "Kazakhstan": {"lat": 48.0196, "lon": 66.9237},
    "Jordan": {"lat": 30.5852, "lon": 36.2384},
    "Lithuania": {"lat": 55.1694, "lon": 23.8813},
    "Turkey": {"lat": 38.9637, "lon": 35.2433},
    "South Korea": {"lat": 35.9078, "lon": 127.7669},
    "Taiwan": {"lat": 23.6978, "lon": 120.9605},
    "Bulgaria": {"lat": 42.7339, "lon": 25.4858},
    "Estonia": {"lat": 58.5953, "lon": 25.0136},
    "Panama": {"lat": 8.5380, "lon": -80.7821},
    "Morocco": {"lat": 31.7917, "lon": -7.0926},
    "Kuwait": {"lat": 29.3759, "lon": 47.9774},
    "Armenia": {"lat": 40.0691, "lon": 45.0382},
    "Malta": {"lat": 35.9375, "lon": 14.3754},
    "Uzbekistan": {"lat": 41.3775, "lon": 64.5853},
    "U.S. Virgin Islands": {"lat": 18.3358, "lon": -64.8963},
    "Lebanon": {"lat": 33.8547, "lon": 35.8623},
    "Guam": {"lat": 13.4443, "lon": 144.7937},
    "Serbia": {"lat": 44.0165, "lon": 21.0059},
    "Slovakia": {"lat": 48.6690, "lon": 19.6990},
    "Jamaica": {"lat": 18.1096, "lon": -77.2975},
    "Japan": {"lat": 36.2048, "lon": 138.2529},
    "Cyprus": {"lat": 35.1264, "lon": 33.4299},
    "Bahrain": {"lat": 26.0667, "lon": 50.5577},
    "Guatemala": {"lat": 15.7835, "lon": -90.2308},
    "Bangladesh": {"lat": 23.6850, "lon": 90.3563},
    "Nicaragua": {"lat": 12.8654, "lon": -85.2072},
    "Belarus": {"lat": 53.7098, "lon": 27.9534},
    "Moldova": {"lat": 47.4116, "lon": 28.3699},
    "Senegal": {"lat": 14.4974, "lon": -14.4524},
    "Iraq": {"lat": 33.2232, "lon": 43.6793},
    "El Salvador": {"lat": 13.7942, "lon": -88.8965},
    "Latvia": {"lat": 56.8796, "lon": 24.6032},
    "Sri Lanka": {"lat": 7.8731, "lon": 80.7718},
    "Dominican Republic": {"lat": 18.7357, "lon": -70.1627},
    "Ecuador": {"lat": -1.8312, "lon": -78.1834},
    "Mozambique": {"lat": -18.6657, "lon": 35.5296},
    "Albania": {"lat": 41.1533, "lon": 20.1683},
    "Namibia": {"lat": -22.9576, "lon": 18.4904},
    "Paraguay": {"lat": -23.4425, "lon": -58.4438},
    "Bolivia": {"lat": -16.2902, "lon": -63.5887},
    "Ethiopia": {"lat": 9.145, "lon": 40.489673},
    "New Zealand": {"lat": -40.9006, "lon": 174.886},
    "Croatia": {"lat": 45.1, "lon": 15.2},
    "Zambia": {"lat": -13.1339, "lon": 27.8493},
    "Oman": {"lat": 21.4735, "lon": 55.9754},
    "Slovenia": {"lat": 46.1512, "lon": 14.9955},
    "Tanzania": {"lat": -6.3690, "lon": 34.8888},
    "Rwanda": {"lat": -1.9403, "lon": 29.8739},
}
    
    # apply lambda functions to assign values to our dataframe from our dict
    country_frame['lat'] = country_frame['job_country'].map(lambda x: country_coordinates[x]['lat'])
    country_frame['lon'] = country_frame['job_country'].map(lambda x: country_coordinates[x]['lon'])    
    
    print(country_frame.head(3))
    
    return country_frame
