from ROOT import *
import ROOT
import operator
import array
ROOT.gSystem.Load('libRooFit')
import sys

#fileName_In = sys.argv[1]
#fileName_Out = sys.argv[2]
#l1tauType = sys.argv[3]
#isolation = sys.argv[4] 
#etaRange = sys.argv[5]

fileName_In = "/home/sbhowmik/HLTTau/HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/ratePlot/results/hist_Rate_for_HPSL1andHLTTau_Background_DeepTau_All_Stitching_20211012.root"
fileName_Out = "/home/sbhowmik/HLTTau/HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/ratePlot/plots/plot_Rate_for_All_WorkingPoints_HPSL1andHLTTau_DeepTau_All_Stitching_20211012"
l1tauType = "HPS"
isolation = "DeepTau"
etaRange = "All"

def SetLucaStyle ():
    LS = TStyle (gStyle) #copy some of the basics of defualt style...
    LS.SetName("LucaStyle")
    LS.SetTitle("Luca Style")
    # pad
    LS.SetOptStat(000000)
    #LS.SetTickLength(0.02,"X")
    #LS.SetTickLength(0.02,"Y")
    #LS.SetPadTickY(1)
    #LS.SetPadTickX(1)
    LS.SetPadGridY(1);
    LS.SetPadGridX(1);
    #LS.SetPadBottomMargin(0.13)
    LS.SetPadLeftMargin(0.11)
    LS.SetCanvasDefH(800)
    LS.SetCanvasDefW(800)
    # axis

    LS.cd() 
    return LS


#############################################

SetLucaStyle()

fileIn = TFile (fileName_In)

tauNumbers = ["Double", "Single"]
#tauNumbers = ["Double"]
#workingPointNames = ["NoCut", "dZ", "VLoose", "Loose", "Medium", "Tight"]
workingPointNames = ["VLoose", "Loose", "Medium", "Tight"]
#workingPoints = ["No cut", "dz cut", "dz cut + Very Loose", "dz cut + Loose", "dz cut + Medium", "dz cut + Tight"]
if(isolation == "ChargedIso"):
    workingPoints=["I_{ch} < 0.50#times p_{T}", "I_{ch} < 0.20#times p_{T}", "I_{ch} < 0.10#times p_{T}", "I_{ch} < 0.05#times p_{T}"] 
if(isolation == "DeepTau"):
    workingPoints=["D > 0.5", "D > 0.6", "D > 0.7", "D > 0.8"]
    workingPoints=["D > 0.1", "D > 0.2", "D > 0.3", "D > 0.35"]

#workingPointNames = ["NoCut"]
#workingPoints = [" "]

c1 = TCanvas ("c1", "c1", 800, 800)
c1.SetLogy()
#c1.SetLogx()

xpos  = 0.11
ypos  = 0.91
cmsTextSize   = 0.03
CMSbox       = ROOT.TLatex  (xpos, ypos, "#scale[1.5]{CMS} ")
CMSbox       = ROOT.TLatex  (xpos, ypos, "#scale[1.5]{CMS}           Phase-2 Simulation              PU=200            14 TeV")
CMSbox.SetNDC()
CMSbox.SetTextSize(cmsTextSize)

lumi = "57 fb^{-1} (13 TeV)"
lumi = ""
lumibox = ROOT.TLatex  (0.7, 0.91, lumi)
lumibox.SetNDC()
lumibox.SetTextSize(cmsTextSize)

xposText = 0.14
yposText = 0.85
extraTextSize   = 0.035
extraText1 =["#tau_{h}#tau_{h} Trigger" , "#tau_{h} Trigger"]
extraTextBox1 = ROOT.TLatex  (xposText, yposText, extraText1[1])
extraTextBox1.SetNDC()
extraTextBox1.SetTextSize(extraTextSize)
if(l1tauType=="NN"):
    extraTextBox2 = ROOT.TLatex  (xposText, yposText - 0.06, "L1NN + HLT")
