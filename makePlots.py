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
ROOT.gROOT.SetBatch(True)

channel_list = ['diMuon_CR']
blind = False
vbf = False
vtag = False
folder = '/eos/user/z/zdemirag/www/monojet/'
binLowE = [250,275,300,350,400,450,500,650,800,1150,1500]
nb = len(binLowE)-1

print "Starting Plotting Be Patient!"

def plot_stack(channel, name, var, bin, low, high, ylabel, xlabel, setLog=False):
    lumi = 7980.
    lumi_str = 7.98

    if not os.path.exists(folder):
        os.mkdir(folder)

    ## setup stack plot
    stack = THStack('a', 'a')
    if var.startswith(channel+'_recoil_pt'):
        added = TH1D('added', 'added', nb, array('d', binLowE))
    else:
        added = TH1D('added', 'added', bin, low, high)

    added.Sumw2()

    Variables = {}
    cut_standard = build_selection(channel)

    print "INFO Channel is: ", channel, " variable is: ", var, " Selection is: ", cut_standard,"\n"
    print 'INFO time is:', datetime.datetime.fromtimestamp(time.time())

    reordered_physics_processes = list(reversed(ordered_physics_processes)) if channel in ['diMuon_CR', 'diElectron_CR'] else ordered_physics_processes

    for Type in reordered_physics_processes:
        histName = Type + '_' + name + '_' + channel

        if var.startswith(channel+'_recoil_pt'):
            Variables[Type] = TH1F(histName, histName, nb, array('d', binLowE))
        else:
            Variables[Type] = TH1F(histName, histName, bin, low, high)
        
        Variables[Type].Sumw2()
        Variables[Type].StatOverflows(kTRUE)

        input_tree = makeTrees(Type, "Events", channel)
        scale = float(lumi * physics_processes[Type]['xsec'])
        common_weight = build_weights(channel, Type)

        makeTrees(Type, 'Events', channel).Draw(var + " >> " + histName, "(" + cut_standard + " )" + common_weight, "goff")

        print Type, scale, common_weight

        if var == channel+'_recoil_pt':
            nbins = Variables[Type].GetNbinsX()
            Variables[Type].SetBinContent(Variables[Type].GetNbinsX(), Variables[Type].GetBinContent(nbins) + Variables[Type].GetBinContent(nbins + 1))

        if Type == 'Data':
            Variables[Type].SetMarkerStyle(20)
            Variables[Type].Scale(1, "width")
        else:
            Variables[Type].SetFillColor(TColor.GetColor(physics_processes[Type]['color']))
            Variables[Type].SetLineColor(TColor.GetColor(physics_processes[Type]['color']))
            Variables[Type].Scale(scale, "width")
            if Type != 'signal_vbf':
                stack.Add(Variables[Type], "hist")
                added.Add(Variables[Type])

    print 'INFO - Drawing the Legend', datetime.datetime.fromtimestamp(time.time())

    legend = TLegend(.60, .55, .92, .92)
    lastAdded = ''
    for process in ordered_physics_processes:
        Variables[process].SetTitle(process)
        if physics_processes[process]['label'] != lastAdded:
            lastAdded = physics_processes[process]['label']
            if process != 'Data' and process != 'signal_vbf' and process != 'signal_ggf':
                legend.AddEntry(Variables[process], physics_processes[process]['label'], "f")
            if process == 'Data':
                legend.AddEntry(Variables[process], physics_processes[process]['label'], "p")

    c4 = TCanvas("c4", "c4", 600, 700)
    c4.SetBottomMargin(0.3)
    c4.SetRightMargin(0.06)
    stack.SetMinimum(0.01)

    if setLog:
        c4.SetLogy()
        stack.SetMaximum(Variables['Data'].GetMaximum() + 1e8 * Variables['Data'].GetMaximum())
    else:
        stack.SetMaximum(Variables['Data'].GetMaximum() + 0.5 * Variables['Data'].GetMaximum())
    
    stack.Draw()
    stack.GetYaxis().SetTitle(ylabel)
    stack.GetYaxis().SetTitleOffset(1.2)
    stack.GetXaxis().SetTitleOffset(1.2)
    stack.GetXaxis().SetLabelSize(0)
    stack.GetXaxis().SetTitle('')
    
    Variables['Data'].Draw("Esame")  

    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.Draw("same")
    plot_cms(True, lumi_str, c4)

    Pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 0.9)
    Pad.SetTopMargin(0.7)
    Pad.SetRightMargin(0.06)
    Pad.SetFillColor(0)
    Pad.SetGridy(1)
    Pad.SetFillStyle(0)
    Pad.Draw()
    Pad.cd(0)

    data = Variables['Data'].Clone()

    plot_ratio(False, data, added, bin, xlabel, 0.5, 1.5, 5)

    f1 = TF1("f1", "1", -5000, 5000)
    f1.SetLineColor(4)
    f1.SetLineStyle(2)
    f1.SetLineWidth(2)
    f1.Draw("same")

    Pad.Update()
    Pad.RedrawAxis()

    c4.SaveAs(folder + '/Histo_' + name + '_' + channel + '.pdf')
    c4.SaveAs(folder + '/Histo_' + name + '_' + channel + '.png')
    c4.SaveAs(folder + '/Histo_' + name + '_' + channel + '.C')

    del Variables
    del var
    c4.IsA().Destructor(c4)
    stack.IsA().Destructor(stack)

arguments = {}

#                   = [var, bin, low, high, yaxis, xaxis, setLog]

arguments['diMuon_CR_recoil_pt']      = ['diMuon_CR_recoil_pt','diMuon_CR_recoil_pt',100,200,3500,'Events/GeV','Recoil [GeV]',True]


variable_list = ['diMuon_CR_recoil_pt']

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
