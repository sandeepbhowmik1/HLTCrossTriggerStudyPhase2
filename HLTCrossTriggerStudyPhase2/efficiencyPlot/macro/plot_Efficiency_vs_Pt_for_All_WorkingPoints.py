import ROOT
import Efficiency_plot_macro as EfficiencyPlot
import sys

#fileName_In = sys.argv[1]
#fileName_In_txt = sys.argv[2]
#fileName_Out = sys.argv[3]
#isolation = sys.argv[4]
#etaRange = sys.argv[5]
#l1tauType = sys.argv[6]

fileName_In = "/home/sbhowmik/HLTTau/HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/efficiencyPlot/results/fitOutput_Efficiency_vs_Pt_for_Double_Gen_HPSL1andHLTTau_DeepTau_All_Stitching_20211012.root"
fileName_In_txt = "/home/sbhowmik/HLTTau/HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/ratePlot/results/hist_Rate_for_HPSL1andHLTTau_Background_DeepTau_All_Stitching_20211012.txt"
fileName_Out = "/home/sbhowmik/HLTTau/HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/efficiencyPlot/plots/plot_Efficiency_vs_Pt_for_Double_Gen_HPSL1andHLTTau_DeepTau_All_Stitching_20211012"
isolation = "DeepTau"
etaRange = "All"
l1tauType = "HPS"

if(etaRange=="Barrel"):
    etaMin = 0
    etaMax = 1.5
elif(etaRange=="Endcap"):
    etaMin = 1.5
    etaMax = 2.4
else:
    etaMin = 0
    etaMax = 2.1

with open(fileName_In_txt,'r') as f:
    for line in f:
        words = line.split()
        if words[0]=='DoubleTau' and words[1]=='NoCut' :
            pt_Threshold_NoCut = words[4]
        if words[0]=='DoubleTau' and words[1]=='dZ' :
            pt_Threshold_dZ = words[4]
        if words[0]=='DoubleTau' and words[1]=='VLoose' :
            pt_Threshold_VLoose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Loose' :
            pt_Threshold_Loose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Medium' :
            pt_Threshold_Medium = words[4]
        if words[0]=='DoubleTau' and words[1]=='Tight' :
            pt_Threshold_Tight = words[4]


fileIn_HLTTau = ROOT.TFile.Open(fileName_In)

hist_HLTTau = []
fit_HLTTau = []
efficiency_HLTTau = []
plots = []

#workingPointNames=["hltTauNoCut","hltTaudZ", "hltTauVLoose", "hltTauLoose", "hltTauMedium", "hltTauTight"]
workingPointNames=["hltTauVLoose", "hltTauLoose", "hltTauMedium", "hltTauTight"]
#workingPointNames=["hltLoose", "hltMedium", "hltTight"]
if(isolation == "ChargedIso"):
    workingPoints=["I_{ch} < 0.50#times p_{T}", "I_{ch} < 0.20#times p_{T}", "I_{ch} < 0.10#times p_{T}", "I_{ch} < 0.05#times p_{T}"]
if(isolation == "DeepTau"):
    #workingPoints=["D > 0.5", "D > 0.6", "D > 0.7", "D > 0.8"]
    workingPoints=["D > 0.3, #tau p_{T} > %s" % pt_Threshold_VLoose, "D > 0.4, #tau p_{T} > %s" % pt_Threshold_Loose, "D > 0.5, #tau p_{T} > %s" % pt_Threshold_Medium, "D > 0.6, #tau p_{T} > %s" % pt_Threshold_Tight]
#workingPoints = ["No cut (No p_{T} Threshold )", "dz cut (p_{T} Threshold = %s GeV)" % pt_Threshold_dZ, "dz cut + Very Loose (p_{T} Threshold = %s GeV)" % pt_Threshold_VLoose, "dz cut + Loose (p_{T} Threshold = %s GeV)" % pt_Threshold_Loose, "dz cut + Medium (p_{T} Threshold = %s GeV)" % pt_Threshold_Medium, "dz cut + Tight (p_{T} Threshold = %s GeV)" % pt_Threshold_Tight]
#workingPoints = ["Loose (p_{T} Threshold=%sGeV)" % hltTauPt_Threshold[2], "Medium (p_{T} Threshold=%sGeV)" % hltTauPt_Threshold[1], "Tight (p_{T} Threshold=%sGeV)" % hltTauPt_Threshold[0]]
#workingPoints = ["#tau p_{T} > 5 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[5], "#tau p_{T} > 10 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[4], "#tau p_{T} > 15 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[3], "#tau p_{T} > 20 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[2], "#tau p_{T} > 25 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[1], "#tau p_{T} > 30 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[0]]

#plotRanges=[500, 1000]
plotRanges=[100, 200, 500]

for k in range (0, len(plotRanges)):
    count=0
    plots.append(EfficiencyPlot.EfficiencyPlot())
    for i in range (0, len(workingPointNames)):
        count+=1
        if(count==5):
            count+=1
        hist_HLTTau.append(fileIn_HLTTau.Get("histo_Phase2_HLTTau_"+workingPointNames[i]))
        hist_HLTTau[-1].__class__ = ROOT.RooHist
        fit_HLTTau.append(fileIn_HLTTau.Get("fit_Phase2_HLTTau_"+workingPointNames[i]))
        fit_HLTTau[-1].__class__ = ROOT.RooCurve
        efficiency_HLTTau.append(EfficiencyPlot.Efficiency(Name="HLTTau", Histo=hist_HLTTau[-1], Fit=fit_HLTTau[-1],
                                                               MarkerColor=(count), MarkerStyle=20, LineColor=(count),LineStyle=1,
                                                               Legend=workingPoints[i]))

        plots[-1].addEfficiency(efficiency_HLTTau[-1])
    plots[-1].xposText =0.14
    plots[-1].yposText =0.85
    plots[-1].extraText1 = "#tau_{h}#tau_{h} Trigger"
    plots[-1].extraText2 = "HLT"
    if(l1tauType=="NN"):
        plots[-1].extraText2 = "L1NN + HLT"
    elif(l1tauType=="HPS"):
        plots[-1].extraText2 = "L1HPS + HLT"
    else:
        plots[-1].extraText2 = "HLT"
    if(etaRange=="Barrel"):
        plots[-1].extraText3 = "|#eta| < 1.5"
    elif(etaRange=="Endcap"):
        plots[-1].extraText3 = "1.5 < |#eta| < 2.4"
    else:
        plots[-1].extraText3 = "|#eta| < 2.1"
    plots[-1].extraText4 = "Rate 150 Hz"
    #plots[-1].extraText4 = ""
    plots[-1].extraText5 = ""
    plots[-1].extraText6 = ""
    plots[-1].name = fileName_Out + "_" + str(plotRanges[k])
    plots[-1].xRange = (20, plotRanges[k]+1)
    plots[-1].xTitle = "gen #tau_{h} p_{T} (GeV)"
    #plots[-1].xTitle = "Offline #tau_{h} p_{T} [GeV]"
    #plots[-1].legendPosition = (0.12, 0.725, 0.85, 0.898)
    plots[-1].legendPosition = (0.5, 0.15, 0.87, 0.3)

canvas = []
for plot in plots:
    canvas.append(plot.plot())

fileIn_HLTTau.Close()


