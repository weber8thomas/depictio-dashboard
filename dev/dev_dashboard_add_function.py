from dash import html, dcc, Input, Output, State, ALL, MATCH
from dash_bootstrap_components import Modal, ModalBody, Button
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash

import plotly.express as px
import pandas as pd

import dash_draggable

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://use.fontawesome.com/releases/v5.7.2/css/all.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
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

# print(common_params)
# print(common_params_names)
# print(specific_params)

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
    "list": dcc.Dropdown,
}

# Identify the parameters not in the dropdown elements
secondary_common_params = [
    e
    for e in common_params_names[1:]
    # e for e in common_params_names[1:] if e not in dropdown_elements
]
secondary_common_params_lite = [
    e
    for e in secondary_common_params
    if e
    not in [
        "category_orders",
        "color_discrete_sequence",
        "color_discrete_map",
        "log_x",
        "log_y",
        "labels",
        "range_x",
        "range_y",
    ]
]
# print(secondary_common_params)
# print("\n")


init_layout = dict()
init_children = list()
app.layout = html.Div(
    [
        html.H1("Dash Draggable"),
        dmc.Button(
            "Add",
            id="add-button",
            size="xl",
            radius="xl",
            variant="gradient",
            n_clicks=0,
        ),
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
                dcc.Interval(
                    id="interval",
                    interval=2000,  # Save slider value every 1 second
                    n_intervals=0,
                ),
                # dcc.Store(id="selections-store", storage_type="session", data={}),
            ],
            fluid=False,
        ),
        html.Div(id="output-container"),
        html.Div(id="output-container2"),
    ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


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
    print("add_new_div")
    # print(app._callback_list)

    print("index: {}".format(n))
    new_plot_id = f"graph-{n}"
    print(new_plot_id)

    new_element = html.Div(
        [
            html.Div(id={"type": "add-content", "index": n}),
            dbc.Modal(
                id={"type": "modal", "index": n},
                children=[
                    dbc.ModalHeader(html.H5("Chose your new component type")),
                    dbc.ModalBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dmc.Button(
                                            "Figure",
                                            id={
                                                "type": "btn-option",
                                                "index": n,
                                                "value": "Figure",
                                            },
                                            n_clicks=0,
                                            style={"display": "inline-block"},
                                            size="xl",
                                            color="grape",
                                        )
                                    ),
                                    dbc.Col(
                                        dmc.Button(
                                            "Card",
                                            id={
                                                "type": "btn-option",
                                                "index": n,
                                                "value": "Card",
                                            },
                                            n_clicks=0,
                                            style={"display": "inline-block"},
                                            size="xl",
                                            color="violet",
                                        )
                                    ),
                                    dbc.Col(
                                        dmc.Button(
                                            "Interactive",
                                            id={
                                                "type": "btn-option",
                                                "index": n,
                                                "value": "Interactive",
                                            },
                                            n_clicks=0,
                                            style={"display": "inline-block"},
                                            size="xl",
                                            color="indigo",
                                        )
                                    ),
                                ]
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
    return children, updated_layouts


# Define the callback to update the specific parameters dropdowns
@dash.callback(
    [
        Output({"type": "collapse", "index": MATCH}, "children"),
    ],
    [Input({"type": "edit-button", "index": MATCH}, "n_clicks")],
    [State({"type": "edit-button", "index": MATCH}, "id")],
    # prevent_initial_call=True,
)
def update_specific_params(n_clicks, edit_button_id):
    print("update_specific_params")
    # print(app._callback_list)

    print(n_clicks, edit_button_id)

    value = "scatter"
    if value is not None:
        specific_params_options = [
            {"label": param_name, "value": param_name}
            for param_name in specific_params[value]
        ]

        specific_params_dropdowns = list()
        for e in specific_params[value]:
            processed_type_tmp = param_info[value][e]["processed_type"]
            allowed_types = ["str", "int", "float", "column"]
            if processed_type_tmp in allowed_types:
                input_fct = plotly_bootstrap_mapping[processed_type_tmp]
                tmp_options = dict()

                if processed_type_tmp == "column":
                    tmp_options = {
                        "options": list(df.columns),
                        "value": None,
                        "persistence": True,
                        "id": {
                            "type": f"tmp-{e}",
                            "index": edit_button_id["index"],
                        },
                    }
                if processed_type_tmp == "str":
                    tmp_options = {
                        "placeholder": e,
                        "type": "text",
                        "persistence": True,
                        "id": {
                            "type": f"tmp-{e}",
                            "index": edit_button_id["index"],
                        },
                        "value": None,
                    }
                if processed_type_tmp in ["int", "float"]:
                    tmp_options = {
                        "placeholder": e,
                        "type": "number",
                        "persistence": True,
                        "id": {
                            "type": f"tmp-{e}",
                            "index": edit_button_id["index"],
                        },
                        "value": None,
                    }
                input_fct_with_params = input_fct(**tmp_options)
                accordion_item = dbc.AccordionItem(
                    [dbc.Row(input_fct_with_params)],
                    className="my-2",
                    title=e,
                )
                specific_params_dropdowns.append(accordion_item)

        secondary_common_params_dropdowns = list()
        for e in secondary_common_params:
            processed_type_tmp = param_info[value][e]["processed_type"]
            # allowed_types = ["str", "int", "float", "column", "list"]
            allowed_types = ["str", "int", "float", "column"]
            if processed_type_tmp in allowed_types:
                input_fct = plotly_bootstrap_mapping[processed_type_tmp]
                tmp_options = dict()

                if processed_type_tmp == "column":
                    tmp_options = {
                        "options": list(df.columns),
                        "value": None,
                        "persistence": True,
                        "id": {
                            "type": f"tmp-{e}",
                            "index": edit_button_id["index"],
                        },
                    }
                if processed_type_tmp == "str":
                    tmp_options = {
                        "placeholder": e,
                        "type": "text",
                        "persistence": True,
                        "id": {
                            "type": f"tmp-{e}",
                            "index": edit_button_id["index"],
                        },
                        "value": None,
                    }
                if processed_type_tmp in ["int", "float"]:
                    tmp_options = {
                        "placeholder": e,
                        "type": "number",
                        "persistence": True,
                        "id": {
                            "type": f"tmp-{e}",
                            "index": edit_button_id["index"],
                        },
                        "value": None,
                    }

                # if processed_type_tmp is "list":
                #     tmp_options = {
                #         # "options": list(df.columns),
                #         # "value": None,
                #         "persistence": True,
                #         "id": {
                #             "type": f"tmp-{e}",
                #             "index": edit_button_id["index"],
                #         },
                #     }

                input_fct_with_params = input_fct(**tmp_options)
                accordion_item = dbc.AccordionItem(
                    [dbc.Row(input_fct_with_params)],
                    className="my-2",
                    title=e,
                )
                secondary_common_params_dropdowns.append(accordion_item)

        secondary_common_params_layout = [html.H5("Common parameters")] + [
            dbc.Accordion(
                secondary_common_params_dropdowns,
                flush=True,
                always_open=True,
                persistence_type="session",
                persistence=True,
                id="accordion-sec-common",
            ),
        ]
        dynamic_specific_params_layout = [
            html.H5(f"{value.capitalize()} specific parameters")
        ] + [
            dbc.Accordion(
                specific_params_dropdowns,
                flush=True,
                always_open=True,
                persistence_type="session",
                persistence=True,
                id="accordion",
            ),
        ]
        return [secondary_common_params_layout + dynamic_specific_params_layout]
    else:
        return html.Div()


def generate_dropdown_ids(value):
    specific_param_ids = [
        f"{value}-{param_name}" for param_name in specific_params[value]
    ]
    secondary_param_ids = [f"{value}-{e}" for e in secondary_common_params]

    return secondary_param_ids + specific_param_ids


@app.callback(
    Output(
        {
            "type": "collapse",
            "index": MATCH,
        },
        "is_open",
    ),
    [
        Input(
            {
                "type": "edit-button",
                "index": MATCH,
            },
            "n_clicks",
        )
    ],
    [
        State(
            {
                "type": "collapse",
                "index": MATCH,
            },
            "is_open",
        )
    ],
    prevent_initial_call=True,
)
def toggle_collapse(n, is_open):
    print(n, is_open, n % 2 == 0)
    if n % 2 == 0:
        return False
    else:
        return True


@app.callback(
    Output({"type": "dict_kwargs", "index": MATCH}, "value"),
    [
        Input({"type": "collapse", "index": MATCH}, "children"),
        Input("interval", "n_intervals"),
    ],
    [State({"type": "dict_kwargs", "index": MATCH}, "data")],
    # prevent_initial_call=True,
)
def get_values_to_generate_kwargs(*args):
    print("get_values_to_generate_kwargs")
    # print(args)
    print("\n")

    children = args[0]
    existing_kwargs = args[-1]
    print(existing_kwargs)

    if children:
        accordion_secondary_common_params = children[1]["props"]["children"]
        if accordion_secondary_common_params:
            print("TOTO")
            accordion_secondary_common_params = [
                param["props"]["children"][0]["props"]["children"]
                for param in accordion_secondary_common_params
            ]

            accordion_secondary_common_params_args = {
                elem["props"]["id"]["type"].replace("tmp-", ""): elem["props"]["value"]
                for elem in accordion_secondary_common_params
            }
            if not {k: v for k, v in accordion_secondary_common_params_args.items() if v is not None}:
                accordion_secondary_common_params_args = {**accordion_secondary_common_params_args, **existing_kwargs}
            print(accordion_secondary_common_params)
            return accordion_secondary_common_params_args
        else:
            return existing_kwargs
    else:
        return existing_kwargs

        # accordion_specific_params = args[0][3]


@app.callback(
    Output({"type": "graph", "index": MATCH}, "figure"),
    [
        Input({"type": "dict_kwargs", "index": MATCH}, "value"),
        [
            Input({"type": f"tmp-{e}", "index": MATCH}, "children")
            for e in secondary_common_params_lite
        ],
        Input("interval", "n_intervals"),
    ],
    # prevent_initial_call=True,
)
def update_figure(*args):
    dict_kwargs = args[0]
    print("update figure")
    print(dict_kwargs)
    # # print(app._callback_list)

    # print(dict_kwargs)
    dict_kwargs = {k: v for k, v in dict_kwargs.items() if v is not None}
    print(dict_kwargs)
    if dict_kwargs:
        figure = px.scatter(df, **dict_kwargs)
        return figure
    print("\n")

    # accordion_specific_params = args[0][3]


@app.callback(
    Output({"type": "modal-body", "index": MATCH}, "children"),
    [Input({"type": "btn-option", "index": MATCH, "value": ALL}, "n_clicks")],
    [
        State({"type": "btn-option", "index": MATCH, "value": ALL}, "id"),
    ],
    prevent_initial_call=True,
)
def update_modal(n_clicks, ids):
    print("update_modal")
    print(n_clicks, ids)
    print("\n")

    visualization_type = "scatter"
    for n, id in zip(n_clicks, ids):
        print(n, id)
        if n > 0:
            if id["value"] == "Figure":
                plot_func = plotly_vizu_dict[visualization_type]
                plot_kwargs = dict(
                    x=df.columns[0], y=df.columns[1], color=df.columns[2]
                )


                figure = plot_func(
                    df,
                    **plot_kwargs,
                )
                figure.update_layout(uirevision=1)

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
                            # dbc.Col(width=0.5),
                            dbc.Col(
                                [
                                    html.Div(
                                        children=[
                                            dmc.Button(
                                                "Edit",
                                                id={
                                                    "type": "edit-button",
                                                    "index": id["index"],
                                                },
                                                n_clicks=0,
                                                size="lg",
                                            ),
                                            dbc.Collapse(
                                                id={
                                                    "type": "collapse",
                                                    "index": id["index"],
                                                },
                                                is_open=False,
                                            ),
                                        ]
                                    )
                                ],
                                width="auto",
                            ),
                        ]
                    ),
                    html.Hr(),
                    dmc.Button(
                        "Done",
                        id={"type": "btn-done", "index": id["index"]},
                        n_clicks=0,
                        style={"display": "block"},
                    ),
                    dcc.Store(id={"type": "dict_kwargs", "index": id["index"]}, data=plot_kwargs, storage_type="session"),
                ]
            elif id["value"] == "Card":
                print("Card")
                return [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dmc.TextInput(
                                                label="Card title",
                                                id={
                                                    "type": "card-input",
                                                    "index": id["index"],
                                                },
                                            ),
                                            dmc.Select(
                                                label="Select your column",
                                                id={
                                                    "type": "card-dropdown-column",
                                                    "index": id["index"],
                                                },
                                                data=[
                                                    {"label": e, "value": e}
                                                    for e in df.columns
                                                ],
                                                value=None,
                                            ),
                                            dmc.Select(
                                                label="Select your aggregation method",
                                                id={
                                                    "type": "card-dropdown-aggregation",
                                                    "index": id["index"],
                                                },
                                                data=[
                                                    {"label": e, "value": e}
                                                    for e in [
                                                        "average",
                                                        "median",
                                                        "sum",
                                                    ]
                                                ],
                                                value=None,
                                            ),
                                        ],
                                    ),
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        id={"type": "card-body", "index": id["index"]}
                                    )
                                ),
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
                ]
            elif id["value"] == "Interactive":
                return [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Input(
                                    # id="input-box",
                                    type="text",
                                    id={"type": "input", "index": id["index"]},
                                )
                            )
                        ]
                    ),
                    html.Button(
                        "Done",
                        id={"type": "btn-done", "index": id["index"]},
                        n_clicks=0,
                        style={"display": "block"},
                    ),
                ]
    return []


