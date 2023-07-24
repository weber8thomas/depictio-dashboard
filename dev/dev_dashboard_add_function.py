from dash import html, dcc, Input, Output, State, ALL, MATCH
from dash_bootstrap_components import Modal, ModalBody, Button
import dash_bootstrap_components as dbc
import dash

import plotly.express as px
import pandas as pd

import dash_draggable

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP,
    "https://use.fontawesome.com/releases/v5.7.2/css/all.css",
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)


df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)
# print(df)

# Import necessary libraries
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import inspect
import pandas as pd
import inspect
import json
import os
import plotly.express as px
import re
from pprint import pprint

import os, sys


def get_common_params(plotly_vizu_list):
    common_params = set.intersection(
        *[set(inspect.signature(func).parameters.keys()) for func in plotly_vizu_list]
    )
    common_param_names = [p for p in list(common_params)]
    common_param_names.sort(
        key=lambda x: list(inspect.signature(plotly_vizu_list[0]).parameters).index(x)
    )
    return common_params, common_param_names


def get_specific_params(plotly_vizu_list, common_params):
    specific_params = {}
    for vizu_func in plotly_vizu_list:
        func_params = inspect.signature(vizu_func).parameters
        param_names = list(func_params.keys())
        common_params_tmp = (
            common_params.intersection(func_params.keys())
            if common_params
            else set(func_params.keys())
        )
        specific_params[vizu_func.__name__] = [
            p for p in param_names if p not in common_params_tmp
        ]
    return specific_params


def extract_info_from_docstring(docstring):
    lines = docstring.split("\n")
    # print(lines)
    parameters_section = False
    result = {}

    for line in lines:
        # print(line)
        if line.startswith("Parameters"):
            parameters_section = True
            continue
        if parameters_section:
            # if line.startswith("----------"):
            #     break
            if line.startswith("    ") is False:
                # print(line.split(': '))
                line_processed = line.split(": ")
                # print(line_processed)
                if len(line_processed) == 2:
                    parameter, type = line_processed[0], line_processed[1]
                    result[parameter] = {"type": type, "description": list()}
                else:
                    continue

            elif line.startswith("    ") is True:
                # result[-1] += " " + line.strip()
                # print(line.strip())
                result[parameter]["description"].append(line.strip())

    return result


def process_json_from_docstring(data):
    for key, value in data.items():
        # Get the type associated with the field
        field_type = value.get("type")
        # field_type = value.get('type')
        description = " ".join(value.get("description"))

        # Check if there are any options available for the field
        options = []
        # for description in value.get('description', []):
        if "One of" in description:
            # The options are usually listed after 'One of'
            option_str = description.split("One of")[-1].split(".")[0]

            options = list(set(re.findall("`'(.*?)'`", option_str)))
        elif "one of" in data[key]["type"]:
            option_str = data[key]["type"].split("one of")[-1]
            options = list(set(re.findall("`'(.*?)'`", option_str)))

        if options:
            data[key]["options"] = options

        if "Series or array-like" in field_type:
            data[key]["processed_type"] = "column"
        else:
            data[key]["processed_type"] = data[key]["type"].split(" ")[0].split(",")[0]
    return data


def get_param_info(plotly_vizu_list):
    # Code for extract_info_from_docstring and process_json_from_docstring...
    # ...
    param_info = {}
    for func in plotly_vizu_list:
        param_info[func.__name__] = extract_info_from_docstring(func.__doc__)
        param_info[func.__name__] = process_json_from_docstring(
            param_info[func.__name__]
        )
    return param_info


def get_dropdown_options(df):
    dropdown_options = [{"label": col, "value": col} for col in df.columns]
    return dropdown_options


# TODO: utils / config

# Define the list of Plotly visualizations
plotly_vizu_list = [px.scatter, px.line, px.bar, px.histogram, px.box]

# Map visualization function names to the functions themselves
plotly_vizu_dict = {vizu_func.__name__: vizu_func for vizu_func in plotly_vizu_list}

# Get common and specific parameters for the visualizations
common_params, common_params_names = get_common_params(plotly_vizu_list)
specific_params = get_specific_params(plotly_vizu_list, common_params)

# Generate parameter information and dropdown options
param_info = get_param_info(plotly_vizu_list)
dropdown_options = get_dropdown_options(df)

