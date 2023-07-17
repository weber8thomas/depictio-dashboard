from dash import html, dcc, Input, Output, State, ALL, MATCH
import dash

import plotly.express as px
import pandas as pd

import dash_draggable

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)

app.layout = html.Div(
    [
        html.H1("Dash Draggable"),
        dash_draggable.ResponsiveGridLayout(
            id="draggable",
            children=[
                # html.Div(
                #     children=[
                #         dcc.Graph(
                #             id="graph-with-slider",
                #             responsive=True,
                #             style={"min-height": "0", "flex-grow": "1"},
                #         )
                #     ],
                #     style={
                #         "height": "100%",
                #         "width": "100%",
                #         "display": "flex",
                #         "flex-direction": "column",
                #         "flex-grow": "0",
                #     },
                # ),
                html.Div(
                    children=[
                        dcc.Slider(
                            id={"type":"slider", "index": "year-slider"},
                            # id="year-slider",
                            min=df["year"].min(),
                            max=df["year"].max(),
                            value=df["year"].min(),
                            marks={
                                str(year): str(year) for year in df["year"].unique()
                            },
                            step=None,
                        )
                    ],
                    style={
                        "height": "100%",
                        "width": "100%",
                        "display": "flex",
                        "flex-direction": "column",
                        "flex-grow": "0",
                    },
                ),
            ],
        ),
        html.Div(id="output-container"),  # Added to display the selected value
        html.Div(id="output-container2"),  # Added to display the selected value
    ]
)


# @app.callback(Output("graph-with-slider", "figure"), Input("year-slider", "value"))
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]

#     fig = px.scatter(
#         filtered_df,
#         x="gdpPercap",
#         y="lifeExp",
#         size="pop",
#         color="continent",
#         hover_name="country",
#         log_x=True,
#         size_max=55,
#     )

#     fig.update_layout(transition_duration=500)

#     return fig


# Added callback to display the slider's selected value
@app.callback(Output("output-container", "children"), [Input({"type":"slider", "id": "year-slider"}, "value")])
def display_selected_value(value):
    return "Selected year: {}".format(value)

# Added callback to display the slider's selected value
@app.callback(Output("output-container2", "children"), [
    Input({"type": "slider", "index": ALL}, "value"),
    ])
def display_selected_value(value):
    return "Selected year: {}".format(value)


if __name__ == "__main__":
    app.run_server(debug=True, port="5080")
