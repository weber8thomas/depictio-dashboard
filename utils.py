import plotly.express as px
from dash import html, dcc, Input, Output, State
import os, json
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


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
            "title": "Scatter plot of GDP per Capita vs. Life Expectancy",
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
    "time-slider-input": {
        "type": "Input",
        "description": "Year slider",
        "property": "Property Z",
        "material-icons": "tune",
        "function": dcc.Slider,
        "kwargs": {
            "column": "year",
            # "operation": lambda col: round(col.mean(), 2),
            # "min": df["year"].min(),
            # "max": df["year"].max(),
            # "value": init_year,
            # "step": None,
            # "included": True,
        },
    },
    "continent-multiselect-input": {
        "type": "Input",
        "description": "Continent dropdown",
        "property": "Property I",
        "material-icons": "tune",
        "function": dcc.Dropdown,
        "kwargs": {
            "column": "continent",
            "multi": True,
            # "operation": lambda col: round(col.mean(), 2),
            # "min": df["year"].min(),
            # "max": df["year"].max(),
            # "value": init_year,
            # "step": None,
            # "included": True,
        },
    },
    "lifeexp-slider-input": {
        "type": "Input",
        "description": "Continent dropdown",
        "property": "Property I",
        "material-icons": "tune",
        "function": dcc.Dropdown,
        "kwargs": {
            "column": "continent",
            "multi": True,
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


def create_input_component(df, dict_data, input_component_id):
    # print(dict_data)
    col = dict_data["kwargs"]["column"]
    # print(col)
    # print(df)
    ComponentFunction = dict_data.get("function", dcc.Slider)  # Default to dcc.Slider

    if ComponentFunction is dcc.Slider:
        kwargs = dict(
            min=df[f"{col}"].min(),
            max=df[f"{col}"].max(),
            # value=value,
            marks={str(elem): str(elem) for elem in df[f"{col}"].unique()},
            step=None,
            included=True,
        )
    elif ComponentFunction is dcc.Dropdown:
        kwargs = dict(
            options=[{"label": i, "value": i} for i in df[f"{col}"].unique().tolist()],
            # value=value,
            multi=True,
        )
    # kwargs = dict(
    #     min=df[f"{col}"].min(),
    #     max=df[f"{col}"].max(),
    #     value=value,
    #     marks={str(elem): str(elem) for elem in df[f"{col}"].unique()},
    #     step=None,
    #     included=True,
    # )

    # return ComponentFunction(
    #     # id=input_component_id,
    #     # df[f"{col}"].unique().tolist(),
    #     id={"type": "input-component", "index": input_component_id},
    #     **kwargs,
    # )
    return html.Div(
        children=[
            html.H5(dict_data["description"]),
            ComponentFunction(
                # id=input_component_id,
                # df[f"{col}"].unique().tolist(),
                id={"type": "input-component", "index": input_component_id},
                **kwargs,
            ),
        ]
    )


def process_data_for_card(df, column, operation):
    value = operation(df[column])
    return value


def create_initial_figure(df, plot_type, input_id=None, filter=dict(), id=None):
    # print("TOTO")
    # print(selected_year)
    print(df)
    print(filter)
    print(plot_type)
    if filter and input_id:
        filtered_df = df
        # Apply all active filters
        for input_component_name, filter_value in filter.items():
            column_name = AVAILABLE_PLOT_TYPES[input_component_name]["kwargs"]["column"]
            print(column_name, filter_value)
            if isinstance(filter_value, list):  # check if filter_value is a list
                if filter_value:
                    filtered_df = filtered_df[filtered_df[column_name].isin(filter_value)]
                else:
                    filtered_df = filtered_df
            else:
                filtered_df = filtered_df[filtered_df[column_name] == filter_value]

    else:
        filtered_df = df
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
            value,
            AVAILABLE_PLOT_TYPES[plot_type]["kwargs"]["legend"],
        )
    elif AVAILABLE_PLOT_TYPES[plot_type]["type"] is "Input":
        fig = create_input_component(
            df,
            AVAILABLE_PLOT_TYPES[plot_type],
            input_component_id=id
            # selected_year, df, AVAILABLE_PLOT_TYPES[plot_type], id
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
