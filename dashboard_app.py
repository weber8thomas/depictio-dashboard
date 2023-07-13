import dash

# from dash.dependencies import Input, Output, State
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import dash_draggable
from dash import dash_table
import time
import os, json
import json
import ast
import pandas
from utils import (
    AVAILABLE_PLOT_TYPES,
    load_data,
    create_card,
    process_data_for_card,
    create_initial_figure,
)
from config import external_stylesheets

# AVAILABLE_PLOT_TYPES = dict(sorted(AVAILABLE_PLOT_TYPES.items()))


app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    # suppress_callback_exceptions=True,
)


df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)


data = load_data()
init_layout = data["stored_layout_data"] if data else {}
init_children = data["stored_children_data"] if data else list()
init_year = data["stored_year_data"] if data else df["year"].min()


header = dbc.Col(
    [
        html.H2("Description", className="mb-3"),
        html.Ul(
            [
                html.Li(
                    [
                        html.I(
                            className="material-icons mr-1",
                            children="check_circle_outline",
                        ),
                        "The charts are draggable and resizable.",
                    ],
                    className="lead",
                ),
                html.Li(
                    [
                        html.I(
                            className="material-icons mr-1",
                            children="check_circle_outline",
                        ),
                        "Click the 'Add Plot' button to add a new plot.",
                    ],
                    className="lead",
                ),
            ],
            className="list-unstyled",
        ),
    ],
)
buttons = dbc.Col(
    [
        dbc.Button(
            "Add Plot",
            id="add-plot-button",
            color="primary",
            size="lg",
            style={"font-size": "22px"},
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H1(
                        "Success!",
                        className="text-success",
                    )
                ),
                dbc.ModalBody(
                    html.H5(
                        "Your amazing dashboard was successfully saved!",
                        className="text-success",
                    ),
                    style={"background-color": "#F0FFF0"},
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="success-modal-close",
                        className="ml-auto",
                        color="success",
                    )
                ),
            ],
            id="success-modal-dashboard",
            centered=True,
        ),
        dbc.Button(
            "Save",
            id="save-button-dashboard",
            color="success",
            style={"margin-left": "10px", "font-size": "22px"},
            size="lg",
            n_clicks=0,
        ),
    ],
    className="d-flex justify-content-center align-items-center",
)


top_row = dbc.Row(
    [
        header,
        buttons,
        html.Hr(),
    ]
)

backend_components = html.Div(
    [
        dcc.Interval(
            id="save-slider-value-interval",
            interval=10000,  # Save slider value every 1 second
            n_intervals=0,
        ),
        dcc.Store(id="stored-year", storage_type="session", data=init_year),
        dcc.Store(id="stored-children", storage_type="session", data=init_children),
        dcc.Store(id="stored-layout", storage_type="session", data=init_layout),
    ]
)

modal_table_columns = html.Thead(
    [
        html.Tr(
            [
                html.Th(html.H5("")),
                html.Th(html.H5("Plot Type")),
                html.Th(html.H5("Description")),
                html.Th(
                    html.H5(
                        "Property",
                        style={"text-align": "left"},
                    ),
                ),
                html.Th(),
            ]
        )
    ]
)

modal_table_content = html.Tbody(
    [
        html.Tr(
            [
                html.Td(
                    html.I(
                        className="material-icons",
                        children=AVAILABLE_PLOT_TYPES[plot_type]["material-icons"],
                    )
                ),
                html.Td(AVAILABLE_PLOT_TYPES[plot_type]["type"]),
                html.Td(AVAILABLE_PLOT_TYPES[plot_type]["description"]),
                html.Td(AVAILABLE_PLOT_TYPES[plot_type]["property"]),
                html.Td(
                    dbc.Button(
                        "Select",
                        id=f"add-plot-button-{plot_type.lower().replace(' ', '-')}",
                        color="light",
                        n_clicks=0,
                        style={
                            "cursor": "pointer",
                            # "width": "100%",
                        },
                    ),
                    style={"text-align": "center"},
                ),
            ],
            id=f"{AVAILABLE_PLOT_TYPES[plot_type]['type'].lower().replace(' ', '-')}-row",
            style={"width": "100%"},
        )
        for plot_type in AVAILABLE_PLOT_TYPES
    ]
)

modal = dbc.Modal(
    [
        dbc.ModalHeader(html.H3("Select a plot type")),
        dbc.ModalBody(
            [
                dbc.Table(
                    [modal_table_columns, modal_table_content],
                    bordered=True,
                    hover=True,
                    responsive=True,
                    striped=True,
                    size="sm",
                    style={"width": "100%"},
                ),
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="modal-close-button", color="secondary")
        ),
    ],
    id="modal-dashboard",
    centered=True,
    size="lg",
)

