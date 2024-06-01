from ROOT import *
import json

lumi = 1.0

weight_file = 'config/weight_config.json'
config_file = 'config/processes_config.json'
dataDir = "/eos/user/z/zdemirag/Monojet/Run3Summer22/NanoAODv12_pfnano/"

def extract_data_from_json(json_file):
    with open(weight_file, 'r') as file:
        json_data = json.load(file)
        extracted_data = {}
        for name, data in json_data.items():
            cross_section = data["CrossSection"]["13.6TeV"]
            nevents_2022 = data["NEvents"]["2022"]
            extracted_data[name] = cross_section / nevents_2022
        return extracted_data

weight_dic = extract_data_from_json(weight_file)

def load_processes_from_config(config_file, dataDir, scale_map):
    with open(config_file, 'r') as file:
        config_data = json.load(file)
    
    processes = {}
    for process in config_data['processes']:
        name = process['name']
        xsec = 1.0 if process['label'] == "Data" else weight_dic[process['files'][0].split('_merged.root')[0]]
        processes[name] = {
            'label': process['label'],
            'color': process['color'],
            'ordering': process['ordering'],
            'xsec': xsec,
            'files': [dataDir + f for f in process['files']]
        }
    return processes

physics_processes = load_processes_from_config(config_file, dataDir, weight_dic)

# Now you can use physics_processes as needed
tmp = {}
for p in physics_processes: 
    if physics_processes[p]['ordering'] > -1: 
        tmp[p] = physics_processes[p]['ordering']

ordered_physics_processes = []
for key, value in sorted(tmp.items(), key=lambda item: (item[1], item[0])):
    ordered_physics_processes.append(key)

def makeTrees(process,tree,channel):
    Trees={}
    Trees[process]   = TChain(tree)
    for sample in  physics_processes[process]['files']:
        Trees[process].Add(sample)
    return Trees[process]
