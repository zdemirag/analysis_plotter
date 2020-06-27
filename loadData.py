#! /usr/bin/env python
from ROOT import *
import csv
import re

lumi = 1.0

# Dictionaries for aesthetic details
labels = {
    'Zvv_HT.*'  : 'QCD Z#rightarrow#nu#nu',
    'EWKZvv.*'  : 'EWK Z#rightarrow#nu#nu',
    'Wlv_HT.*'  : 'QCD W#rightarrow l #nu',
    'EWKWlv.*'  : 'EWK W#rightarrow l #nu',
    'Zll_HT.*'  : 'QCD Z#rightarrow l l',
    'EWKZll.*'  : 'EWK Z#rightarrow l l',
}

process_ht_bins = {
    'Zvv' : [100, 200, 400, 600, 800, 1200, 2500],
    'Wlv' : [100, 200, 400, 600, 800, 1200, 2500],
    'Zll' : [70, 100, 200, 400, 600, 800, 1200, 2500]
}

# The CSV file containing XS + sumw information for every MC
csv_file = '/afs/cern.ch/work/a/aakpinar/public/forZeynep/VBF_trees/csv/xs_sumw.csv'

def get_data_from_csv(csv_file):
    '''Load data from the input CSV file: XS+sumw for each MC'''
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        # Construct the dataset --> xs/sumw map
        d = {row[0] : float(row[1])/float(row[2]) for row in reader if 'Dataset' not in row}
    return d

scale_map = get_data_from_csv(csv_file)

dataDir = "/afs/cern.ch/work/a/aakpinar/public/forZeynep/VBF_trees/"

physics_processes = {}
for process, ht_bins in process_ht_bins.items():
    for ht_bin in ht_bins:
        process_tag = '{}_HT{}'.format(process, ht_bin)
        # Set relevant information for this particular process
        physics_processes[process_tag] = {'datacard' : process}

