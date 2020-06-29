#! /usr/bin/env python
import sys, os, string, re, time, datetime
import numpy as n

from multiprocessing import Process
from ROOT import *
from math import *
from array import *

### analysis macro
from loadData import *
from tdrStyle import *
from selection import build_selection, build_weights
from pretty import plot_ratio, plot_cms

setTDRStyle()
gROOT.LoadMacro("functions.C+");

### Setup global variables
channel_list = ['signal']

blind = False
vbf = False
vtag = False

folder = './plots'

binLowE = [200, 500, 800, 1200, 1600, 2000, 2750, 3500]
nb = len(binLowE)-1

print "Starting Plotting Be Patient!"

def plot_stack(channel, name,var, bin, low, high, ylabel, xlabel, setLog = False):

    lumi=41500. 
    lumi_str = 41.5

    if not os.path.exists(folder):
        os.mkdir(folder)

    yield_dic = {}    

    ## setup stack plot
    stack = THStack('a', 'a')
    if var.startswith('mjj'):
        added = TH1D('added','added',nb,array('d',binLowE))
    else:
        added = TH1D('added', 'added',bin,low,high)

    added.Sumw2()

    f  = {}
    h1 = {}

    Variables = {}
    cut_standard = build_selection(channel)

    print "INFO Channel is: ", channel, " variable is: ", var, " Selection is: ", cut_standard,"\n"
    print 'INFO time is:', datetime.datetime.fromtimestamp( time.time())

    reordered_physics_processes = []
    if channel == 'Zmm' or channel == 'Zee': 
        reordered_physics_processes = reversed(ordered_physics_processes)
    else: 
        reordered_physics_processes = ordered_physics_processes

    for Type in reordered_physics_processes:
        histName = Type+'_'+name+'_'+channel

        if var.startswith('mjj'):
            Variables[Type] = TH1F(histName,histName,nb,array('d',binLowE))
        else:
            Variables[Type] = TH1F(histName, histName, bin, low, high)
        
        Variables[Type].Sumw2()
        Variables[Type].StatOverflows(kTRUE)

        input_tree = makeTrees(Type,"sr_vbf",channel)
        scale = float(lumi*physics_processes[Type]['xsec'])
        common_weight = build_weights(channel,Type)

        makeTrees(Type,'sr_vbf',channel).Draw(var + " >> " + histName,"(" + cut_standard+ " )"+common_weight,"goff")

        print Type, scale, common_weight

        if var == "mjj":
            nbins = Variables[Type].GetNbinsX()
            Variables[Type].SetBinContent(Variables[Type].GetNbinsX(),Variables[Type].GetBinContent(nbins)+Variables[Type].GetBinContent(nbins+1))

        if Type is'data':            
            Variables[Type].SetMarkerStyle(20)
            Variables[Type].Scale(1,"width")
        else:
            Variables[Type].SetFillColor(TColor.GetColor(physics_processes[Type]['color']))
            Variables[Type].SetLineColor(TColor.GetColor(physics_processes[Type]['color']))        
            Variables[Type].Scale(scale,"width")
            if Type is not 'signal_vbf':
                stack.Add(Variables[Type],"hist")
                added.Add(Variables[Type])            

    print 'INFO - Drawing the Legend', datetime.datetime.fromtimestamp( time.time())

    legend = TLegend(.60,.55,.92,.92)
    lastAdded  = ''
    for process in  ordered_physics_processes:
        Variables[process].SetTitle(process)
        if physics_processes[process]['label'] != lastAdded:
            lastAdded = physics_processes[process]['label']
            if process is not 'data' and process is not 'signal_vbf' and process is not 'signal_ggf':
                legend . AddEntry(Variables[process],physics_processes[process]['label'] , "f")
            if process is 'data':
                legend . AddEntry(Variables[process],physics_processes[process]['label'] , "p")

    c4 = TCanvas("c4","c4", 600, 700)
    c4.SetBottomMargin(0.3)
    c4.SetRightMargin(0.06)
    stack.SetMinimum(0.01)

    if setLog:
        c4.SetLogy()
        if "eta" in var:
            stack.SetMaximum( Variables['data'].GetMaximum()  +  1e8*Variables['data'].GetMaximum() )
        else:
            stack.SetMaximum( Variables['data'].GetMaximum()  +  1e2*Variables['data'].GetMaximum() )

    else:
        stack.SetMaximum( Variables['data'].GetMaximum()  +  0.5*Variables['data'].GetMaximum() )
    
    stack.Draw()
    stack.GetYaxis().SetTitle(ylabel)
    #stack.GetYaxis().CenterTitle()
    stack.GetYaxis().SetTitleOffset(1.2)
    stack.GetXaxis().SetTitleOffset(1.2)
    stack.GetXaxis().SetTitle(xlabel)
    stack.GetXaxis().SetLabelSize(0)
    stack.GetXaxis().SetTitle('')
    
    if channel is 'signal' and blind:
         for b in range(Variables['data'].GetNbinsX()):
             Variables['data'].SetBinContent(b+1,0.0)

    Variables['data'].Draw("Esame")  
    #Variables['signal_vbf'].SetLineWidth(2)
    #Variables['signal_ggf'].SetLineWidth(2)
    #Variables['signal_vbf'].SetLineColor(1)
    #Variables['signal_ggf'].SetLineColor(4)
    #Variables['signal_vbf'].Draw("samehist")
    #Variables['signal_ggf'].Draw("samehist")

    #legend . AddEntry(Variables['signal_vbf'],physics_processes['signal_vbf']['label'] , "l")
    #legend . AddEntry(Variables['signal_ggf'],physics_processes['signal_ggf']['label'] , "l")

    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);

    legend.Draw("same")
    plot_cms(True,lumi_str,c4)


    Pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 0.9)
    Pad.SetTopMargin(0.7)
    Pad.SetRightMargin(0.06)
    Pad.SetFillColor(0)
    Pad.SetGridy(1)
    Pad.SetFillStyle(0)
    Pad.Draw()
    Pad.cd(0)

    data = Variables['data'].Clone()

    plot_ratio(False,data,added,bin,xlabel,0.5,1.5,5)

    f1 = TF1("f1","1",-5000,5000);
    f1.SetLineColor(4);
    f1.SetLineStyle(2);
    f1.SetLineWidth(2);
    f1.Draw("same")

    Pad.Update()
    Pad.RedrawAxis()

    c4.SaveAs(folder+'/Histo_vbf_' + name + '_'+channel+'.pdf')
    c4.SaveAs(folder+'/Histo_vbf_' + name + '_'+channel+'.png')
    c4.SaveAs(folder+'/Histo_vbf_' + name + '_'+channel+'.C')

    del Variables
    del var
    del f
    del h1
    c4.IsA().Destructor( c4 )
    stack.IsA().Destructor( stack )