# Define the elements for the dropdown menu
dropdown_elements = ["x", "y", "color"]

# Define allowed types and the corresponding Bootstrap components
allowed_types = ["str", "int", "float", "boolean", "column"]
plotly_bootstrap_mapping = {
    "str": dbc.Input,
    "int": dbc.Input,
    "float": dbc.Input,
    "boolean": dbc.Checklist,
    "column": dcc.Dropdown,
}

# Identify the parameters not in the dropdown elements
secondary_common_params = [
    e
    for e in common_params_names[1:]
    # e for e in common_params_names[1:] if e not in dropdown_elements
]


init_layout = dict()
init_children = list()
app.layout = html.Div(
    [
        html.H1("Dash Draggable"),
        html.Button("Add", id="add-button", n_clicks=0),
        dash_draggable.ResponsiveGridLayout(
            id="draggable",
            clearSavedLayout=True,
            layouts=init_layout,
            children=init_children,
            isDraggable=True,
            isResizable=True,
        ),
        dbc.Container(
            [
                # dcc.Interval(
                #     id="interval",
                #     interval=1000,  # Save slider value every 1 second
                #     n_intervals=0,
                # ),
                dcc.Store(id="selections-store", storage_type="session", data={}),
                # html.H1(
                #     "Prepare your visualization",
                #     className="text-center mb-4",
                # ),
                # html.Hr(),
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             [
                #                 dbc.Button(
                #                     "Edit",
                #                     id="edit-button",
                #                     color="primary",
                #                     size="lg",
                #                     style={"font-size": "22px"},
                #                 ),
                #             ],
                #             className="d-flex justify-content-center align-items-center",
                #         ),
                #         # html.Hr(),
                #         # dbc.Row(
                #         #     [
                #         #         dbc.Col(
                #         #             dcc.Graph(id="graph-container", config={"editable": True}),
                #         #         ),
                #         #     ],
                #         #     className="mt-3",
                #         # ),
                #     ],
                #     className="text-center mt-3",
                #     justify="center",
                # ),
                # html.Hr(),
                # html.Tr(),
                # dcc.Store("offcanvas-state-store", storage_type="session"),
                # dbc.Row(
                #     [
                #         dbc.Offcanvas(
                #             [
                #                 html.Div(id="specific-params-container"),
                #             ],
                #             id="modal",
                #             title="Edit Menu",
                #             scrollable=True,
                #             # size="xl",
                #             backdrop=False,
                #             placement="end",
                #         ),
                #     ],
                #     justify="center",
                # ),
            ],
            fluid=False,
        ),
        html.Div(id="output-container"),
        html.Div(id="output-container2"),
        html.Div(id="test-div"),
        # html.Div(id="tmp-container"),
    ]
)


# Add a Div element for testing the button's n_clicks


@app.callback(
    Output("test-div", "children"),
    Input("edit-button", "n_clicks"),
)
def test_button_clicks(n_clicks):
    return str(n_clicks)


@app.callback(
    Output({"type": "modal", "index": MATCH}, "is_open"),
    [Input({"type": "btn-done", "index": MATCH}, "n_clicks")],
    prevent_initial_call=True,
)
def close_modal(n_clicks):
    if n_clicks > 0:
        return False
    return True


@app.callback(
    [Output("draggable", "children"), Output("draggable", "layouts")],
    [Input("add-button", "n_clicks")],
    [State("draggable", "children"), State("draggable", "layouts")],
    prevent_initial_call=True,
)
def add_new_div(n, children, layouts):
    print("index: {}".format(n))
    new_plot_id = f"graph-{n}"

    new_element = html.Div(
        [
            html.Div(id={"type": "add-content", "index": n}),
            Modal(
                id={"type": "modal", "index": n},
                children=[
                    dbc.ModalHeader(dbc.ModalTitle("Header")),
                    ModalBody(
                        [
                            html.Button(
                                "Figure",
                                id={
                                    "type": "btn-option",
                                    "index": n,
                                    "value": "Figure",
                                },
                                n_clicks=0,
                                style={"display": "inline-block"},
                            ),
                            html.Button(
                                "Card",
                                id={"type": "btn-option", "index": n, "value": "Card"},
                                n_clicks=0,
                                style={"display": "inline-block"},
                            ),
                            html.Button(
                                "Interactive",
                                id={
                                    "type": "btn-option",
                                    "index": n,
                                    "value": "Interactive",
                                },
                                n_clicks=0,
                                style={"display": "inline-block"},
                            ),
                        ],
                        id={"type": "modal-body", "index": n},
                        style={
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "center",
                            "flex-direction": "column",
                        },
                    ),
                ],
                is_open=True,
                size="xl",
                backdrop=False,
            ),
        ],
        style={
            "height": "100%",
            "width": "100%",
            "display": "flex",
            "flex-direction": "column",
            "flex-grow": "0",
        },
        id=new_plot_id,
    )

    children.append(new_element)
    new_layout_item = {
        "i": f"{new_plot_id}",
        "x": 10 * ((len(children) + 1) % 2),
        "y": n * 10,
        "w": 6,
        "h": 5,
    }

    # Update the layouts property for both 'lg' and 'sm' sizes
    updated_layouts = {}
    for size in ["lg", "sm"]:
        if size not in layouts:
            layouts[size] = []
        updated_layouts[size] = layouts[size] + [new_layout_item]
    # print(layouts)
    # print(updated_layouts)
    # print(children)
    return children, updated_layouts


# # define the callback to show/hide the modal
# @dash.callback(
#     Output("modal", "is_open"),
#     # [Output({"type": "edit-modal", "index": MATCH}, "is_open")],
#     [Input("edit-button", "n_clicks")],
#     # [
#     #     Input({"type": "edit-button", "index": MATCH}, "n_clicks"),
#     # ],
#     # [State({"type": "edit-modal", "index": MATCH}, "is_open")],
#     [State("modal", "is_open")],
#     prevent_initial_call=True,
# )
# def toggle_modal(n1, is_open):
#     print(n1, is_open)
#     if n1:
#         return not is_open
#     return is_open


# def generate_callback(element_id):
#     @dash.callback(
#         Output(f"stored-{element_id}", "data"),
#         Input("interval", "n_intervals"),
#         State(element_id, "value"),
#     )
#     def save_value(n_intervals, value):
#         if n_intervals == 0:
#             raise dash.exceptions.PreventUpdate
#         return value

#     @dash.callback(
#         Output(element_id, "value"),
#         Input(f"stored-{element_id}", "data"),
#     )
#     def update_value(data):
#         if data is None:
#             raise dash.exceptions.PreventUpdate
#         return data

#     return save_value, update_value


app.layout.children.insert(
    0,
    dcc.Store(id=f"stored-visualization-type", storage_type="session", data="scatter"),
)

# save_value_callback, update_value_callback = generate_callback("visualization-type")


# # Define the callback to update the specific parameters dropdowns
# @dash.callback(
#     [
#         Output("specific-params-container", "children"),
#         # Output({"type": "specific-params-container", "index": MATCH, "value": ALL}, "children"),
#         # Output("offcanvas-state-store", "data"),
#     ],
#     # [Input("visualization-type", "value"), Input("interval", "n_intervals")],
#     [Input("interval", "n_intervals")],
#     # [State("offcanvas-state-store", "data")],
#     prevent_initial_call=True,
# )
# def update_specific_params(n_intervals):
#     # def update_specific_params(n_intervals, offcanvas_states):
#     # def update_specific_params(value, n_intervals, offcanvas_states):
#     # print(value)
#     value = "scatter"
#     if value is not None:
#         specific_params_options = [
#             {"label": param_name, "value": param_name}
#             for param_name in specific_params[value]
#         ]

#         specific_params_dropdowns = list()
#         for e in specific_params[value]:
#             processed_type_tmp = param_info[value][e]["processed_type"]
#             allowed_types = ["str", "int", "float", "column"]
#             if processed_type_tmp in allowed_types:
#                 input_fct = plotly_bootstrap_mapping[processed_type_tmp]
#                 # print(e, input_fct(), processed_type_tmp)
#                 tmp_options = dict()

#                 if processed_type_tmp == "column":
#                     tmp_options = {
#                         "options": list(df.columns),
#                         "value": None,
#                         "persistence": True,
#                         "id": f"{e}",
#                     }
#                 if processed_type_tmp == "str":
#                     tmp_options = {
#                         "placeholder": e,
#                         "type": "text",
#                         "persistence": True,
#                         "id": f"{e}",
#                         "value": None,
#                     }
#                 if processed_type_tmp in ["int", "float"]:
#                     tmp_options = {
#                         "placeholder": e,
#                         "type": "number",
#                         "persistence": True,
#                         "id": f"{e}",
#                         "value": None,
#                     }
#                 input_fct_with_params = input_fct(**tmp_options)
#                 accordion_item = dbc.AccordionItem(
#                     [dbc.Row(input_fct_with_params)],
#                     className="my-2",
#                     title=e,
#                 )
#                 specific_params_dropdowns.append(accordion_item)

#         secondary_common_params_dropdowns = list()
#         for e in secondary_common_params:
#             processed_type_tmp = param_info[value][e]["processed_type"]
#             allowed_types = ["str", "int", "float", "column"]
#             if processed_type_tmp in allowed_types:
#                 input_fct = plotly_bootstrap_mapping[processed_type_tmp]
#                 tmp_options = dict()

#                 if processed_type_tmp == "column":
#                     tmp_options = {
#                         "options": list(df.columns),
#                         "value": None,
#                         "persistence": True,
#                         "id": f"{e}",
#                     }
#                 if processed_type_tmp == "str":
#                     tmp_options = {
#                         "placeholder": e,
#                         "type": "text",
#                         "persistence": True,
#                         "id": f"{e}",
#                         "value": None,
#                     }
#                 if processed_type_tmp in ["int", "float"]:
#                     tmp_options = {
#                         "placeholder": e,
#                         "type": "number",
#                         "persistence": True,
#                         "id": f"{e}",
#                         "value": None,
#                     }
#                 input_fct_with_params = input_fct(**tmp_options)
#                 accordion_item = dbc.AccordionItem(
#                     [dbc.Row(input_fct_with_params)],
#                     className="my-2",
#                     title=e,
#                 )
#                 secondary_common_params_dropdowns.append(accordion_item)

#         secondary_common_params_layout = [html.H5("Common parameters")] + [
#             dbc.Accordion(
#                 secondary_common_params_dropdowns,
#                 flush=True,
#                 always_open=True,
#                 persistence_type="session",
#                 persistence=True,
#                 id="accordion-sec-common",
#             ),
#         ]
#         dynamic_specific_params_layout = [
#             html.H5(f"{value.capitalize()} specific parameters")
#         ] + [
#             dbc.Accordion(
#                 specific_params_dropdowns,
#                 flush=True,
#                 always_open=True,
#                 persistence_type="session",
#                 persistence=True,
#                 id="accordion",
#             ),
#         ]

#         return (
#             secondary_common_params_layout + dynamic_specific_params_layout,
#             # secondary_common_params_layout + dynamic_specific_params_layout,
#         )
#     else:
#         # return html.Div(), html.Div()
#         return html.Div()


def generate_dropdown_ids(value):
    specific_param_ids = [
        f"{value}-{param_name}" for param_name in specific_params[value]
    ]
    secondary_param_ids = [f"{value}-{e}" for e in secondary_common_params]

    return secondary_param_ids + specific_param_ids


@app.callback(
    Output("collapse", "is_open"),
    [Input("edit-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    print(is_open)
    if n is None or n == 0:
        return False
    else:
        return not is_open


# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("edit-button", "n_clicks")],
#     [State("collapse", "is_open")],
#     prevent_initial_call=True,
# )
# def toggle_collapse(n, is_open):
#     print(n, is_open)
#     if n:
#         return not is_open
#     return is_open


# @app.callback(
#     Output({"type": "tmp-container", "index": MATCH}, "children"),
#     [
#         Input({"type": "tmp-x", "index": MATCH}, "value"),
#         Input({"type": "tmp-y", "index": MATCH}, "value"),
#         Input({"type": "tmp-color", "index": MATCH}, "value"),
#     ],
#     # [Input("tmp-x", "value"), Input("tmp-y", "value"), Input("tmp-color", "value")],
#     prevent_initial_call=True,
# )
# def toggle_collapse(x, y, color):
#     return "X: {}, Y: {}, Color: {}".format(x, y, color)


@app.callback(
    Output({"type": "graph", "index": MATCH}, "figure"),
    [
        Input({"type": "tmp-x", "index": MATCH}, "value"),
        Input({"type": "tmp-y", "index": MATCH}, "value"),
        Input({"type": "tmp-color", "index": MATCH}, "value"),
    ],
    prevent_initial_call=True,
)
def update_figure(x, y, color):
    print("X: {}, y: {}, color: {}".format(x, y, color))
    if x or y or color:
        print("TOTO update figure")
        # Your logic here to generate the figure using x, y, and color.
        # This will be triggered by the changes in the dropdowns and the n_clicks of the "Figure" button.
        figure = px.scatter(df, x=x, y=y, color=color)
        return figure


@app.callback(
    Output({"type": "modal-body", "index": MATCH}, "children"),
    # Output({"type": "edit-modal", "index": MATCH}, "children"),
    [Input({"type": "btn-option", "index": MATCH, "value": ALL}, "n_clicks")],
    [
        State({"type": "btn-option", "index": MATCH, "value": ALL}, "id"),
        #  State("visualization-type", "value"),
        # State({"type": "specific-params-container", "index": MATCH, "value": ALL}, "children"),
        # State("specific-params-container", "children"),
    ],
    prevent_initial_call=True,
)
# def update_modal(n_clicks, ids, children_values):
def update_modal(n_clicks, ids):
    # def update_modal(n_clicks, ids, visualization_type, children_values):
    visualization_type = "scatter"
    for n, id in zip(n_clicks, ids):
        if n > 0:
            if id["value"] == "Figure":
                print("TOTO")
                # print(children_values)
                d = dict()
                print("\n")
                print("TATA")
                # if children_values:
                #     for child in children_values[1]["props"]["children"]:
                #         print(
                #             child["props"]["children"][0]["props"]["children"]["props"][
                #                 "id"
                #             ]
                #         )
                #         d[
                #             child["props"]["children"][0]["props"]["children"]["props"][
                #                 "id"
                #             ].replace(f"{visualization_type}-", "")
                #         ] = child["props"]["children"][0]["props"]["children"]["props"][
                #             "value"
                #         ]
                #     print("TOTO2")

                #     for child in children_values[3]["props"]["children"]:
                #         d[
                #             child["props"]["children"][0]["props"]["children"]["props"][
                #                 "id"
                #             ].replace(f"{visualization_type}-", "")
                #         ] = child["props"]["children"][0]["props"]["children"]["props"][
                #             "value"
                #         ]
                #     print("TATA")
                #     print(visualization_type)
                #     print(plotly_vizu_dict)
                # Process inputs and generate the appropriate graph
                plot_func = plotly_vizu_dict[visualization_type]
                print("TATA2")
                plot_kwargs = dict(
                    x=df.columns[0], y=df.columns[1], color=df.columns[2]
                )
                # plot_kwargs = dict(
                #     x=df.columns[0], y=df.columns[1], color=df.columns[2]
                # )
                if d:
                    plot_kwargs = d

                print(plot_func)
                print(plot_kwargs)
                figure = plot_func(
                    df,
                    **plot_kwargs,
                )
                # figure = px.scatter(df, x="gdpPercap", y="lifeExp")
                figure.update_layout(uirevision=1)
                print("TATA3")

                print("TATA4")
                print("idindex: ", str(id["index"]))
                id_index = id["index"]

                return [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=figure,
                                    id={"type": "graph", "index": id["index"]},
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    dbc.Button(
                                        "Edit",
                                        id="edit-button",
                                        # id={"type": "edit-button", "index": f"edit-btn-{id_index}"},
                                        # color="primary",
                                        n_clicks=0,
                                        size="lg",
                                        # style={"font-size": "22px"},
                                    ),
                                    dbc.Collapse(
                                        dbc.Accordion(
                                            [
                                                dbc.AccordionItem(
                                                    dcc.Dropdown(
                                                        options=[
                                                            {"label": e, "value": e}
                                                            for e in list(df.columns)
                                                        ],
                                                        id={
                                                            "type": "tmp-x",
                                                            "index": id["index"],
                                                        },
                                                    ),
                                                    title="x",
                                                ),
                                                dbc.AccordionItem(
                                                    dcc.Dropdown(
                                                        options=[
                                                            {"label": e, "value": e}
                                                            for e in list(df.columns)
                                                        ],
                                                        id={
                                                            "type": "tmp-y",
                                                            "index": id["index"],
                                                        },
                                                    ),
                                                    title="y",
                                                ),
                                                dbc.AccordionItem(
                                                    dcc.Dropdown(
                                                        options=[
                                                            {"label": e, "value": e}
                                                            for e in list(df.columns)
                                                        ],
                                                        id={
                                                            "type": "tmp-color",
                                                            "index": id["index"],
                                                        },
                                                    ),
                                                    title="color",
                                                ),
                                            ],
                                            id="accordion",
                                            flush=True,
                                            always_open=True,
                                            persistence=True,
                                            start_collapsed=True,
                                        ),
                                        # id={"type": "collapse", "index": id["index"]},
                                        id="collapse",
                                        is_open=False,
                                        style={
                                            "height": "100%",
                                            "width": "100%",
                                            "display": "flex",
                                            "flex-direction": "column",
                                            "flex-grow": "0",
                                        },
                                    ),
                                ],
                                width="auto",
                            ),
                        ]
                    ),
                    html.Button(
                        "Done",
                        id={"type": "btn-done", "index": id["index"]},
                        n_clicks=0,
                        style={"display": "block"},
                    ),
                    # dbc.Row(
                    #     [
                    #         dbc.Offcanvas(
                    #             [
                    #                 html.Div(
                    #                     # id="specific-params-container",
                    #                     id={
                    #                         "type": "specific-params-container",
                    #                         "index": id["index"],
                    #                     }
                    #                 ),
                    #             ],
                    #             # id="modal",
                    #             id={"type": "edit-modal", "index": f"edit-modal-{id_index}"},
                    #             title="Edit Menu",
                    #             scrollable=True,
                    #             # size="xl",
                    #             backdrop=False,
                    #         ),
                    #     ],
                    #     justify="center",
                    # ),
                ]
            elif id["value"] == "Card":
                return [
                    html.Div("This is a Card!"),
                    html.Button(
                        "Done",
                        id={"type": "btn-done", "index": id["index"]},
                        n_clicks=0,
                        style={"display": "block"},
                    ),
                ]
            elif id["value"] == "Interactive":
                return [
                    dcc.Input(id="input-box", type="text"),
                    html.Div(id="output-box"),
                    html.Button(
                        "Done",
                        id={"type": "btn-done", "index": id["index"]},
                        n_clicks=0,
                        style={"display": "block"},
                    ),
                ]
    return []


