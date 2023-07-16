import plotly.express as px
from dash import html, dcc, Input, Output, State
import os, json
import dash_bootstrap_components as dbc


AVAILABLE_PLOT_TYPES = {
    "scatter-plot": {
        "type": "Scatter plot",
        "description": "Scatter plot of GDP per Capita vs. Life Expectancy",
        "property": "Property A",
        "material-icons": "scatter_plot",
        "function": px.scatter,
        "kwargs": {
            "x": "gdpPercap",
            "y": "lifeExp",
            "size": "pop",
            "color": "continent",
            "hover_name": "country",
            "log_x": True,
            "size_max": 55,
            # "animation_frame": "year",
        },
    },
    "bar-plot": {
        "type": "Bar plot",
        "description": "Bar plot of Total GDP per Year",
        "property": "Property B",
        "material-icons": "bar_chart",
        "function": px.bar,
        "kwargs": {
            "x": "year",
            "y": "gdpPercap",
            "color": "continent",
            "hover_name": "country",
            "facet_col": "continent",
            "facet_col_wrap": 3,
            "height": 700,
        },
    },
    "line-plot": {
        "type": "Line plot",
        "description": "Line plot of GDP per Capita over Time",
        "property": "Property C",
        "material-icons": "show_chart",
        "function": px.line,
        "kwargs": {
            "x": "year",
            "y": "gdpPercap",
            "color": "continent",
            "hover_name": "country",
            "line_group": "country",
            "line_shape": "spline",
            "render_mode": "svg",
        },
    },
    "box-plot": {
        "type": "Box plot",
        "description": "Box plot of Life Expectancy by Continent",
        "property": "Property D",
        "material-icons": "candlestick_chart",
        "function": px.box,
        "kwargs": {
            "x": "continent",
            "y": "lifeExp",
            "color": "continent",
            "hover_name": "country",
            "points": "all",
            "notched": True,
        },
    },
    "pie-chart": {
        "type": "Pie chart",
        "description": "Pie chart of Population by Continent",
        "property": "Property E",
        "material-icons": "pie_chart",
        "function": px.pie,
        "kwargs": {
            "names": "continent",
            "values": "pop",
            "hover_name": "continent",
            "hole": 0.4,
            # "animation_frame": "year",
            # "title": "Population by Continent",
        },
    },
    "countries-card": {
        "type": "Card",
        "description": "Countries number",
        "property": "Property X",
        "material-icons": "score",
        "function": dbc.Card,
        "kwargs": {
            "legend": "Countries number",
            "column": "country",
            "operation": lambda col: col.nunique(),
        },
    },
    "global-lifeexp-card": {
        "type": "Card",
        "description": "Average life expectancy",
        "property": "Property X",
        "material-icons": "score",
        "function": dbc.Card,
        "kwargs": {
            "legend": "Average life expectancy",
            "column": "lifeExp",
            "operation": lambda col: round(col.mean(), 2),
        },
    },
    "time-slider": {
        "type": "Slider",
        "description": "Year slider",
        "property": "Property Z",
        "material-icons": "tune",
        "function": dcc.Slider,
        "kwargs": {
            "legend": "Average life expectancy",
            "column": "year",
            # "operation": lambda col: round(col.mean(), 2),
            # "min": df["year"].min(),
            # "max": df["year"].max(),
            # "value": init_year,
            # "step": None,
            # "included": True,
        },
    },
}


# Add a new function to create a card with a number and a legend
def create_card(value, legend):
    return dbc.Card(
        [
            html.H2("{value}".format(value=value), className="card-title"),
            html.P(legend, className="card-text"),
        ],
        body=True,
        color="light",
    )


def create_slider(value, df, dict_data, slider_id):
    # print(dict_data)
    col = dict_data["column"]
    # print(col)
    # print(df)
    return dcc.Slider(
        id={"type": "slider", "id":slider_id},
        min=df[f"{col}"].min(),
        max=df[f"{col}"].max(),
        value=value,
        marks={str(elem): str(elem) for elem in df[f"{col}"].unique()},
        step=None,
        included=True,
    )


def process_data_for_card(df, column, operation):
    value = operation(df[column])
    return value


def create_initial_figure(df, selected_year, plot_type, id=None):
    # print("TOTO")
    # print(selected_year)
    filtered_df = df[df.year == selected_year]
    # filtered_df = df
    # print(plot_type)
    if AVAILABLE_PLOT_TYPES[plot_type]["type"] is "Card":
        value = process_data_for_card(
            filtered_df,
            AVAILABLE_PLOT_TYPES[plot_type]["kwargs"]["column"],
            AVAILABLE_PLOT_TYPES[plot_type]["kwargs"]["operation"],
        )
        # print(value)
        fig = create_card(
            selected_year,
            AVAILABLE_PLOT_TYPES[plot_type]["kwargs"]["legend"],
        )
    elif AVAILABLE_PLOT_TYPES[plot_type]["type"] is "Slider":
        fig = create_slider(
            selected_year,
            df,
            AVAILABLE_PLOT_TYPES[plot_type]["kwargs"],
            id
        )
    else:
        fig = AVAILABLE_PLOT_TYPES[plot_type]["function"](
            filtered_df, **AVAILABLE_PLOT_TYPES[plot_type]["kwargs"]
        )

        fig.update_layout(transition_duration=500)

    return fig


def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            data = json.load(file)
        return data
    return None
