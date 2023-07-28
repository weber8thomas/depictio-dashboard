# Import necessary libraries
import numpy as np
from dash import html, dcc, Input, Output, State, ALL, MATCH
import dash
import dash_bootstrap_components as dbc
import dash_draggable
import dash_mantine_components as dmc
import inspect
import pandas as pd
import plotly.express as px
import re

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


agg_functions = {
    "int64": {
        "title": "Integer",
        "input_methods": {
            "Slider" : {
                "mantine": dmc.Slider,
                "description": "Single value slider",
            },
            "RangeSlider" : {
                "mantine": dmc.RangeSlider,
                "description": "Two values slider",
            },
        },
        "card_methods": {
            "count": {
                "pandas": "count",
                "numpy": "count_nonzero",
                "description": "Counts the number of non-NA cells",
            },
            "unique": {
                "pandas": "nunique",
                "numpy": None,
                "description": "Number of distinct elements",
            },
            "sum": {
                "pandas": "sum",
                "numpy": "sum",
                "description": "Sum of non-NA values",
            },
            "average": {
                "pandas": "mean",
                "numpy": "mean",
                "description": "Mean of non-NA values",
            },
            "median": {
                "pandas": "median",
                "numpy": "median",
                "description": "Arithmetic median of non-NA values",
            },
            "min": {
                "pandas": "min",
                "numpy": "min",
                "description": "Minimum of non-NA values",
            },
            "max": {
                "pandas": "max",
                "numpy": "max",
                "description": "Maximum of non-NA values",
            },
            "range": {
                "pandas": lambda df: df.max() - df.min(),
                "numpy": "ptp",
                "description": "Range of non-NA values",
            },
            "variance": {
                "pandas": "var",
                "numpy": "var",
                "description": "Variance of non-NA values",
            },
            "std_dev": {
                "pandas": "std",
                "numpy": "std",
                "description": "Standard Deviation of non-NA values",
            },
            "percentile": {
                "pandas": "quantile",
                "numpy": "percentile",
                "description": "Percentiles of non-NA values",
            },
            "skewness": {
                "pandas": "skew",
                "numpy": None,
                "description": "Skewness of non-NA values",
            },
            "kurtosis": {
                "pandas": "kurt",
                "numpy": None,
                "description": "Kurtosis of non-NA values",
            },
            "cumulative_sum": {
                "pandas": "cumsum",
                "numpy": "cumsum",
                "description": "Cumulative sum of non-NA values",
            },
        },
    },
    "float64": {
        "title": "Floating Point",
        "input_methods": {
            "Slider" : {
                "mantine": dmc.Slider,
                "description": "Single value slider",
            },
            "RangeSlider" : {
                "mantine": dmc.RangeSlider,
                "description": "Two values slider",
            },
        },
        "card_methods": {
            "count": {
                "pandas": "count",
                "numpy": "count_nonzero",
                "description": "Counts the number of non-NA cells",
            },
            "unique": {
                "pandas": "nunique",
                "numpy": None,
                "description": "Number of distinct elements",
            },
            "sum": {
                "pandas": "sum",
                "numpy": "sum",
                "description": "Sum of non-NA values",
            },
            "average": {
                "pandas": "mean",
                "numpy": "mean",
                "description": "Mean of non-NA values",
            },
            "median": {
                "pandas": "median",
                "numpy": "median",
                "description": "Arithmetic median of non-NA values",
            },
            "min": {
                "pandas": "min",
                "numpy": "min",
                "description": "Minimum of non-NA values",
            },
            "max": {
                "pandas": "max",
                "numpy": "max",
                "description": "Maximum of non-NA values",
            },
            "range": {
                "pandas": lambda df: df.max() - df.min(),
                "numpy": "ptp",
                "description": "Range of non-NA values",
            },
            "variance": {
                "pandas": "var",
                "numpy": "var",
                "description": "Variance of non-NA values",
            },
            "std_dev": {
                "pandas": "std",
                "numpy": "std",
                "description": "Standard Deviation of non-NA values",
            },
            "percentile": {
                "pandas": "quantile",
                "numpy": "percentile",
                "description": "Percentiles of non-NA values",
            },
            "skewness": {
                "pandas": "skew",
                "numpy": None,
                "description": "Skewness of non-NA values",
            },
            "kurtosis": {
                "pandas": "kurt",
                "numpy": None,
                "description": "Kurtosis of non-NA values",
            },
            "cumulative_sum": {
                "pandas": "cumsum",
                "numpy": "cumsum",
                "description": "Cumulative sum of non-NA values",
            },
        },
    },
    "bool": {
        "title": "Boolean",
        "description": "Boolean values",
        "input_methods": {
            "Checkbox" : {
                "mantine": dmc.Checkbox,
                "description": "Checkbox",
            },
            "Switch" : {
                "mantine": dmc.Switch,
                "description": "Switch",
            },
        },
        "card_methods": {
            "count": {
                "pandas": "count",
                "numpy": "count_nonzero",
                "description": "Counts the number of non-NA cells",
            },
            "sum": {
                "pandas": "sum",
                "numpy": "sum",
                "description": "Sum of non-NA values",
            },
            "min": {
                "pandas": "min",
                "numpy": "min",
                "description": "Minimum of non-NA values",
            },
            "max": {
                "pandas": "max",
                "numpy": "max",
                "description": "Maximum of non-NA values",
            },
        },
    },
    "datetime": {
        "title": "Datetime",
        "description": "Date and time values",
        "card_methods": {
            "count": {
                "pandas": "count",
                "numpy": "count_nonzero",
                "description": "Counts the number of non-NA cells",
            },
            "min": {
                "pandas": "min",
                "numpy": "min",
                "description": "Minimum of non-NA values",
            },
            "max": {
                "pandas": "max",
                "numpy": "max",
                "description": "Maximum of non-NA values",
            },
        },
    },
    "timedelta": {
        "title": "Timedelta",
        "description": "Differences between two datetimes",
        "card_methods": {
            "count": {
                "pandas": "count",
                "numpy": "count_nonzero",
                "description": "Counts the number of non-NA cells",
            },
            "sum": {
                "pandas": "sum",
                "numpy": "sum",
                "description": "Sum of non-NA values",
            },
            "min": {
                "pandas": "min",
                "numpy": "min",
                "description": "Minimum of non-NA values",
            },
            "max": {
                "pandas": "max",
                "numpy": "max",
                "description": "Maximum of non-NA values",
            },
        },
    },
    "category": {
        "title": "Category",
        "description": "Finite list of text values",
        "card_methods": {
            "count": {
                "pandas": "count",
                "numpy": "count_nonzero",
                "description": "Counts the number of non-NA cells",
            },
            "mode": {
                "pandas": "mode",
                "numpy": None,
                "description": "Most common value",
            },
        },
    },
    "object": {
        "title": "Object",
        "input_methods": {
            "TextInput" : {
                "mantine": dmc.TextInput,
                "description": "Text input box",
            },
            "Select" : {
                "mantine": dmc.Select,
                "description": "Select",
            },
            "MultiSelect" : {
                "mantine": dmc.MultiSelect,
                "description": "MultiSelect",
            },
            "SegmentedControl" : {
                "mantine": dmc.SegmentedControl,
                "description": "SegmentedControl",
            },
        },
        "description": "Text or mixed numeric or non-numeric values",
        "card_methods": {
            "count": {
                "pandas": "count",
                "numpy": "count_nonzero",
                "description": "Counts the number of non-NA cells",
            },
            "mode": {
                "pandas": "mode",
                "numpy": None,
                "description": "Most common value",
            },
            "nunique": {
                "pandas": "nunique",
                "numpy": None,
                "description": "Number of distinct elements",
            },
        },
    },
}


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
                            "height": "100%",
                            "width": "100%",
                        },
                    ),
                ],
                is_open=True,
                size="xl",
                backdrop=False,
                style={
                    "height": "100%",
                    "width": "100%",
                    # "display": "flex",
                    # "flex-direction": "column",
                    # "flex-grow": "0",
                },
            ),
        ],
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
            if not {
                k: v
                for k, v in accordion_secondary_common_params_args.items()
                if v is not None
            }:
                accordion_secondary_common_params_args = {
                    **accordion_secondary_common_params_args,
                    **existing_kwargs,
                }
            # print(accordion_secondary_common_params)
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
                    dcc.Store(
                        id={"type": "dict_kwargs", "index": id["index"]},
                        data=plot_kwargs,
                        storage_type="session",
                    ),
                ]
            elif id["value"] == "Card":
                print("Card")
                return [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H5("Card edit menu"),
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
                                                    value=None,
                                                ),
                                                html.Div(
                                                    id={
                                                        "type": "debug-print",
                                                        "index": id["index"],
                                                    },
                                                ),
                                            ],
                                        ),
                                        id={
                                            "type": "card",
                                            "index": id["index"],
                                        },
                                    ),
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    html.H5("Resulting card"),
                                    dbc.Card(
                                        dbc.CardBody(
                                            id={
                                                "type": "card-body",
                                                "index": id["index"],
                                            }
                                        )
                                    ),
                                ],
                                width="auto",
                            ),
                        ]
                    ),
                    html.Hr(),
                    dbc.Row(
                        dmc.Button(
                            "Done",
                            id={"type": "btn-done", "index": id["index"]},
                            n_clicks=0,
                            style={"display": "block"},
                        )
                    ),
                ]
            elif id["value"] == "Interactive":
                print("Interactive")
                return [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H5("Card edit menu"),
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dmc.TextInput(
                                                    label="Card title",
                                                    id={
                                                        "type": "input-title",
                                                        "index": id["index"],
                                                    },
                                                ),
                                                dmc.Select(
                                                    label="Select your column",
                                                    id={
                                                        "type": "input-dropdown-column",
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
                                                        "type": "input-dropdown-method",
                                                        "index": id["index"],
                                                    },
                                                    value=None,
                                                ),
                                            ],
                                        ),
                                        id={
                                            "type": "input",
                                            "index": id["index"],
                                        },
                                    ),
                                ],
                                width="auto",
                            ),
                            dbc.Col(
                                [
                                    html.H5("Resulting card"),
                                    dbc.Card(
                                        dbc.CardBody(
                                            id={
                                                "type": "input-body",
                                                "index": id["index"],
                                            }
                                        )
                                    color="light",
                                    ),
                                ],
                                width="auto",
                            ),
                        ]
                    ),
                    html.Hr(),
                    dbc.Row(
                        dmc.Button(
                            "Done",
                            id={"type": "btn-done", "index": id["index"]},
                            n_clicks=0,
                            style={"display": "block"},
                        )
                    ),
                ]
    return []


