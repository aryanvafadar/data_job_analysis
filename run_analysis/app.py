import config
import functions
import folium
import folium.map
import numpy as np
import pandas as pd
import plotly.express as px

from folium.plugins import HeatMap
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly

ui.h1("Data Analytics Job Postings Analysis")
    

ui.h3("Query Results")

# Column wrap for our query 3 results 
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
                            color_discrete_sequence=px.colors.qualitative.Pastel
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
                color_continuous_scale='Peach'
            )
            
            figure.update_layout(
                plot_bgcolor='#F8FAFC',
                xaxis=dict(showgrid=True, gridcolor='#e1edf5'),
                yaxis=dict(showgrid=True, gridcolor='#e1edf5'),
                width=650,
                height=500
                
            )
            
            return figure
            

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
                color_continuous_scale=px.colors.sequential.Viridis,
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

