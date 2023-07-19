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


# Set up Dash app with Bootstrap CSS and additional CSS file
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "custom.css"],
    suppress_callback_exceptions=True,
)

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)
print(df)

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


app.layout = dbc.Container(
    [
        dcc.Interval(
            id="interval",
            interval=2000,  # Save slider value every 1 second
            n_intervals=0,
        ),
        dcc.Store(id="selections-store", storage_type="session", data={}),
        html.H1(
            "Prepare your visualization",
            className="text-center mb-4",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(html.H5("Visualization type"), width=2),
                dbc.Col(
                    dcc.Dropdown(
                        id="visualization-type",
                        options=[
                            {"label": func.__name__, "value": func.__name__}
                            for func in plotly_vizu_list
                        ],
                        value=plotly_vizu_list[0].__name__,
                    ),
                    width=4,
                ),
                html.Hr(),
                dbc.Col(
                    [
                        dbc.Button(
                            "Edit",
                            id="edit-button",
                            color="primary",
                            size="lg",
                            style={"font-size": "22px"},
                        ),
                    ],
                    className="d-flex justify-content-center align-items-center",
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(id="graph-container", config={"editable": True}),
                        ),
                    ],
                    className="mt-3",
                ),
            ],
            className="text-center mt-3",
            justify="center",
        ),
        html.Hr(),
        html.Tr(),
        dbc.Row(
            [
                dcc.Store("offcanvas-state-store", storage_type="session"),
                dbc.Offcanvas(
                    [
                        html.Div(id="specific-params-container"),
                    ],
                    id="modal",
                    title="Edit Menu",
                    scrollable=True,
                    # size="xl",
                    backdrop=False,
                ),
            ],
            justify="center",
        ),
    ],
    fluid=False,
)



# define the callback to show/hide the modal
@dash.callback(
    Output("modal", "is_open"),
    [Input("edit-button", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, is_open):
    print(n1, is_open)
    if n1:
        return not is_open
    return is_open



def generate_callback(element_id):
    @dash.callback(
        Output(f"stored-{element_id}", "data"),
        Input("interval", "n_intervals"),
        State(element_id, "value"),
    )
    def save_value(n_intervals, value):
        if n_intervals == 0:
            raise dash.exceptions.PreventUpdate
        return value

    @dash.callback(
        Output(element_id, "value"),
        Input(f"stored-{element_id}", "data"),
    )
    def update_value(data):
        if data is None:
            raise dash.exceptions.PreventUpdate
        return data

    return save_value, update_value


app.layout.children.insert(
    0,
    dcc.Store(id=f"stored-visualization-type", storage_type="session", data="scatter"),
)

save_value_callback, update_value_callback = generate_callback("visualization-type")


# Define the callback to update the specific parameters dropdowns
@dash.callback(
    [
        Output("specific-params-container", "children"),
        Output("offcanvas-state-store", "data"),
    ],
    [Input("visualization-type", "value"), Input("interval", "n_intervals")],
    [State("offcanvas-state-store", "data")],
)
def update_specific_params(value, n_intervals, offcanvas_states):
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
                # print(e, input_fct(), processed_type_tmp)
                tmp_options = dict()

                if processed_type_tmp == "column":
                    tmp_options = {
                        "options": list(df.columns),
                        "value": None,
                        "persistence": True,
                        "id": f"{e}",
                    }
                if processed_type_tmp == "str":
                    tmp_options = {
                        "placeholder": e,
                        "type": "text",
                        "persistence": True,
                        "id": f"{e}",
                        "value": None,
                    }
                if processed_type_tmp in ["int", "float"]:
                    tmp_options = {
                        "placeholder": e,
                        "type": "number",
                        "persistence": True,
                        "id": f"{e}",
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
            allowed_types = ["str", "int", "float", "column"]
            if processed_type_tmp in allowed_types:
                input_fct = plotly_bootstrap_mapping[processed_type_tmp]
                tmp_options = dict()

                if processed_type_tmp == "column":
                    tmp_options = {
                        "options": list(df.columns),
                        "value": None,
                        "persistence": True,
                        "id": f"{e}",
                    }
                if processed_type_tmp == "str":
                    tmp_options = {
                        "placeholder": e,
                        "type": "text",
                        "persistence": True,
                        "id": f"{e}",
                        "value": None,
                    }
                if processed_type_tmp in ["int", "float"]:
                    tmp_options = {
                        "placeholder": e,
                        "type": "number",
                        "persistence": True,
                        "id": f"{e}",
                        "value": None,
                    }
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

        return (
            secondary_common_params_layout + dynamic_specific_params_layout,
            secondary_common_params_layout + dynamic_specific_params_layout,
        )
    else:
        return html.Div(), html.Div()


def generate_dropdown_ids(value):
    specific_param_ids = [
        f"{value}-{param_name}" for param_name in specific_params[value]
    ]
    secondary_param_ids = [f"{value}-{e}" for e in secondary_common_params]

    return secondary_param_ids + specific_param_ids


@dash.callback(
    Output("graph-container", "figure"),
    [
        Input("visualization-type", "value"),
        Input("specific-params-container", "children"),
    ],
)
def update_graph(
    visualization_type,
    *children_values,
):

    d = dict()
    print("\nTOTO")
    print(children_values)
    print('\n')
    print("TATA")
    print(children_values[1])
    for child in children_values[0][1]["props"]["children"]:
        print(child["props"]["children"][0]["props"]["children"]["props"]["id"])
        d[
            child["props"]["children"][0]["props"]["children"]["props"]["id"].replace(
                f"{visualization_type}-", ""
            )
        ] = child["props"]["children"][0]["props"]["children"]["props"]["value"]
    for child in children_values[0][3]["props"]["children"]:
        d[
            child["props"]["children"][0]["props"]["children"]["props"]["id"].replace(
                f"{visualization_type}-", ""
            )
        ] = child["props"]["children"][0]["props"]["children"]["props"]["value"]

    # Process inputs and generate the appropriate graph
    plot_func = plotly_vizu_dict[visualization_type]
    plot_kwargs = {}

    plot_kwargs = d

    print(plot_func)
    print(plot_kwargs)
    figure = plot_func(
        df,
        **plot_kwargs,
    )
    figure.update_layout(uirevision=1)

    return figure


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
