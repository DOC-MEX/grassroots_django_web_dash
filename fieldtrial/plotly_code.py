
import plotly.express as px
import pandas as pd

#import json
#from .grass_plots import get_plot
from .grass_plots import dict_phenotypes
from .grass_plots import numpy_data
from .grass_plots import treatments
from .grass_plots import plotly_plot
#######################################################
def plots_heatmap(uuid, phenotype, study_json):
    #single_study = get_plot(uuid)
    #study_json   = json.loads(single_study)
    studies_ids =[]

    if 'phenotypes' in study_json['results'][0]['results'][0]['data']:
        studies_ids.append(uuid)
        print("Study has phenotypes", studies_ids)


    plot_data         = study_json['results'][0]['results'][0]['data']['plots']
    name              = study_json['results'][0]['results'][0]['data']['so:name']
    treatment_factors = study_json['results'][0]['results'][0]['data']['treatment_factors']
    total_rows        = study_json['results'][0]['results'][0]['data']['num_rows']
    total_columns     = study_json['results'][0]['results'][0]['data']['num_columns']
    phenotypes        = study_json['results'][0]['results'][0]['data']['phenotypes']
    
    phenoHeaders = []
    for key in phenotypes:
        phenoHeaders.append(key)   # for csv file. Includes non-numerical phenotypes

    print("study name :", name)

    dictTraits = dict_phenotypes(phenotypes, plot_data)  #create dictionary of phenotypes keys and their traits
    default    = list(dictTraits.keys())[0]              #use first one as default.

    print (dictTraits[default])

    phenoKeys   = list(dictTraits.keys())
    #phenoValues = list(dictTraits.values())
    #selected_phenotype = default
 
    print("DASH number of phenotypes observations: ", len(phenoKeys))

    matrices  = numpy_data(plot_data, phenotypes, phenotype,
             total_rows, total_columns)

    row     = matrices[0]
    column  = matrices[1]
    row_raw = matrices[2]
    row_acc = matrices[3]
    traitName = matrices[4]
    units     = matrices[5]
    plotID   = matrices[6]

    treatment=[]
    if ( len(treatment_factors)>0):
          treatment = treatments(plot_data, row, column)
          
    #-----------------------CSV--------------------------------------
    #create_CSV(plot_data, phenotypes, treatment_factors, uuid)
    #-----------------------CSV--------------------------------------

    accession  = row_acc.reshape(row,column)    #!! at this point 2D array has not been flipped!
    plotIDs    = plotID.reshape(row,column)
    
    #print("original unflipped accession---: ", np.shape(accession))
    
    figure = plotly_plot(row_raw, accession, traitName, units, plotIDs, treatment)
    del plot_data, matrices, study_json

    return figure