# Callback to update aggregation dropdown options based on the selected column
@app.callback(
    Output({"type": "input-dropdown-method", "index": MATCH}, "data"),
    Input({"type": "input-dropdown-column", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def update_aggregation_options(column_value):
    if column_value is None:
        return []

    # Get the type of the selected column
    column_type = df[column_value].dtype
    print(column_value, column_type, type(column_type))

    if column_type in ["object", "category"]:
        nb_unique = df[column_value].nunique()
    else:
        nb_unique = 0

    # Get the aggregation functions available for the selected column type
    agg_functions_tmp_methods = agg_functions[str(column_type)]["input_methods"]
    print(agg_functions_tmp_methods)

    # Create a list of options for the dropdown
    options = [{"label": k, "value": k} for k in agg_functions_tmp_methods.keys()]
    print(options)

    if nb_unique > 5:
        options = [e for e in options if e["label"] != "SegmentedControl"]

    return options


# Callback to reset aggregation dropdown value based on the selected column
@app.callback(
    Output({"type": "input-dropdown-method", "index": MATCH}, "value"),
    Input({"type": "input-dropdown-column", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def reset_aggregation_value(column_value):
    return None


# Callback to update card body based on the selected column and aggregation
@app.callback(
    Output({"type": "input-body", "index": MATCH}, "children"),
    [
        Input({"type": "input-title", "index": MATCH}, "value"),
        Input({"type": "input-dropdown-column", "index": MATCH}, "value"),
        Input({"type": "input-dropdown-method", "index": MATCH}, "value"),
        # Input("interval", "n_intervals"),
    ],
    prevent_initial_call=True,
)
def update_card_body(input_value, column_value, aggregation_value):
    if input_value is None or column_value is None or aggregation_value is None:
        return []

    # Get the type of the selected column
    column_type = str(df[column_value].dtype)

    # Get the pandas function for the selected aggregation
    func_name = agg_functions[column_type]["input_methods"][aggregation_value]["mantine"]
    print(func_name)

    # if callable(func_name):
    #     # If the function is a lambda function
    #     v = func_name(df[column_value])
    # else:
    #     # If the function is a pandas function
    #     v = getattr(df[column_value], func_name)()
    #     print(v, type(v))
    #     if type(v) is pd.core.series.Series and func_name != "mode":
    #         v = v.iloc[0]
    #     elif type(v) is pd.core.series.Series and func_name == "mode":
    #         if v.shape[0] == df[column_value].nunique():
    #             v = "All values are represented equally"
    #         else:
    #             v = v.iloc[0]

    # if type(v) is np.float64:
    #     v = round(v, 2)
        # v = "{:,.2f}".format(round(v, 2))
        # v = "{:,.2f}".format(round(v, 2)).replace(",", " ")

    card_title = html.H5(f"{input_value}")

    if aggregation_value  in  ["Select", "MultiSelect", "SegmentedControl"]:
        data = df[column_value].unique()

        new_card_body = [card_title, func_name(data=data)]
        print(new_card_body)

        return new_card_body

    elif aggregation_value in ["Slider", "RangeSlider"]:
        min_value = df[column_value].min()
        max_value = df[column_value].max()
        new_card_body = [card_title, func_name(min=min_value, max=max_value)]
        print(new_card_body)
        return new_card_body

# Callback to update aggregation dropdown options based on the selected column
@app.callback(
    Output({"type": "card-dropdown-aggregation", "index": MATCH}, "data"),
    Input({"type": "card-dropdown-column", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def update_aggregation_options(column_value):
    if column_value is None:
        return []

    # Get the type of the selected column
    column_type = df[column_value].dtype
    print(column_value, column_type, type(column_type))

    # Get the aggregation functions available for the selected column type
    agg_functions_tmp_methods = agg_functions[str(column_type)]["card_methods"]
    print(agg_functions_tmp_methods)

    # Create a list of options for the dropdown
    options = [{"label": k, "value": k} for k in agg_functions_tmp_methods.keys()]
    print(options)

    return options


# Callback to reset aggregation dropdown value based on the selected column
@app.callback(
    Output({"type": "card-dropdown-aggregation", "index": MATCH}, "value"),
    Input({"type": "card-dropdown-column", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def reset_aggregation_value(column_value):
    return None


# Callback to update card body based on the selected column and aggregation
@app.callback(
    Output({"type": "card-body", "index": MATCH}, "children"),
    [
        Input({"type": "card-input", "index": MATCH}, "value"),
        Input({"type": "card-dropdown-column", "index": MATCH}, "value"),
        Input({"type": "card-dropdown-aggregation", "index": MATCH}, "value"),
        # Input("interval", "n_intervals"),
    ],
    prevent_initial_call=True,
)
def update_card_body(input_value, column_value, aggregation_value):
    if input_value is None or column_value is None or aggregation_value is None:
        return []

    # Get the type of the selected column
    column_type = str(df[column_value].dtype)

    # Get the pandas function for the selected aggregation
    func_name = agg_functions[column_type]["card_methods"][aggregation_value]["pandas"]

    if callable(func_name):
        # If the function is a lambda function
        v = func_name(df[column_value])
    else:
        # If the function is a pandas function
        v = getattr(df[column_value], func_name)()
        print(v, type(v))
        if type(v) is pd.core.series.Series and func_name != "mode":
            v = v.iloc[0]
        elif type(v) is pd.core.series.Series and func_name == "mode":
            if v.shape[0] == df[column_value].nunique():
                v = "All values are represented equally"
            else:
                v = v.iloc[0]

    if type(v) is np.float64:
        v = round(v, 2)
        # v = "{:,.2f}".format(round(v, 2))
        # v = "{:,.2f}".format(round(v, 2)).replace(",", " ")


    new_card_body = [html.H5(f"{input_value}"), html.P(f"{v}")]

    return new_card_body


def find_ids_recursive(dash_component):
    """
    Recursively search for ids in the properties of a Dash component.
    :param dash_component: The Dash component to search in
    :return: A list of all ids found
    """
    if isinstance(dash_component, dict) and "props" in dash_component:
        # print(f"Inspecting {dash_component.get('type')}")
        if "id" in dash_component["props"]:
            id = dash_component["props"]["id"]
            # print(f"Found id: {id}")
            yield id
        if "children" in dash_component["props"]:
            children = dash_component["props"]["children"]
            if isinstance(children, list):
                for child in children:
                    yield from find_ids_recursive(child)
            elif isinstance(children, dict):
                yield from find_ids_recursive(children)


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

    # print(f"Inspecting children:")
    box_type = [sub_e for e in children for sub_e in list(find_ids_recursive(e))][0][
        "type"
    ]
    print(box_type)
    # print(f"Found ids: {all_ids}")

    if box_type == "graph":
        child = children[0]["props"]["children"][0]["props"]["children"]  # Figure
        child["props"]["id"]["type"] = (
            "updated-" + child["props"]["id"]["type"]
        )  # Figure

        print("OK")
        return child
    elif box_type == "card":
        print(children)
        child = children[0]["props"]["children"][1]["props"]["children"][1]  # Card
        print(child)
        child["props"]["children"]["props"]["id"]["type"] = (
            "updated-" + child["props"]["children"]["props"]["id"]["type"]
        )  # Figure
        return child
    elif box_type == "input":
        print(children)
        child = children[0]["props"]["children"][1]["props"]["children"][1]  # Card
        print(child)
        child["props"]["children"]["props"]["id"]["type"] = (
            "updated-" + child["props"]["children"]["props"]["id"]["type"]
        )  # Figure
        return child
    # elif box_type == "input":
    #     child = children[0]["props"]["children"][1]["props"]["children"] # Card
    #     print(child)
    #     child["props"]["children"]["props"]["id"]["type"] = "updated-" + child["props"]["children"]["props"]["id"]["type"] # Figure
    #     return child

    else:
        return html.Div()

    # print("\nEND")

    # if n_clicks > 0:
    #     # print(children)
    #     # figure = children[0]["props"]["children"][0]["props"]["children"]["props"]["figure"]
    #     # print(children)
    #     # print(list(child["props"].keys()))
    #     # print(child_id)
    #     # child = children[0]["props"]["children"][0]["props"]["children"]["props"]["children"]
    #     # print(child)
    #     # if child["props"]["type"] is not "Card":
    #     # else:
    #     #     child["props"]["children"]["type"] = (
    #     #         "updated-" + child["props"]["id"]["type"]
    #     #     )

    #     # print(child)
    #     # # print(figure)
    #     # return dcc.Graph(
    #     #     figure=figure, id={"type": "graph", "index": btn_id["index"]}
    #     # )


if __name__ == "__main__":
    app.run_server(debug=True, port="5080")