arguments = {}
#                   = [var, bin, low, high, yaxis, xaxis, setLog]
arguments['met_pt']      = ['met_pt','met_pt',100,200,3500,'Events/GeV','E_{T}^{miss} [GeV]',True]
arguments['met_phi']     = ['met_phi','met_phi',25,-5,5,'Events','E_{T}^{miss} #Phi [GeV]',True]
arguments['CaloMET_pt']  = ['CaloMET_pt','CaloMET_pt',50,0,2000,'Events/GeV','Calo E_{T}^{miss} [GeV]',True]
# arguments['dphipfmet']  = ['dphipfmet','dphipfmet',50,0,5,'Events','#Delta #Phi(jet,E_{T}^{miss})',False]

# Leading jet
arguments['leadak4_pt']    = ['leadak4_pt','leadak4_pt',47,80,1000,'Events/GeV','Leading Jet P_{T} [GeV]',True]
arguments['leadak4_phi']   = ['leadak4_phi','leadak4_phi',25,-5,5,'Events','Leading Jet #phi',False]
arguments['leadak4_eta']   = ['leadak4_eta','leadak4_eta',25,-5,5,'Events','Leading Jet #eta',True]

# Trailing jet
arguments['trailak4_pt']   = ['trailak4_pt','trailak4_pt',49,40,1000,'Events/GeV','Trailing Jet P_{T} [GeV]',True]
arguments['trailak4_phi']  = ['trailak4_phi','trailak4_phi',25,-5,5,'Events','Trailing Jet #phi',False]
arguments['trailak4_eta']  = ['trailak4_eta','trailak4_eta',25,-5,5,'Events','Trailing Jet #eta',True]

# arguments['npv']        = ['npv','npv',50,0,50,'Events','Number of primary vertices',False]
# arguments['njet']       = ['nJet','nJet',6,0,6,'Events','Number of jets',False]

# Dijet quantities
arguments['mjj']       = ['mjj','mjj',5,0,5000,'Events/GeV','m_{jj}',True]
arguments['detajj']    = ['detajj', 'detajj', 40, 0, 8, 'Events', '#Delta #eta_{jj}', True]
arguments['dphijj']    = ['dphijj', 'dphijj', 30, 0, 1.5, 'Events', '#Delta #phi_{jj}', True]

arguments['dphicalopf'] = ['dphicalopf','deltaPhi(calometphi,pfmetphi)',50,0,5,'Events','#Delta#phi_{calomet,pfmet}',False]

# What will you plot
variable_list = ['mjj', 'leadak4_pt', 'leadak4_eta', 'trailak4_pt', 'trailak4_eta', 'detajj']

processes     = []

start_time = time.time()

for channel in channel_list:
    for var in variable_list:
        print var
        arguments[var].insert(0,channel)
        print  arguments[var]
        process = Process(target = plot_stack, args = arguments[var])
        process.start()
        processes.append(process)
        arguments[var].remove(channel)
for process in processes: 
    process.join()

print("--- %s seconds ---" % (time.time()-start_time))
print datetime.datetime.fromtimestamp(time.time()-start_time)
