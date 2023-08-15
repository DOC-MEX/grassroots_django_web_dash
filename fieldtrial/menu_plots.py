import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc      
from dash.exceptions import PreventUpdate
import json

from .grass_plots import get_plot
from .grass_plots import dict_phenotypes

from .plotly_code import plots_heatmap

from django_plotly_dash import DjangoDash

app = DjangoDash('menu_plots')   # replaces dash.Dash

#########################################################
app.layout = html.Div(children=[
    #html.Div(children=[
    dbc.Row(
      dbc.Col(
          html.Label(['Select phenotype:'],style={'font-weight': 'bold', "text-align": "left"})  
      ),

    ),# Row 1
    dbc.Row(
      dbc.Col(
        dcc.Dropdown( id='MENU1',
              options = [],
              #value   = 'SpkPop_CalcGbSamp_m2', 
              searchable = True,
              style={'width':"80%"}
        ),
      ),
    ),# Row 2
    
    #]),
    dcc.Graph(id='HEATMAP'),
    html.Br(),
    dcc.Store(id='STUDY'),

    dcc.RadioItems(
        id='uuid',        
        value='test'
        ),

])
#########################################################


##############DROPDOWN MENU ###########################################
@app.callback(
    [Output('MENU1', 'options'),
     Output('MENU1', 'value'), 
     Output('STUDY', 'data') ],   # Store study to avoid unnecessary calls to the server
    [Input('uuid', 'value')])     # get in from the initial_arguments generated in the views.py

def get_phenotypes(uuid):
    #print("uuid-------->", uuid)
    #print("type-------->", type(uuid))   check that initial argument was passed succesfully

    if uuid is None:
        raise PreventUpdate

    single_study = get_plot(uuid)
    study_json   = json.loads(single_study)

    studies_ids =[]

    if 'phenotypes' in study_json['results'][0]['results'][0]['data']:
        studies_ids.append(uuid)        

    plot_data         = study_json['results'][0]['results'][0]['data']['plots']
    phenotypes        = study_json['results'][0]['results'][0]['data']['phenotypes']

    dictTraits = dict_phenotypes(phenotypes, plot_data)  

    phenoKeys   = list(dictTraits.keys())
    phenoValues = list(dictTraits.values())

    options = [{'label': phenoValues[i], 'value':phenoKeys[i]} for i in range(len(phenoKeys))]
    value   = list(dictTraits.keys())[0]    
    
    return options, value, study_json


##############HEATMAP PLOT###########################################
@app.callback(        
    Output('HEATMAP', 'figure'),
    [Input('MENU1', 'value'),  # phenotype selected from the dropdown menu
    Input('uuid', 'value'),
    Input('STUDY', 'data')])   # study stored in the Store component 
def create_heatmap(menu_selection, uuid, study):
    
    if menu_selection is None:
        raise PreventUpdate
    
    figure = plots_heatmap(uuid, menu_selection, study)
    
    return figure
    
