import json

dataDir = "/eos/user/z/zdemirag/Monojet/Run3Summer22/NanoAODv12_pfnano/"

# Read file names from the text file
def read_file_list(file_path):
    mapping_dic = {}
    file_list = []
    with open(file_path, 'r') as file:
        files = [line.strip() for line in file if line.strip()]
        for file_name in files:
            file_list.append(file_name)
            process_name = file_name.split('_merged.root')[0]
            
            # Fill the mapping dictionary based on the file name patterns
            if file_name.startswith("WtoLNu-2Jets"):
                mapping_dic[process_name] = ["QCD W#rightarrow l #nu", "Wln", "#E6E6FA", 7]
            elif file_name.startswith("VBFtoLNu"):
                mapping_dic[process_name] = ["EWK W#rightarrow l #nu", "EWKWln", "#08306B", 4]
            elif file_name.startswith("DYto2L-2Jets"):
                mapping_dic[process_name] = ["Z#rightarrow ll", "Zll", "#F08080", 1]
            elif file_name.startswith("VBFto2L"):
                mapping_dic[process_name] = ["EWK Z#rightarrow ll", "EWKZll", "#FC4E2A", 2]
            elif (file_name.startswith("WW_TuneCP5") or 
                  file_name.startswith("WZ_TuneCP5") or 
                  file_name.startswith("ZZ_TuneCP5")):
                mapping_dic[process_name] = ["Diboson", "Diboson", "#DAA520", 5]
            elif file_name.startswith("TTto"):
                mapping_dic[process_name] = ["Top", "Top", "#FFD700", 3]
            else:
                mapping_dic[process_name] = ["Data", "Data", 1, 9]
                
    return file_list, mapping_dic

# Generate JSON configuration from the file list
def generate_json_config(file_list, mapping_dic):
    config = {"processes": []}
    for file_name in file_list:
        process_name = file_name.split('_merged.root')[0]
        process_info = mapping_dic[process_name]
        config["processes"].append({
            "name": process_name, #process_info[1],
            "label": process_info[0],
            "color": process_info[2],
            "ordering": process_info[3],
            "files": [file_name]
        })
    return config

# Main function to generate and save the JSON config
def main():
    file_list_path = 'file_list.txt'
    file_list, mapping_dic = read_file_list(file_list_path)
    config = generate_json_config(file_list, mapping_dic)
    
    with open('processes_config.json', 'w') as json_file:
        json.dump(config, json_file, indent=4)

if __name__ == "__main__":
    main()
