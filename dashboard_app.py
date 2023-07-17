import dash

# from dash.dependencies import Input, Output, State
from dash import html, dcc, Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
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
    suppress_callback_exceptions=True,
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
        dbc.Checklist(
            id="edit-dashboard-mode-button",
            # color="secondary",
            style={"margin-left": "20px", "font-size": "22px"},
            # size="lg",
            # n_clicks=0,
            options=[
                {"label": "Edit dashboard", "value": 0},
            ],
            value=[0],
            switch=True,
        ),
        # dmc.Switch(
        #     offLabel=DashIconify(icon="basil:edit-outline", width=20),
        #     onLabel=DashIconify(icon="basil:edit-solid", width=20),
        #     size="lg",
        # ),
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
        # dcc.Interval(
        #     id="save-input-value-interval",
        #     interval=2000,  # Save input value every 1 second
        #     n_intervals=0,
        # ),
        # dcc.Store(id="stored-year", storage_type="session", data=init_year),
        # dcc.Store(id="stored-children", storage_type="session", data=init_children),
        # dcc.Store(id="stored-layout", storage_type="session", data=init_layout),
        dcc.Store(id="stored-children", storage_type="session"),
        dcc.Store(id="stored-layout", storage_type="session"),
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
        # html.Div(id="year-input"),  # Added to display the selected value
        html.Div(id="year-input2"),  # Added to display the selected value
        backend_components,
        # dcc.input(
        #     id="year-input",
        #     min=df["year"].min(),
        #     max=df["year"].max(),
        #     value=init_year,
        #     marks={str(year): str(year) for year in df["year"].unique()},
        #     step=None,
        #     included=True,
        # ),
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


# @app.callback(
#     Output("stored-year", "data"),
#     Input("save-input-value-interval", "n_intervals"),
#     State("year-input", "value"),
# )
# def save_input_value(n_intervals, value):
#     if n_intervals == 0:
#         raise dash.exceptions.PreventUpdate
#     return value


# @app.callback(
#     Output("year-input", "value"),
#     Input("stored-year", "data"),
# )
# def update_input_value(data):
#     if data is None:
#         raise dash.exceptions.PreventUpdate

#     return data


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


# @app.callback(
#     Output("year-input", "children"),
#     # Input({"type": "input", "index": dash.dependencies.ALL}, "value"),
#     Input("time-input", "value"),
# )
# def display_selected_value(value):
#     return html.Div("Selected year: {}".format(value))