elif(l1tauType=="HPS"):
    extraTextBox2 = ROOT.TLatex  (xposText, yposText - 0.06, "L1HPS + HLT")
else:
    extraTextBox2 = ROOT.TLatex  (xposText, yposText - 0.06, "HLT")
extraTextBox2.SetNDC()
extraTextBox2.SetTextSize(extraTextSize)
if(etaRange=="Barrel"):
    extraTextBox3 = ROOT.TLatex  (xposText, yposText - 0.12, "|#eta| < 1.5")
elif(etaRange=="Endcap"):
    extraTextBox3 = ROOT.TLatex  (xposText, yposText - 0.12, "1.5 < |#eta| < 2.4") 
else:
    extraTextBox3 = ROOT.TLatex  (xposText, yposText - 0.12, "|#eta| < 2.1")

extraTextBox3.SetNDC()
extraTextBox3.SetTextSize(extraTextSize)

extraTextBox4 = ROOT.TLatex  (xposText, yposText - 0.18, "")
extraTextBox4.SetNDC()
extraTextBox4.SetTextSize(extraTextSize)

extraTextBox5 = ROOT.TLatex  (xposText, yposText - 0.24, "")
extraTextBox5.SetNDC()
extraTextBox5.SetTextSize(extraTextSize)

legend = ROOT.TLegend(0.52, 0.66, 0.89, 0.88)
#legend = ROOT.TLegend(0.17, 0.36, 0.49, 0.38)
legend.SetLineColor(0)
legend.SetFillColor(0)
legend.SetTextSize(extraTextSize)



first = True
idxTau=0
for tauNumber in tauNumbers:
    count=0
    for i in range (0, len(workingPointNames)):
    #for i in range (0, 1):
        count+=1
        if(count==5):
            count+=1
        hist_HLTTau = fileIn.Get("Rate_%s_HLTTau_%s" % (tauNumber,workingPointNames[i]))
        #hist_HLTTau = fileIn.Get("Rate_%s_HLTTau" % (tauNumber))
        hist_HLTTau.SetLineColor(count)
        hist_HLTTau.SetMarkerColor(count)
        hist_HLTTau.SetMarkerStyle(8)
        hist_HLTTau.SetMinimum(1)
        hist_HLTTau.SetMaximum(100000)
        if(tauNumber=="Double"):
            hist_HLTTau.SetMarkerSize(1.0)
            hist_HLTTau.SetAxisRange(0, 80)
        else:
            hist_HLTTau.SetMarkerSize(0.50)
            hist_HLTTau.SetAxisRange(0, 160)
        hist_HLTTau.SetTitle(";#tau_{h} p_{T} (GeV) ; Rate (Hz)")
        hist_HLTTau.GetXaxis().SetTitleOffset(0.9)
        hist_HLTTau.GetXaxis().SetTitleSize(0.05)
        hist_HLTTau.GetYaxis().SetTitleOffset(0.9)
        hist_HLTTau.GetYaxis().SetTitleSize(0.05)
        if (i==0):
            #hist_HLTTau.Draw("p e")
            hist_HLTTau.Draw("p ")
        else:
            #hist_HLTTau.Draw("p e same")
            hist_HLTTau.Draw("p  same")
        if (idxTau==0):
            legend.AddEntry(hist_HLTTau,  workingPoints[i],  "lp") 
    legend.Draw()

    CMSbox.Draw()
    lumibox.Draw()
    extraTextBox1.SetText(xposText, yposText, extraText1[idxTau])
    extraTextBox1.Draw()
    extraTextBox2.Draw()
    extraTextBox3.Draw()
    extraTextBox4.Draw()
    extraTextBox5.Draw()

    c1.Print(fileName_Out + "_" + tauNumber + ".pdf", "pdf")
    c1.Print(fileName_Out + "_" + tauNumber + ".png", "png")
    c1.Print(fileName_Out + "_" + tauNumber + ".root", "root")
    idxTau+=1



