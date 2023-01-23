import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, dash_table
from datetime import date
import numpy as np
import plotly.graph_objects as go

app = Dash(__name__)

# upload data
# df = pd.read_csv("/Users/chancock/PycharmProjects/udot/venv/data_files/data-19-22.csv", low_memory=False)
# df = pd.read_csv("venv/data_files/data-19-22.csv", low_memory=False)
df = pd.read_csv("data-19-22.csv", low_memory=False)

activity_list = df.ACTIVITY_CD.sort_values(ascending=True).unique()
activity_type_list = ['Scoping', 'Geometry', 'Plans-in-Hand', 'PS&E', 'Advertising', 'Post-Advertising', 'Other']
discipline_list = ['AERONAUTICS SERVICES',
                   'ASSET MANAGEMENT',
                   'BRIDGE MANAGEMENT - BRIDGE INSPECTION',
                   'BRIDGE MANAGEMENT - PLANNING & PROGRAMMING',
                   'BRIDGE MANAGEMENT & ASSET MANAGEMENT',
                   'CONST SERVICES - CONSTRUCTABILITY REVIEW SERVICES',
                   'CONST SERVICES - INDEPENDENT COST ESTIMATING',
                   'CONST SERVICES - TRAINING',
                   'CONSTRUCTION ENGINEERING MANAGEMENT',
                   'DRAINAGE DESIGN',
                   'ENVIRONMENTAL - AIR QUALITY',
                   'ENVIRONMENTAL - ARCHAEOLOGY & PALEONTOLOGY',
                   'ENVIRONMENTAL - ARCHITECTURAL HISTORIAN',
                   'ENVIRONMENTAL - BIOLOGICAL & WILDLIFE',
                   'ENVIRONMENTAL - NOISE',
                   'ENVIRONMENTAL - WETLANDS & OTHER WATERS',
                   'ENVIRONMENTAL DOCUMENT PREPARATION',
                   'GEOGRAPHIC INFORMATION SYSTEMS (GIS)',
                   'GEOTECHNICAL',
                   'HAZ MAT,  WASTE ASSESSMENT &  REMEDIATION',
                   'HYDRAULIC DESIGN',
                   'ITS - CONSTRUCTION INSPECTION',
                   'ITS - INSTALLATION, TESTING & INTEG OF FIELD EQUIP',
                   'ITS - PROJECT DEVELOPMENT, DESIGN & OVERSIGHT',
                   'LANDSCAPE ARCHITECTURE',
                   'MATERIALS TESTING',
                   'PLANNING',
                   'PRECONSTRUCTION ENGINEERING',
                   'PROGRAM ASSISTANCE AND OVERSIGHT FOR CM/GC AND D/B',
                   'PROJECT MANAGEMENT',
                   'PUBLIC INVOLVEMENT',
                   'RESEARCH',
                   'RIGHT OF WAY ENGINEERING',
                   'ROW ACQUISITION SERVICES',
                   'ROW APPRAISAL REVIEW SERVICES',
                   'ROW APPRAISAL SERVICES, COMPLEX',
                   'ROW CELL TOWER & OTHER WIRELESS COM. LEASING',
                   'ROW LEAD AGENT SERVICES, COMPLEX',
                   'ROW LEAD AGENT SERVICES, NON-COMPLEX',
                   'ROW PROJECT COORDINATION SERVICES',
                   'ROW RELOCATION SERVICES, NON-RESIDENTIAL',
                   'ROW RELOCATION SERVICES, RESIDENTIAL',
                   'ROW TITLE/CLOSING SERVICES',
                   'SPECIALIZED SERVICES',
                   'STRUCTURAL DESIGN ENGINEER',
                   'STRUCTURES DESIGN',
                   'SUB-SURFACE UTILITY ENGINEERING',
                   'SURVEYING SERVICES - AERIAL PHOTOGRAMETRY',
                   'SURVEYING SERVICES - SURVEYING & MAPPING',
                   'TRAFFIC DATA',
                   'TRAFFIC SIGNALS & ROADWAY LIGHTING DESIGN',
                   'TRANSIT AND RAILWAY DESIGN',
                   'UTILITY COORDINATION',
                   'VE & RISK ANALYSIS - VALUE ENGINEERING']