@app.callback(
    Output("year-input2", "children"),
    Input({"type": "input-component", "index": ALL}, "value"),
    # Input("time-input", "value"),
)
def display_selected_value(value):
    return html.Div("Selected year: {}".format(value))


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
        Input("edit-dashboard-mode-button", "value"),
        Input({"type": "remove-button", "index": dash.dependencies.ALL}, "n_clicks"),
        Input({"type": "input-component", "index": dash.dependencies.ALL}, "value"),
        # Input("time-input", "value"),
        Input("stored-layout", "data"),
        Input("stored-children", "data"),
        Input("draggable", "layouts"),
    ],
    [
        State("draggable", "children"),
        State("draggable", "layouts"),
        State("stored-layout", "data"),
        State("stored-children", "data"),
    ],
    # prevent_initial_call=True,
)
def update_draggable_children(
    # n_clicks, selected_year, current_draggable_children, current_layouts, stored_figures
    *args,
):
    # for arg in [*args]:
    #     print("\n")
    #     print(arg)
    # print("______________________")

    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]
    print(triggered_input)
    print(ctx.triggered)
    print("\n")
    stored_layout_data = args[-7]
    stored_children_data = args[-6]
    new_layouts = args[-5]
    # print(args[-10])
    switch_state = True if len(args[-10]) > 0 else False
    # print(f"Switch state: {switch_state}")

    # remove-button -6
    # selected_year = args[-5]

    # TODO: fix this
    selected_year = init_year

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
        print(n_clicks)

        new_plot_id = f"graph-{n_clicks}-{plot_type.lower().replace(' ', '-')}"
        new_plot_type = plot_type
        print(new_plot_type)

        if "-card" in new_plot_type:
            new_plot = html.Div(
                create_initial_figure(df, selected_year, new_plot_type), id=new_plot_id
            )
        elif "-input" in new_plot_type:
            print(new_plot_id)
            # input_id = f"{plot_type.lower().replace(' ', '-')}"
            new_plot = create_initial_figure(
                df, selected_year, new_plot_type, new_plot_id
            )
        else:
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
        # print(new_plot)

        # new_draggable_child = new_plot
        edit_button = dbc.Button(
            "Edit",
            id={
                "type": "edit-button",
                "index": f"edit-{new_plot_id}",
            },
            color="secondary",
            style={"margin-left": "10px"},
            # size="lg",
        )
        new_draggable_child = html.Div(
            [
                dbc.Button(
                    "Remove",
                    id={"type": "remove-button", "index": f"remove-{new_plot_id}"},
                    color="danger",
                ),
                edit_button,
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

    elif "-input" in triggered_input and 'remove-' not in triggered_input:
        input_id = ast.literal_eval(triggered_input)["index"]
        input_value = ctx.triggered[0]["value"]

        updated_draggable_children = []

        for child in current_draggable_children:
            if child["props"]["id"].replace("draggable-", "") == input_id:
                updated_draggable_children.append(child)
            elif child["props"]["id"].replace("draggable-", "") != input_id:
                # print(child["props"]["id"]["index"])
                index = -1 if switch_state is True else 0
                graph = child["props"]["children"][index]
                if type(graph["props"]["id"]) is str:
                    # Extract the figure type and its corresponding function
                    figure_type = "-".join(graph["props"]["id"].split("-")[2:])
                    graph_id = graph["props"]["id"]
                    updated_fig = create_initial_figure(df, input_value, figure_type)

                    if "-card" in graph_id:
                        graph["props"]["children"] = updated_fig

                    else:
                        graph["props"]["figure"] = updated_fig
                    rm_button = dbc.Button(
                        "Remove",
                        id={
                            "type": "remove-button",
                            "index": child["props"]["id"],
                        },
                        color="danger",
                    )
                    edit_button = dbc.Button(
                        "Edit",
                        id={
                            "type": "edit-button",
                            "index": child["props"]["id"],
                        },
                        color="secondary",
                        style={"margin-left": "10px"},
                    )
                    children = (
                        [rm_button, edit_button, graph]
                        if switch_state is True
                        else [graph]
                    )
                    updated_child = html.Div(
                        children=children,
                        id=child["props"]["id"],
                    )

                    updated_draggable_children.append(updated_child)
        return (
            updated_draggable_children,
            current_layouts,
            current_layouts,
            updated_draggable_children,
        )

    # if the remove button was clicked, return an empty list to remove all the plots

    elif "remove-" in triggered_input:
        print(triggered_input, type(triggered_input))
        # extract the UUID from the button_id
        # try:

        button_id = ast.literal_eval(triggered_input)
        # except:
        #     pass
        # print(button_id, type(button_id))
        button_uuid = button_id["index"]
        # print("\n")
        # print(button_uuid)

        print(current_draggable_children)
        # find the child div with the corresponding id
        for child in current_draggable_children:
            print(child)
            # print("\n")
            print(child["props"]["id"], button_uuid)
            if "-".join(child["props"]["id"].split('-')[1:]) == "-".join(button_uuid.split('-')[1:]):
                print(child["props"]["id"])
                print(current_draggable_children)
                print(len(current_draggable_children))
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
    elif triggered_input == "edit-dashboard-mode-button":
        # switch_state = True if len(ctx.triggered[0]["value"]) > 0 else False
        print(switch_state)
        # assuming the switch state is added as the first argument in args
        updated_draggable_children = []

        for child in current_draggable_children:
            graph = child["props"]["children"][
                -1
            ]  # Assuming graph is always the last child
            if switch_state:  # If switch is 'on', add the remove button
                remove_button = dbc.Button(
                    "Remove",
                    id={
                        "type": "remove-button",
                        "index": child["props"]["id"],
                    },
                    color="danger",
                )
                edit_button = dbc.Button(
                    "Edit",
                    id={
                        "type": "edit-button",
                        "index": child["props"]["id"],
                    },
                    color="secondary",
                    style={"margin-left": "10px"},
                )

                updated_child = html.Div(
                    [remove_button, edit_button, graph],
                    id=child["props"]["id"],
                )
            else:  # If switch is 'off', remove the button
                updated_child = html.Div(
                    [graph],
                    id=child["props"]["id"],
                )
            updated_draggable_children.append(updated_child)
        return (
            updated_draggable_children,
            new_layouts,
            # selected_year,
            new_layouts,
            updated_draggable_children,
            # selected_year,
        )

    # Add an else condition to return the current layout when there's no triggering input
    else:
        raise dash.exceptions.PreventUpdate


@app.callback(
    Output("save-button-dashboard", "n_clicks"),
    Input("save-button-dashboard", "n_clicks"),
    State("stored-layout", "data"),
    State("stored-children", "data"),
    # State("stored-year", "data"),
)
def save_data_dashboard(
    n_clicks,
    stored_layout_data,
    stored_children_data,
    # stored_year_data,
):
    # print(dash.callback_context.triggered[0]["prop_id"].split(".")[0], n_clicks)
    if n_clicks > 0:
        data = {
            "stored_layout_data": stored_layout_data,
            "stored_children_data": stored_children_data,
            # "stored_year_data": stored_year_data,
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


if __name__ == "__main__":
    app.run_server(debug=True, port="8052")