physics_processes = {
        # QCD Znunu processes
        'Zvv_HT100'         : { 'label'   : 'QCD Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : scale_map['ZJetsToNuNu_HT-100To200-mg_2017'],
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-100To200-mg_2017.root"],
                                },
        'Zvv_HT200'         : { 'label'   : 'QCD Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : scale_map['ZJetsToNuNu_HT-200To400-mg_2017'],
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-200To400-mg_2017.root"],
                                },
        'Zvv_HT400'         : { 'label'   : 'QCD Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : scale_map['ZJetsToNuNu_HT-400To600-mg_new_pmx_2017'],
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-400To600-mg_new_pmx_2017.root"],
                                },
        'Zvv_HT600'         : { 'label'   : 'QCD Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : scale_map['ZJetsToNuNu_HT-600To800-mg_new_pmx_2017'],
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-600To800-mg_new_pmx_2017.root"],
                                },
        'Zvv_HT800'         : { 'label'   : 'QCD Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : scale_map['ZJetsToNuNu_HT-800To1200-mg_2017'],
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-800To1200-mg_2017.root"],
                                },
        'Zvv_HT1200'        : { 'label'   : 'QCD Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : scale_map['ZJetsToNuNu_HT-1200To2500-mg_new_pmx_2017'],
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-1200To2500-mg_new_pmx_2017.root"],
                                },
        'Zvv_HT2500'        : { 'label'   : 'QCD Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : scale_map['ZJetsToNuNu_HT-2500ToInf-mg_2017'],
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-2500ToInf-mg_2017.root"],
                                },
        # EWK Znunu processes
        'EWKZvv'            : { 'label'   : 'EWK Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 5,
                                'xsec'    : scale_map['EWKZ2Jets_ZToNuNu-mg_new_pmx_2017'],
                                'files'   : [dataDir+"tree_EWKZ2Jets_ZToNuNu-mg_new_pmx_2017.root"],
                                },
        # QCD Wlnu processes
        'Wlv_HT100'         : { 'label'   : 'QCD W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 6,
                                'xsec'    : scale_map['WJetsToLNu_HT-100To200-MLM_2017'],
                                'files'   : [dataDir+"tree_WJetsToLNu_HT-100To200-MLM_2017.root"],
                                },
        'Wlv_HT200'         : { 'label'   : 'QCD W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 6,
                                'xsec'    : scale_map['WJetsToLNu_HT-200To400-MLM_2017'],
                                'files'   : [dataDir+"tree_WJetsToLNu_HT-200To400-MLM_2017.root"],
                                },
        'Wlv_HT400'         : { 'label'   : 'QCD W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 6,
                                'xsec'    : scale_map['WJetsToLNu_HT-400To600-MLM_2017'],
                                'files'   : [dataDir+"tree_WJetsToLNu_HT-400To600-MLM_2017.root"],
                                },
        'Wlv_HT600'         : { 'label'   : 'QCD W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 6,
                                'xsec'    : scale_map['WJetsToLNu_HT-600To800-MLM_2017'],
                                'files'   : [dataDir+"tree_WJetsToLNu_HT-600To800-MLM_2017.root"],
                                },
        'Wlv_HT800'         : { 'label'   : 'QCD W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 6,
                                'xsec'    : scale_map['WJetsToLNu_HT-800To1200-MLM_2017'],
                                'files'   : [dataDir+"tree_WJetsToLNu_HT-800To1200-MLM_2017.root"],
                                },
        'Wlv_HT1200'        : { 'label'   : 'QCD W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 6,
                                'xsec'    : scale_map['WJetsToLNu_HT-1200To2500-MLM_2017'],
                                'files'   : [dataDir+"tree_WJetsToLNu_HT-1200To2500-MLM_2017.root"],
                                },
        'Wlv_HT2500'        : { 'label'   : 'QCD W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 6,
                                'xsec'    : scale_map['WJetsToLNu_HT-2500ToInf-MLM_2017'],
                                'files'   : [dataDir+"tree_WJetsToLNu_HT-2500ToInf-MLM_2017.root"],
                                },
        # EWK Wlv processes
        'EWKWpluslv'        : { 'label'   : 'EWK W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 4,
                                'xsec'    : scale_map['EWKWPlus2Jets_WToLNu_M-50-mg_new_pmx_2017'],
                                'files'   : [dataDir+"tree_EWKWPlus2Jets_WToLNu_M-50-mg_new_pmx_2017.root"],
                                },
        'EWKWminuslv'       : { 'label'   : 'EWK W#rightarrow l #nu', 
                                'datacard': 'Wlv', 
                                'color'   : "#E6E6FA",
                                'ordering': 4,
                                'xsec'    : scale_map['EWKWMinus2Jets_WToLNu_M-50-mg_new_pmx_2017'],
                                'files'   : [dataDir+"tree_EWKWMinus2Jets_WToLNu_M-50-mg_new_pmx_2017.root"],
                                },
        # QCD DY processes
        'Zll_HT70'          : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-70to100-MLM_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-70to100-MLM_2017.root"]
                                },
        'Zll_HT100'         : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-100to200-MLM_new_pmx_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-100to200-MLM_new_pmx_2017.root"] 
                                },
        'Zll_HT100_ext1'    : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-100to200-MLM_ext1_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-100to200-MLM_ext1_2017.root"] 
                                },
        'Zll_HT200'         : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-200to400-MLM_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-200to400-MLM_2017.root"]
                                },
        'Zll_HT200_ext1'    : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-200to400-MLM_ext1_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-200to400-MLM_ext1_2017.root"]
                                },
        'Zll_HT400'         : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-400to600-MLM_new_pmx_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-400to600-MLM_new_pmx_2017.root"]
                                },
        'Zll_HT400_ext1'    : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-400to600-MLM_ext1_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-400to600-MLM_ext1_2017.root"]
                                },
        'Zll_HT600'         : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-600to800-MLM_new_pmx_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-600to800-MLM_new_pmx_2017.root"]
                                },
        'Zll_HT800'         : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-800to1200-MLM_new_pmx_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-800to1200-MLM_new_pmx_2017.root"]
                                },
        'Zll_HT1200'        : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-1200to2500-MLM_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-1200to2500-MLM_2017.root"]
                                },
        'Zll_HT2500'        : { 'label'   : 'QCD Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 3,
                                'xsec'    : scale_map['DYJetsToLL_M-50_HT-2500toInf-MLM_new_pmx_2017'],
                                'files'   : [dataDir+"tree_DYJetsToLL_M-50_HT-2500toInf-MLM_new_pmx_2017.root"]
                                },
        # EWK Zll processes
        'EWKZll'            : { 'label'   : 'EWK Z#rightarrow l l', 
                                'datacard': 'Zll', 
                                'color'   : "#F08080",
                                'ordering': 2,
                                'xsec'    : scale_map['EWKZ2Jets_ZToLL_M-50-mg_new_pmx_2017'],
                                'files'   : [dataDir+"tree_EWKZ2Jets_ZToLL_M-50-mg_new_pmx_2017.root"],
                                },

        'data'              : { 'label':'Data',
                                'datacard':'data',
                                'color': 1,
                                'ordering': 8,    
                                'xsec' : 1.0,  # No scaling to data                
                                'files':[dataDir+'tree_MET_2017B.root',
                                         dataDir+'tree_MET_2017C.root',                  
                                         dataDir+'tree_MET_2017D.root',                  
                                         dataDir+'tree_MET_2017E.root',                  
                                         dataDir+'tree_MET_2017F.root'
                                         ]                  
                                },
        
#        'signal_vbf'        : {'label':'qqH 125',
#                               'datacard':'signal',
#                               'color':1,
#                               'ordering': 9,
#                               'xsec' : 1.0,
#                               'files':[dataDir+'vbfHinv_m125.root',],
#                               },
                
        }

tmp = {}
for p in physics_processes: 
    if physics_processes[p]['ordering']>-1: tmp[p] = physics_processes[p]['ordering']
ordered_physics_processes = []

for key, value in sorted(tmp.iteritems(), key=lambda (k,v): (v,k)):
    ordered_physics_processes.append(key)

def makeTrees(process,tree,channel):
    Trees={}
    Trees[process]   = TChain(tree)
    for sample in  physics_processes[process]['files']:
        Trees[process].Add(sample)
    return Trees[process]

######################################################