@app.callback(
    Output({"type": "card-body", "index": MATCH}, "children"),
    [
        Input({"type": "card-input", "index": MATCH}, "value"),
        Input({"type": "card-dropdown-column", "index": MATCH}, "value"),
        Input({"type": "card-dropdown-aggregation", "index": MATCH}, "value"),
    ],
    prevent_initial_call=True,
)
def update_card_body(input_value, column_value, aggregation_value):
    if input_value is None or column_value is None or aggregation_value is None:
        return []
    # This function is called whenever the input_value or dropdown_value changes
    # Do something with input_value and dropdown_value to generate new card_body
    v = df[column_value].nunique(aggregation_value)
    new_card_body = [html.H5(f"{input_value}"), html.P(f"{v}")]

    # You can return anything you want here, as long as it's a valid Dash component or a list of Dash components
    return new_card_body


@app.callback(
    Output({"type": "add-content", "index": MATCH}, "children"),
    [
        Input({"type": "btn-done", "index": MATCH}, "n_clicks"),
    ],
    [
        State({"type": "modal-body", "index": MATCH}, "children"),
        State({"type": "btn-done", "index": MATCH}, "id"),
    ],
    prevent_initial_call=True,
)
def update_button(n_clicks, children, btn_id):
    print("update_button")
    print(n_clicks, btn_id)
    print("\n")

    if n_clicks > 0:
        # print(children)
        # figure = children[0]["props"]["children"][0]["props"]["children"]["props"]["figure"]
        # print(children)
        child = children[0]["props"]["children"][0]["props"]["children"] # Figure
        # child = children[0]["props"]["children"][1]["props"]["children"] # Card
        # print(list(child["props"].keys()))
        # print(child_id)
        # child = children[0]["props"]["children"][0]["props"]["children"]["props"]["children"]
        # print(child)  
        # if child["props"]["type"] is not "Card":
        child["props"]["id"]["type"] = "updated-" + child["props"]["id"]["type"] # Figure
        # else:
        #     child["props"]["children"]["type"] = (
        #         "updated-" + child["props"]["id"]["type"]
        #     )

        # print(child)
        # # print(figure)
        return child
        # return dcc.Graph(
        #     figure=figure, id={"type": "graph", "index": btn_id["index"]}
        # )


if __name__ == "__main__":
    app.run_server(debug=True, port="5080")