selection_type_list = ['CM/GC RFP',
                       'GE / LG POOL RPLOQ',
                       'GE / LG POOL RPLOQ (2016-2019)',
                       'GE / LG POOL SMALL PURCHASE',
                       'LETTER OF INTEREST SOLICITATIO',
                       'PI POOL (DS) (2013-2016)',
                       'PI POOL (DS) (2016-2019)',
                       'PI POOL (RPLOQ) (2013-2016)',
                       'PI POOL RPLOQ (2016-2019)',
                       'POOL - GE / LG',
                       'POOL - GE / LG (DIRECT SELECT)',
                       'POOL - OTHER',
                       'PUBLIC INVOLVEMENT RFP',
                       'ROW ACQUISITION SOLICITATION',
                       'ROW POOL (DIRECT SELECT)',
                       'ROW POOL SMALL PURCHASE',
                       'STANDARD RFQ UNLIMITED',
                       'STREAMLINED SOLICITATION']

# transform data
# df_activity = df.groupby(['ACTIVITY_CD', 'CONTRACT_HDR_SEQ_NO'], as_index=False)['ACTIVITY_BURDENED_LABOR', 'ACTIVITY_HOURS'].sum()
df_activity = df.groupby(['ACTIVITY_CD', 'CONTRACT_HDR_SEQ_NO', 'ACTIVITY_PHASE_NAME', 'DISCIPLINE_DESC', 'SEL_METHOD_DESC'],
           as_index=False)['ACTIVITY_BURDENED_LABOR', 'ACTIVITY_HOURS'].sum()
df_activity['HOURLY_RATE'] = df_activity['ACTIVITY_BURDENED_LABOR'] / df_activity['ACTIVITY_HOURS']
print(df_activity)