# @app.callback(
#     Output({"type": "modal-body", "index": MATCH}, "children"),
#     [Input({"type": "btn-option", "index": MATCH, "value": ALL}, "n_clicks")],
#     [State({"type": "btn-option", "index": MATCH, "value": ALL}, "id")],
#     prevent_initial_call=True,
# )
# def update_modal(n_clicks, ids):
#     for n, id in zip(n_clicks, ids):
#         if n > 0:
#             if id["value"] == "Figure":
#                 return [
#                     dcc.Graph(
#                         figure=px.scatter(
#                             df,
#                             x="gdpPercap",
#                             y="lifeExp",
#                             animation_frame="year",
#                             animation_group="country",
#                             size="pop",
#                             color="continent",
#                             hover_name="country",
#                             log_x=True,
#                             size_max=55,
#                             range_y=[20, 90],
#                         )
#                     ),
#                     html.Button(
#                         "Done",
#                         id={"type": "btn-done", "index": id["index"]},
#                         n_clicks=0,
#                         style={"display": "block"},
#                     ),
#                 ]
#             elif id["value"] == "Card":
#                 return [
#                     html.Div("This is a Card!"),
#                     html.Button(
#                         "Done",
#                         id={"type": "btn-done", "index": id["index"]},
#                         n_clicks=0,
#                         style={"display": "block"},
#                     ),
#                 ]
#             elif id["value"] == "Interactive":
#                 return [
#                     dcc.Input(id="input-box", type="text"),
#                     html.Div(id="output-box"),
#                     html.Button(
#                         "Done",
#                         id={"type": "btn-done", "index": id["index"]},
#                         n_clicks=0,
#                         style={"display": "block"},
#                     ),
#                 ]
#     # return []


@app.callback(
    Output({"type": "add-content", "index": MATCH}, "children"),
    [Input({"type": "btn-done", "index": MATCH}, "n_clicks")],
    [State({"type": "modal-body", "index": MATCH}, "children")],
    prevent_initial_call=True,
)
def update_button(n_clicks, children):
    # print("\n")
    # print("TITI")
    # print(children)

    if n_clicks > 0:
        return children[:1]
    # return None


if __name__ == "__main__":
    app.run_server(debug=True, port="5080")