app.layout = dbc.Container(
    [
        top_row,
        backend_components,
        dcc.Slider(
            id="year-slider",
            min=df["year"].min(),
            max=df["year"].max(),
            value=init_year,
            marks={str(year): str(year) for year in df["year"].unique()},
            step=None,
            included=True,
        ),
        dash_draggable.ResponsiveGridLayout(
            id="draggable",
            clearSavedLayout=True,
            layouts=init_layout,
            children=init_children,
        ),
        modal,
    ],
    fluid=False,
)


@app.callback(
    Output("save-button-dashboard", "n_clicks"),
    Input("save-button-dashboard", "n_clicks"),
    State("stored-layout", "data"),
    State("stored-children", "data"),
    State("stored-year", "data"),
)
def save_data_dashboard(
    n_clicks,
    stored_layout_data,
    stored_children_data,
    stored_year_data,
):
    # print(dash.callback_context.triggered[0]["prop_id"].split(".")[0], n_clicks)
    if n_clicks > 0:
        data = {
            "stored_layout_data": stored_layout_data,
            "stored_children_data": stored_children_data,
            "stored_year_data": stored_year_data,
        }
        with open("data.json", "w") as file:
            json.dump(data, file)
        return n_clicks
    return n_clicks


@app.callback(
    Output("success-modal-dashboard", "is_open"),
    [
        Input("save-button-dashboard", "n_clicks"),
        Input("success-modal-close", "n_clicks"),
    ],
    [State("success-modal-dashboard", "is_open")],
)
def toggle_success_modal_dashboard(n_save, n_close, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # print(trigger_id, n_save, n_close)

    if trigger_id == "save-button-dashboard":
        if n_save is None or n_save == 0:
            raise dash.exceptions.PreventUpdate
        else:
            return True

    elif trigger_id == "success-modal-close":
        if n_close is None or n_close == 0:
            raise dash.exceptions.PreventUpdate
        else:
            return False

    return is_open


@app.callback(
    Output("stored-year", "data"),
    Input("save-slider-value-interval", "n_intervals"),
    State("year-slider", "value"),
)
def save_slider_value(n_intervals, value):
    if n_intervals == 0:
        raise dash.exceptions.PreventUpdate
    return value


@app.callback(
    Output("year-slider", "value"),
    Input("stored-year", "data"),
)
def update_slider_value(data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    return data


# define the callback to show/hide the modal
@app.callback(
    Output("modal-dashboard", "is_open"),
    [Input("add-plot-button", "n_clicks"), Input("modal-close-button", "n_clicks")],
    [State("modal-dashboard", "is_open")],
)
def toggle_modal_dashboard(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [
        Output("draggable", "children"),
        Output("draggable", "layouts"),
        Output("stored-layout", "data"),
        Output("stored-children", "data"),
    ],
    [
        Input(f"add-plot-button-{plot_type.lower().replace(' ', '-')}", "n_clicks")
        for plot_type in AVAILABLE_PLOT_TYPES.keys()
    ]
    + [
        Input("stored-layout", "data"),
        Input("stored-children", "data"),
        Input("draggable", "layouts"),
        Input({"type": "remove-button", "index": dash.dependencies.ALL}, "n_clicks"),
        Input("year-slider", "value"),
    ],
    [
        State("draggable", "children"),
        State("draggable", "layouts"),
        State("stored-layout", "data"),
        State("stored-children", "data"),
    ],
)
def update_draggable_children(
    # n_clicks, selected_year, current_draggable_children, current_layouts, stored_figures
    *args,
):
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]
    # print(triggered_input)
    # print(ctx.triggered)
    stored_layout_data = args[-9]
    stored_children_data = args[-8]
    new_layouts = args[-7]
    # remove-button -6
    selected_year = args[-5]
    current_draggable_children = args[-4]
    current_layouts = args[-3]
    stored_layout = args[-2]
    stored_figures = args[-1]

    # if current_draggable_children is None:
    #     current_draggable_children = []
    # if current_layouts is None:
    #     current_layouts = dict()

    if triggered_input.startswith("add-plot-button-"):
        plot_type = triggered_input.replace("add-plot-button-", "")

        n_clicks = ctx.triggered[0]["value"]

        new_plot_id = f"graph-{n_clicks}-{plot_type.lower().replace(' ', '-')}"
        new_plot_type = plot_type

        if "-card" not in new_plot_type:
            new_plot = dcc.Graph(
                id=new_plot_id,
                figure=create_initial_figure(df, selected_year, new_plot_type),
                responsive=True,
                style={
                    "width": "100%",
                    "height": "100%",
                },
                # config={"staticPlot": False, "editable": True},
            )
        else:
            new_plot = html.Div(
                create_initial_figure(df, selected_year, new_plot_type), id=new_plot_id
            )
        # print(new_plot)

        new_draggable_child = html.Div(
            [
                dbc.Button(
                    "Remove",
                    id={"type": "remove-button", "index": new_plot_id},
                    color="danger",
                ),
                new_plot,
            ],
            id=f"draggable-{new_plot_id}",
        )
        # print(current_draggable_children)
        # print(len(current_draggable_children))

        updated_draggable_children = current_draggable_children + [new_draggable_child]

        # Define the default size and position for the new plot
        if "-card" not in new_plot_type:
            new_layout_item = {
                "i": f"draggable-{new_plot_id}",
                "x": 10 * ((len(updated_draggable_children) + 1) % 2),
                "y": n_clicks * 10,
                "w": 6,
                "h": 14,
            }
        else:
            new_layout_item = {
                "i": f"draggable-{new_plot_id}",
                "x": 10 * ((len(updated_draggable_children) + 1) % 2),
                "y": n_clicks * 10,
                "w": 4,
                "h": 5,
            }

        # Update the layouts property for both 'lg' and 'sm' sizes
        updated_layouts = {}
        for size in ["lg", "sm"]:
            if size not in current_layouts:
                current_layouts[size] = []
            updated_layouts[size] = current_layouts[size] + [new_layout_item]

        # Store the newly created figure in stored_figures
        # stored_figures[new_plot_id] = new_plot

        return (
            updated_draggable_children,
            updated_layouts,
            # selected_year,
            updated_layouts,
            updated_draggable_children,
            # selected_year,
        )

    elif triggered_input == "year-slider":
        updated_draggable_children = []

        for child in current_draggable_children:
            print("\n")
            print(child)
            # try:
            graph = child["props"]["children"][1]
            # print(graph)
            # Extract the figure type and its corresponding function
            figure_type = "-".join(graph["props"]["id"].split("-")[2:])
            # print(figure_type)
            print("\n")
            graph_id = graph["props"]["id"]
            print(graph_id)
            updated_fig = create_initial_figure(df, selected_year, figure_type)
            # stored_figures[graph_id] = updated_fig
            if "-card" not in graph_id:
                graph["props"]["figure"] = updated_fig
            else:
                graph["props"]["children"] = updated_fig

            updated_child = html.Div(
                [
                    dbc.Button(
                        "Remove",
                        id={"type": "remove-button", "index": child["props"]["id"]},
                        color="danger",
                    ),
                    graph,
                ],
                id=child["props"]["id"],
            )

            updated_draggable_children.append(updated_child)
            # except:
            #     # If any exception occurs, just append the current child without modifications
            #     updated_draggable_children.append(child)

        # return updated_draggable_children, current_layouts, stored_figures

        return (
            updated_draggable_children,
            current_layouts,
            # selected_year,
            current_layouts,
            updated_draggable_children,
            # selected_year,
        )

    # if the remove button was clicked, return an empty list to remove all the plots

    elif "remove-button" in triggered_input:
        # print(triggered_input)
        # extract the UUID from the button_id
        # try:

        button_id = ast.literal_eval(triggered_input)
        # except:
        #     pass
        # print(button_id, type(button_id))
        button_uuid = button_id["index"]
        # print("\n")
        # print(button_uuid)

        # find the child div with the corresponding id
        for child in current_draggable_children:
            # print(child)
            # print("\n")
            if child["props"]["id"] == button_uuid:
                current_draggable_children.remove(child)
        return (
            current_draggable_children,
            new_layouts,
            # selected_year,
            new_layouts,
            current_draggable_children,
            # selected_year,
        )
    elif triggered_input == "stored-layout" or triggered_input == "stored-children":
        if stored_layout_data and stored_children_data:
            return (
                stored_children_data,
                stored_layout_data,
                stored_layout_data,
                stored_children_data,
            )
        else:
            # Load data from the file if it exists
            loaded_data = load_data()
            if loaded_data:
                return (
                    loaded_data["stored_children_data"],
                    loaded_data["stored_layout_data"],
                    loaded_data["stored_layout_data"],
                    loaded_data["stored_children_data"],
                )
            else:
                return (
                    current_draggable_children,
                    {},
                    stored_layout,
                    stored_figures,
                )

    elif triggered_input == "draggable":
        return (
            current_draggable_children,
            new_layouts,
            # selected_year,
            new_layouts,
            current_draggable_children,
            # selected_year,
        )

    # Add an else condition to return the current layout when there's no triggering input
    else:
        raise dash.exceptions.PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True, port="8052")