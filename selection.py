import re

def build_weights(channel, Type):

    common_weight = "*(weight_total)"

    ##This is the section where you define the weights => one can make this auxilary, to build proper weights per channel
    #if channel is 'signal':
    #    if Type is 'data':
    #        common_weight = "*(1.0)"
    #    elif re.match(vjets_regex, Type):
    #        common_weight = "*weight_gen*weight_prefire*weight_pileup*weight_theory*weight_trigger_met"
    #    # Do not apply theory weight if not V+jets MC
    #    else:
    #        common_weight = "*weight_gen*weight_prefire*weight_pileup*weight_trigger_met"

    return common_weight

def build_selection(selection):

    selections = ['diMuon_CR']
    
    snippets = {}
    
    selectionString = ''
    for cut in snippets:
        if selection in snippets[cut][1]: 
            selectionString += snippets[cut][0]+'&&'
            

    selectionString+=" 1.0"
    return selectionString

