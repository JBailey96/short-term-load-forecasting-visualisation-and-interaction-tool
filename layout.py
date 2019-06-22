import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from component.graph_control import characteristics_selection
from component.model.regression import regression_model_selection
from data.util.data_characteristics import min_date, max_date
from app import app

app.css.append_css({
    "external_url": "https://use.fontawesome.com/releases/v5.6.3/css/all.css"
})

app.layout = html.Div([
    html.Div([
        html.H4('Visualised:', style={'display': 'inline-block',
                                      'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-day-range',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                display_format='YYYY-MM-DD',
                updatemode='bothdates',
                end_date_placeholder_text='YYYY-MM-DD',
                start_date_placeholder_text='YYYY-MM-DD',
                start_date=max_date,
                day_size=50,
                first_day_of_week=1
            )], style={'padding-right': '5px', 'padding-left': '5px'}),
        dcc.Dropdown(
            id='unit-selection',
            options=[
                {'label': 'Days', 'value': 'Days'},
                {'label': 'Weeks', 'value': 'Weeks'},
                {'label': 'Months (28 days)', 'value': 'Months'},
                {'label': 'Years (364 days)', 'value': 'Years'},
            ],
            value='Days',
            searchable=False,
            clearable=False,
            style={'display': 'inline-block',
                   'width': '15vh', 'vertical-align': 'top', 'padding-right': '5px'}
        ),
        html.Button('+', id='increment', n_clicks_timestamp='0',
                    style={'padding-left': '5px', 'padding-right': '5px'}),
        html.Button('-', id='decrement', n_clicks_timestamp='0',
                    style={'padding-left': '5px'})
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.Div([
        html.H4('Models visualised:', style={'display': 'inline-block',
                                             'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
        dcc.Dropdown(
            id='remove-model-selection',
            options=[],
            searchable=False,
            clearable=False,
            style={'display': 'inline-block',
                   'width': '30vh', 'vertical-align': 'middle', 'padding-right': '5px'}
        ),         html.Button(id='remove-model-button', n_clicks_timestamp='0', className="fa fa-trash", style={'display': 'inline-block', 'font-size': '1.5vw', 'vertical-align': 'middle'})]),
    html.Div([
        html.Details([
            html.Summary('Displacement Models', style={
                     'font-weight': 'bold', 'cursor': 'pointer'}),
            html.Div([
                html.H4('Displaced by:', style={'display': 'inline-block',
                                                'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
                dcc.Input(
                    id='displacement',
                    placeholder=0,
                    type='number',
                    value=0,
                    style={'height': '3vh', 'width': '10vw'}
                ),
                dcc.Dropdown(
                    id='displacement-unit',
                    options=[
                        {'label': 'Half Hours', 'value': 'Half Hours'},
                        {'label': 'Hours', 'value': 'Hours'},
                        {'label': 'Days', 'value': 'Days'},
                        {'label': 'Weeks', 'value': 'Weeks'},
                        {'label': 'Months (28 days)', 'value': 'Months'},
                        {'label': 'Years (364 days)', 'value': 'Years'},
                    ],
                    value='Half Hours',
                    searchable=False,
                    clearable=False,
                    style={'display': 'inline-block',
                           'width': '13vw', 'vertical-align': 'top', 'padding-left': '5px', 'padding-right': '5px'}
                ),
                html.Button('Add Model',
                            id='plot-displacement-button',
                            n_clicks_timestamp='0',
                            style={'display': 'inline-block'})
            ], style={'display': 'flex', 'align-items': 'center', 'height': '35vh'})], style={'width': '50vw'}),
        html.Details([html.Summary('Linear Regression Models', style={
                     'font-weight': 'bold', 'cursor': 'pointer'}),
            html.Div([
                html.Div([
                    html.H4('Selected Model:', style={
                        'display': 'inline-block',
                        'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
                    dcc.Dropdown(
                        id='regression-model-selection',
                        options=regression_model_selection.get_options(),
                        searchable=False,
                        clearable=False,
                        value='None',
                        style={
                            'width': '40vw', 'vertical-align': 'middle', 'padding-right': '5px'}
                    )], style={'display': 'flex', 'align-items': 'center'}),
                html.Div([
                    html.Details([html.Summary('Additional Details', style={'cursor': 'pointer'}),
                                  html.Div([
                                      html.H4('Description:', style={
                                           'display': 'inline-block',
                                           'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
                                      html.Div(id='description-content', style={'word-wrap': 'break-word', 'width': '40vw'})], style={'display': 'flex', 'align-items': 'baseline'}),
                                  html.Div([
                                      html.H4('Variables:', style={
                                          'display': 'inline-block',
                                          'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
                                      html.Div(id='regression-variable-list', style={'word-wrap': 'break-word'})], style={'display': 'flex', 'align-items': 'center'})], style={'display': 'flex', 'align-items': 'center'})]),
                html.Div([
                    html.H4('Training Data:', style={'display': 'inline-block',
                                                     'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
                    html.Div([
                        dcc.DatePickerRange(
                            id='training-data-date-picker-day-range',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            display_format='YYYY-MM-DD',
                            updatemode='bothdates',
                            end_date_placeholder_text='YYYY-MM-DD',
                            start_date_placeholder_text='YYYY-MM-DD',
                            start_date=max_date,
                            end_date=max_date,
                            day_size=50,
                            first_day_of_week=1
                        )])], style={'display': 'flex', 'align-items': 'center'}),
                html.Div([
                    html.H4('Model Name:', style={'display': 'inline-block',
                                                  'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
                    html.Div([
                        dcc.Input(
                            id='regression-model-name',
                            value='',
                            style={'height': '3vh', 'width': '35vw',
                                   'padding-left': '5px', 'padding-right': '5px'}
                        )], style={'padding-right': '5px'}), html.Button('Add Model', id='plot-regression-button',
                                                                         n_clicks_timestamp='0', style={'display': 'inline-block'})], style={'display': 'flex', 'align-items': 'center'})],
            style={'align-items': 'center', 'height': '35vh', 'overflow-y': 'auto'})], style={'width': '50vw'}),
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.Div([
        html.Div([
            html.H4('Highlight points:', style={'display': 'inline-block',
                                                'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
            dcc.Dropdown(
                id='date-highlight-variable-selection',
                options=[
                    {'label': 'None', 'value': 'None'},
                    {'label': 'Year', 'value': 'Year'},
                    {'label': 'Month', 'value': 'Month'},
                    {'label': 'Season', 'value': 'Season'},
                    {'label': 'Day', 'value': 'Day'},
                    {'label': 'Holiday', 'value': 'Holiday'},
                ],
                value='None',
                style={'display': 'inline-block',
                       'width': '20vh', 'vertical-align': 'middle', 'padding-right': '5px'},
                searchable=False
            ),
            dcc.Dropdown(
                id='date-highlight-value-selection',
                options=[
                ],
                value='None',
                style={'display': 'inline-block',
                       'width': '30vh', 'vertical-align': 'middle', 'padding-right': '5px'}
            ),
            dcc.Tabs(id="graph-tabs", value='models', children=[
                dcc.Tab(label='Models Visualisation', value='models', children=[
                    html.Div(id='load-graph', children=[]),
                    html.Div(id='characteristics-graph',
                             children=[])]),
                dcc.Tab(label='Models Error Distribution', value='error', children=[
                    html.Div(id='error-distribution-graph', children=[])
                ]),
            ], style={'width': '98vw', 'height': '7vh'}),
        ], style={'display': 'flex', 'width': '100%', 'align-items': 'center', 'flex-wrap': 'wrap'}),
        html.Div(id='metrics-table-container', children=[
            html.Div([
                    html.H4('Test data', style={'display': 'inline-block',
                                                'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal', 'width': '8vw'}),
                    dcc.DatePickerRange(
                        id='test-data-date-picker-day-range',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        display_format='YYYY-MM-DD',
                        updatemode='bothdates',
                        end_date_placeholder_text='YYYY-MM-DD',
                        start_date_placeholder_text='YYYY-MM-DD',
                        start_date=max_date,
                        day_size=50,
                        first_day_of_week=1
                    )], style={'padding-right': '5px', 'margin-top': '10px'}),
            html.Div(id='visualised-metrics-table', style={'display': 'inline-block', 'padding-right': '10px'})], style={'display': 'none'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-wrap': 'wrap'}),
    html.Div([
        html.H4('Characteristics graph y-axis:', style={'display': 'inline-block',
                                                        'vertical-align': 'middle', 'padding-right': '10px', 'font-weight': 'normal'}),
        dcc.Dropdown(
            id='characteristics-selection',
            options=characteristics_selection.get_options(),
            value='None',
            style={'width': '20vw', 'display': 'inline-block',
                   'vertical-align': 'middle'}
        )
    ], style={'padding-left': '10px', 'float': 'right'}),
    html.Div(id='models', children=[], style={'display': 'none'})
])
