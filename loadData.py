#! /usr/bin/env python
from ROOT import *

lumi = 1.0

######################################################

dataDir = "/afs/cern.ch/work/a/aakpinar/public/forZeynep/tree_test/"

physics_processes = {
        'Zvv_HT100'         : { 'label'   : 'Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : (1.0*10),
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-100To200-mg_2017.root"],
                                },
        'Zvv_HT200'         : { 'label'   : 'Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : 1.0,
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-100To200-mg_2017.root"],
                                },
        'Zvv_HT400'         : { 'label'   : 'Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : 1.0,
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-100To200-mg_2017.root"],
                                },
        'Zvv_HT600'         : { 'label'   : 'Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : 1.0,
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-100To200-mg_2017.root"],
                                },
        'Zvv_HT800'         : { 'label'   : 'Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : 1.0,
                                'files'   : [dataDir+"tree_ZJetsToNuNu_HT-100To200-mg_2017.root"],
                                },

        'data'              : { 'label':'Data',
                                'datacard':'data',
                                'color': 1,
                                'ordering': 8,    
                                'xsec' : 1.0,                  
                                'files':[dataDir+'tree_MET_2017B.root',],                  
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