app.layout = html.Div([
    html.Header(
        children=[
            html.Img(src='https://udottraffic.utah.gov/images/hdr/UDOT_Logo_CMYK2014-1.png', style={'maxWidth': '25%'}),
            html.H1('Contract Sizing Tool', style={
                'paddingLeft': '40px',
                'fontsize': '70px',
                'color': '#EF7720',
                'fontFamily': 'arial',
                'margin': '25px',
                'fontSize': '60px'
            })
        ],
        style={'display': 'flex',
               'flexDirection': 'row',
               'paddingLeft': '30px',
               'paddingBottom': '20px',
               'alignItems': 'center'
               }
    ),
    html.Div(
        id='filter-container',
        style={
            'fontSize': '16px',
            'fontFamily': 'arial',
            'display': 'flex',
            'flexDirection': 'row',
            'backgroundColor': 'lightgray',
            'border': '1px solid darkgray',
            'width': '100%',
            'alignItems': 'center',
            'marginBottom': '20px',
            'justifyContent': 'space-evenly',
            'display': 'none'
        },
        children=[
            html.Div(
                id='dropdown-container',
                className='dropdown=container',
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'maxWidth': '60%',
                    'marginTop': '10px',
                    'marginBottom': '10px'
                },
                children=[
                    html.Div(
                        className='filter-section',
                        style={
                            'display': 'flex',
                            'flexDirection': 'row',
                            'alignItems': 'center'
                        },
                        children=[
                            html.P(
                                'Select an activity:',
                                style={
                                    'minWidth': '116px',
                                    'paddingRight': '20px',
                                    'fontWeight': 600,
                                    'textAlign': 'right',
                                    'fontSize': '24px'
                                }
                            ),
                            dcc.Dropdown(
                                activity_list,
                                id='activity-dropdown',
                                multi=False,
                                value='03M',
                                placeholder='Activity list',
                                style={
                                    'width': '400px',
                                    'fontSize': '18px'
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    ),
    html.Div(
        'Activity Contract Data',
        style={
            'display': 'flex',
            'paddingRight': '30px',
            'paddingLeft': '30px',
            'backgroundColor': 'rgb(239, 119, 32)',
            'color': 'rgb(255,255,255)',
            'fontFamily': 'arial',
            'padding-top': '10px',
            'padding-bottom': '10px'
        }
    ),
    html.Div(
        id='viz-row',
        className='viz-row',
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'maxHeight': '1500px',
            'minHeight': '550px',
            'width': '100%',
            'fontFamily': 'arial',
            'borderBottom': '1px solid lightgray',
            'justifyContent': 'center'
        },
        children=[
            html.Div(
                id='summary-data',
                style={
                    'minWidth': '350px',
                    'width': '20%',
                    'borderRight': '1px solid gray',
                    'backgroundColor': '#E5ECF6',
                    'paddingTop': '20px',
                    'textAlign': 'center',
                    'borderBottom': '1px solid lightgray'
                },
                children=[
                    html.H4('Data Filters'
                            , style={
                            'paddingTop': '0px'
                        }
                            ),
                    dcc.Dropdown(
                        activity_list,
                        id='activity-code-dropdown',
                        multi=False,
                        # value = '03M',
                        placeholder='Activity Code',
                        style={
                            'width': '300px',
                            'fontSize': '12px',
                            'paddingLeft': '25px',
                            'marginBottom': '20px'
                        }
                    ),
                    dcc.Dropdown(
                        activity_type_list,
                        id='activity-type-dropdown',
                        multi=False,
                        # value = '03M',
                        placeholder='Activity Type',
                        style={
                            'width': '300px',
                            'fontSize': '12px',
                            'paddingLeft': '25px',
                            'marginBottom': '20px'
                        }
                    ),
                    dcc.Dropdown(
                        discipline_list,
                        id='discipline-dropdown',
                        multi=False,
                        # value = '03M',
                        placeholder='Discipline',
                        style={
                            'width': '300px',
                            'fontSize': '12px',
                            'paddingLeft': '25px',
                            'marginBottom': '20px'
                        }
                    ),
                    dcc.Dropdown(
                        selection_type_list,
                        id='selection-type-dropdown',
                        multi=False,
                        # value = '03M',
                        placeholder='Selection Method',
                        style={
                            'width': '300px',
                            'fontSize': '12px',
                            'paddingLeft': '25px'
                        }
                    ),
                    html.H4('Proposed Values'
                            , style={
                            'paddingTop': '25px',
                            'borderTop': '1px solid lightgray'
                        }
                            ),
                    html.H4('Cost'
                            , style={
                            'fontSize': '12px'
                        }
                            ),
                    dcc.Input(
                        id="costInput",
                        type="number",
                        placeholder="Enter proposed cost here",
                        style={
                            'width': '280px',
                            'border': '1px solid lightgray',
                            'height': '34px',
                            'color': 'black',
                            'borderRadius': '5px',
                            'paddingLeft': '20px'
                        }
                    ),
                    html.H4('Hours'
                            , style={
                            'fontSize': '12px'
                        }
                            ),
                    dcc.Input(
                        id="hoursInput",
                        type="number",
                        placeholder="Enter proposed hours here",
                        style={
                            'width': '280px',
                            'border': '1px solid lightgray',
                            'height': '34px',
                            'color': 'black',
                            'borderRadius': '5px',
                            'paddingLeft': '20px'
                        }
                    ),
                    html.Button('Compare',
                                id='submit-val',
                                n_clicks=0,
                                style={
                                    'marginTop': '20px',
                                    'backgroundColor': 'rgb(90,134,200)',
                                    'color': 'white',
                                    'height': '34px'
                                }
                                ),
                    html.H4('Contracts Analyzed'
                            , style={
                            'paddingTop': '25px',
                            'borderTop': '1px solid lightgray'
                        }
                            ),
                    html.P(id='summary-contracts'),
                    html.P(id='summary-warning'
                           , style={'color': 'red',
                                    'fontSize': '12px',
                                    'paddingRight': '10px',
                                    'paddingLeft': '10px'}
                           )
                ]
            ),
            dcc.Graph(
                id="activity-graph",
                style={
                    # 'maxHeight': '1500px',
                    'paddingRight': '30px',
                    'paddingLeft': '20px',
                    'width': '85%'
                },
                figure={},
                config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['zoomIn2D', 'zoomOut2d'],
                }
            )
        ]
    ),
    html.Footer(
        id='footer',
        className='footer',
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'width': '100%',
            'paddingLeft': '30px'
        },
        children=[
            html.P('Created by Elevated Consulting Group')
        ]
    )
],
    style={
        'minWidth': '1350px'
    }
)


@app.callback(
    Output('summary-contracts', 'children'),
    Output('summary-warning', 'children'),
    Output('activity-graph', 'figure'),
    Input('activity-code-dropdown', 'value'),
    Input('activity-type-dropdown', 'value'),
    Input('discipline-dropdown', 'value'),
    Input('selection-type-dropdown', 'value'),
    Input('submit-val', 'n_clicks'),
    State('costInput', 'value'),
    State('hoursInput', 'value')
)
def build_graph(activity, activity_type, discipline, selection_type, n_clicks, costValue, hoursValue):
    print()
    print(activity)
    print(activity_type)
    print(discipline)
    print(selection_type)
    print(n_clicks)

    dff = df_activity
    if activity is not None:
        dff = dff[(dff['ACTIVITY_CD'] == activity)]
        print(dff)
    else:
        pass

    if activity_type is not None:
        dff = dff[(dff['ACTIVITY_PHASE_NAME'] == activity_type)]
        print(dff)
    else:
        pass

    if discipline is not None:
        dff = dff[(dff['DISCIPLINE_DESC'] == discipline)]
        print(dff)
    else:
        pass

    if selection_type is not None:
        dff = dff[(dff['SEL_METHOD_DESC'] == selection_type)]
        print(dff)
    else:
        pass

    unique_contracts = dff['CONTRACT_HDR_SEQ_NO'].nunique()

    if unique_contracts > 0:
        # create the statistical measures
        rate_median = dff['HOURLY_RATE'].median()
        rate_q1 = dff['HOURLY_RATE'].quantile(0.25)
        rate_q3 = dff['HOURLY_RATE'].quantile(0.75)
        iqr = rate_q3 - rate_q1

        max_hours = dff['ACTIVITY_HOURS'].max()
        hour_list = [*range(0, max_hours + 15, 1)]
        rate_upper = rate_median + (iqr * 1.5)
        rate_lower = rate_median - (iqr * 1.5)

        print('IQR: ' + str(iqr))
        print('median: ' + str(rate_median))
        print('Upper Bound: ' + str(rate_upper))
        print('Lower Bound: ' + str(rate_lower))

        string_uniques = str(unique_contracts)
        print(string_uniques)

        sample_warning = "Warning: Data based on low contract volume."
        if unique_contracts > 3:
            sample_warning = ""

        activity_plot = px.scatter(dff,
                                   y='ACTIVITY_BURDENED_LABOR',
                                   x='ACTIVITY_HOURS',
                                   hover_name='CONTRACT_HDR_SEQ_NO',
                                   # hover_data=dff.columns,
                                   hover_data=['ACTIVITY_HOURS', 'ACTIVITY_BURDENED_LABOR'],
                                   title='Historical Contract Data',
                                   ).update_layout(xaxis_title='ACTIVITY CONTRACT HOURS',
                                                   yaxis_title='ACTIVITY CONTRACT COST',
                                                   yaxis_tickprefix='$')

        # add the statistical data lines
        activity_plot.add_trace(
            go.Scatter(
                x=hour_list,
                y=rate_median * np.array(hour_list),
                mode="lines",
                hovertemplate='Contract Cost: $%{y:.2d}' + '<br>Total Hours: %{x}',
                name='Median Rate',
                line=go.scatter.Line(color='blue', dash='3px'),
                showlegend=False)
        )

        activity_plot.add_trace(
            go.Scatter(
                x=hour_list,
                y=np.array(hour_list) * (rate_upper),
                mode="lines",
                hovertemplate='Contract Cost: $%{y:.2d}' + '<br>Total Hours: %{x}',
                name='Upper Limit Rate',
                line=go.scatter.Line(color='red', dash='2px'),
                showlegend=False)
        )

        activity_plot.add_trace(
            go.Scatter(
                x=hour_list,
                y=np.array(hour_list) * (rate_lower),
                mode="lines",
                hovertemplate='Contract Cost: $%{y:.2d}' + '<br>Total Hours: %{x}',
                name='Lower Limit Rate',
                line=go.scatter.Line(color='green', dash='2px'),
                showlegend=False)
        )

        activity_plot.add_trace(
            go.Scatter(
                x=[hoursValue],
                y=[costValue],
                hovertemplate='Contract Cost: $%{y:.2d}' + '<br>Total Hours: %{x}',
                name='Proposal Comparison',
                mode='markers',
                marker=go.scatter.Marker(color="orange", size=12),
                showlegend=False)
        )
    else:
        activity_plot = px.scatter(dff,
                                   y='ACTIVITY_BURDENED_LABOR',
                                   x='ACTIVITY_HOURS',
                                   hover_name='CONTRACT_HDR_SEQ_NO',
                                   # hover_data=dff.columns,
                                   hover_data=['ACTIVITY_HOURS', 'ACTIVITY_BURDENED_LABOR'],
                                   title='Historical Contract Data',
                                   ).update_layout(xaxis_title='ACTIVITY CONTRACT HOURS',
                                                   yaxis_title='ACTIVITY CONTRACT COST',
                                                   yaxis_tickprefix='$')

        sample_warning = "Warning: No contracts meet the criteria."
        string_uniques = str(unique_contracts)

    return string_uniques, sample_warning, activity_plot


if __name__ == '__main__':
    app.run_server(debug=True)

