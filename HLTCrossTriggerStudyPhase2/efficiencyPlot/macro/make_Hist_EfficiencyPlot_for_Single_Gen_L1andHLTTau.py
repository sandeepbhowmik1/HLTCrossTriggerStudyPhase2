from ROOT import *
import numpy as n
import math
import sys

#fileName_In = sys.argv[1]
#treeName_In = sys.argv[2]
#fileName_In_txt = sys.argv[3] 
#fileName_Out = sys.argv[4]
#isolation = sys.argv[5]
#etaRange = sys.argv[6]
#l1tauType = sys.argv[7]

fileName_In = "/home/sbhowmik/RootTree/HLTTau/Phase2/rootTree_test_L1andHLTTauAnalyzer_Signal_VBFHToTauTau_ChargedIso_20210208.root"
treeName_In = "L1andHLTTauAnalyzer/L1andHLTTauAnalyzer"
fileName_In_txt = "/home/sbhowmik/HLTTau/HLTTauStudyPhase2/HLTTauPerformancePhase2/ratePlot/results/hist_Rate_for_HPSL1andHLTTau_Background_ChargedIso_All_Stitching_20210208.txt"
#fileName_Out = "/home/sbhowmik/HLTTau/HLTTauStudyPhase2/HLTTauPerformancePhase2/efficiencyPlot/results/hist_EfficiencyPlot_for_Single_Gen_HPSL1andHLTTau_ChargedIso_All_Stitching_20210208.root"
#fileName_Out = "/home/sbhowmik/HLTTau/HLTTauStudyPhase2/HLTTauPerformancePhase2/efficiencyPlot/results/hist_EfficiencyPlot_for_Single_Gen_HPSL1andHLTTau_ChargedIso_All_Stitching_20210208_w2genTau.root"
fileName_Out = "/home/sbhowmik/HLTTau/HLTTauStudyPhase2/HLTTauPerformancePhase2/efficiencyPlot/results/hist_EfficiencyPlot_for_Single_Gen_HPSL1andHLTTau_ChargedIso_All_Stitching_20210417.root"

isolation = "ChargedIso"
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

tauPtMin = 20
L1NNTauPtMin = 32
L1HPSTauPtMin = 21
tauLeadTrack_Pt_min = 5.0

with open(fileName_In_txt,'r') as f:
    for line in f:
        words = line.split()
        if words[0]=='DoubleTau' and words[1]=='NoCut' :
            rate_Target_NoCut = words[2]
            pt_Threshold_NoCut = words[4]
        if words[0]=='DoubleTau' and words[1]=='dZ' :
            rate_Target_dZ = words[2]
            pt_Threshold_dZ = words[4]
        if words[0]=='DoubleTau' and words[1]=='VLoose' :
            rate_Target_VLoose = words[2]
            pt_Threshold_VLoose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Loose' :
            rate_Target_Loose = words[2]
            pt_Threshold_Loose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Medium' :
            rate_Target_Medium = words[2]
            pt_Threshold_Medium = words[4]
        if words[0]=='DoubleTau' and words[1]=='Tight' :
            rate_Target_Tight = words[2]
            pt_Threshold_Tight = words[4]

#pt_Threshold_NoCut = 20.0
#pt_Threshold_dZ = 20.0
#pt_Threshold_VLoose = 20.0
#pt_Threshold_Loose = 20.0
#pt_Threshold_Medium = 20.0
#pt_Threshold_Tight = 20.0

print "rate_Target_NoCut ", rate_Target_NoCut, "pt_Threshold_NoCut", pt_Threshold_NoCut
print "rate_Target_dZ ", rate_Target_dZ, "pt_Threshold_dZ", pt_Threshold_dZ
print "rate_Target_VLoose ", rate_Target_VLoose, "pt_Threshold_VLoose", pt_Threshold_VLoose
print "rate_Target_Loose ", rate_Target_Loose, "pt_Threshold_Loose", pt_Threshold_Loose
print "rate_Target_Medium ", rate_Target_Medium, "pt_Threshold_Medium", pt_Threshold_Medium
print "rate_Target_Tight ", rate_Target_Tight, "pt_Threshold_Tight", pt_Threshold_Tight


fileIn = TFile.Open(fileName_In)
treeIn = fileIn.Get(treeName_In)
fileOut = TFile (fileName_Out, 'recreate')
treeOut = TTree("HLTTauAnalyzer", "HLTTauAnalyzer")

hist_GenHLTTau_Pt_Denominator = TH1F ("GenHLTTau_Pt_Denominator", "GenHLTTau_Pt_Denominator", 200, 0., 1000.)

hist_GenHLTTau_Pt_Numerator_VLoose = TH1F ("GenHLTTau_Pt_Numerator_VLoose", "GenHLTTau_Pt_Numerator_VLoose", 200, 0., 1000.)
hist_GenHLTTau_Pt_Numerator_Loose = TH1F ("GenHLTTau_Pt_Numerator_Loose", "GenHLTTau_Pt_Numerator_Loose", 200, 0., 1000.)
hist_GenHLTTau_Pt_Numerator_Medium = TH1F ("GenHLTTau_Pt_Numerator_Medium", "GenHLTTau_Pt_Numerator_Medium", 200, 0., 1000.)
hist_GenHLTTau_Pt_Numerator_Tight = TH1F ("GenHLTTau_Pt_Numerator_Tight", "GenHLTTau_Pt_Numerator_Tight", 200, 0., 1000.)

hist_GenHLTTau_Pt_Efficiency_VLoose = TH1F ("GenHLTTau_Pt_Efficiency_VLoose", "GenHLTTau_Pt_Efficiency_VLoose", 200, 0., 1000.)
hist_GenHLTTau_Pt_Efficiency_Loose = TH1F ("GenHLTTau_Pt_Efficiency_Loose", "GenHLTTau_Pt_Efficiency_Loose", 200, 0., 1000.)
hist_GenHLTTau_Pt_Efficiency_Medium = TH1F ("GenHLTTau_Pt_Efficiency_Medium", "GenHLTTau_Pt_Efficiency_Medium", 200, 0., 1000.)
hist_GenHLTTau_Pt_Efficiency_Tight = TH1F ("GenHLTTau_Pt_Efficiency_Tight", "GenHLTTau_Pt_Efficiency_Tight", 200, 0., 1000.)

hist_GenHLTTau_Pt_Efficiency_with_dZ_VLoose = TH1F ("GenHLTTau_Pt_Efficiency_with_dZ_VLoose", "GenHLTTau_Pt_Efficiency_with_dZ_VLoose", 200, 0., 1000.)
hist_GenHLTTau_Pt_Efficiency_with_dZ_Loose = TH1F ("GenHLTTau_Pt_Efficiency_with_dZ_Loose", "GenHLTTau_Pt_Efficiency_with_dZ_Loose", 200, 0., 1000.)
hist_GenHLTTau_Pt_Efficiency_with_dZ_Medium = TH1F ("GenHLTTau_Pt_Efficiency_with_dZ_Medium", "GenHLTTau_Pt_Efficiency_with_dZ_Medium", 200, 0., 1000.)
hist_GenHLTTau_Pt_Efficiency_with_dZ_Tight = TH1F ("GenHLTTau_Pt_Efficiency_with_dZ_Tight", "GenHLTTau_Pt_Efficiency_with_dZ_Tight", 200, 0., 1000.)

hist_GenHLTTau_Pt_2D_Denominator_VLoose = TH2F ("GenHLTTau_Pt_2D_Denominator_VLoose", "GenHLTTau_Pt_2D_Denominator_VLoose", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Denominator_Loose = TH2F ("GenHLTTau_Pt_2D_Denominator_Loose", "GenHLTTau_Pt_2D_Denominator_Loose", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Denominator_Medium = TH2F ("GenHLTTau_Pt_2D_Denominator_Medium", "GenHLTTau_Pt_2D_Denominator_Medium", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Denominator_Tight = TH2F ("GenHLTTau_Pt_2D_Denominator_Tight", "GenHLTTau_Pt_2D_Denominator_Tight", 200, 0., 1000., 200, 0., 1000.)


hist_GenHLTTau_Pt_2D_Numerator_VLoose = TH2F ("GenHLTTau_Pt_2D_Numerator_VLoose", "GenHLTTau_Pt_2D_Numerator_VLoose", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Numerator_Loose = TH2F ("GenHLTTau_Pt_2D_Numerator_Loose", "GenHLTTau_Pt_2D_Numerator_Loose", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Numerator_Medium = TH2F ("GenHLTTau_Pt_2D_Numerator_Medium", "GenHLTTau_Pt_2D_Numerator_Medium", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Numerator_Tight = TH2F ("GenHLTTau_Pt_2D_Numerator_Tight", "GenHLTTau_Pt_2D_Numerator_Tight", 200, 0., 1000., 200, 0., 1000.)

hist_GenHLTTau_Pt_2D_Efficiency_VLoose = TH2F ("GenHLTTau_Pt_2D_Efficiency_VLoose", "GenHLTTau_Pt_2D_Efficiency_VLoose", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Efficiency_Loose = TH2F ("GenHLTTau_Pt_2D_Efficiency_Loose", "GenHLTTau_Pt_2D_Efficiency_Loose", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Efficiency_Medium = TH2F ("GenHLTTau_Pt_2D_Efficiency_Medium", "GenHLTTau_Pt_2D_Efficiency_Medium", 200, 0., 1000., 200, 0., 1000.)
hist_GenHLTTau_Pt_2D_Efficiency_Tight = TH2F ("GenHLTTau_Pt_2D_Efficiency_Tight", "GenHLTTau_Pt_2D_Efficiency_Tight", 200, 0., 1000., 200, 0., 1000.)

hist_GenHLTTau_Pt_1D_Efficiency_VLoose = TH1F ("GenHLTTau_Pt_1D_Efficiency_VLoose", "GenHLTTau_Pt_1D_Efficiency_VLoose", 200, 0., 1000.)
hist_GenHLTTau_Pt_1D_Efficiency_Loose = TH1F ("GenHLTTau_Pt_1D_Efficiency_Loose", "GenHLTTau_Pt_1D_Efficiency_Loose", 200, 0., 1000.)
hist_GenHLTTau_Pt_1D_Efficiency_Medium = TH1F ("GenHLTTau_Pt_1D_Efficiency_Medium", "GenHLTTau_Pt_1D_Efficiency_Medium", 200, 0., 1000.)
hist_GenHLTTau_Pt_1D_Efficiency_Tight = TH1F ("GenHLTTau_Pt_1D_Efficiency_Tight", "GenHLTTau_Pt_1D_Efficiency_Tight", 200, 0., 1000.)


bkgSubW = n.zeros(1, dtype=float)
tauPt = n.zeros(1, dtype=float)
tauEta = n.zeros(1, dtype=float)
tauPhi = n.zeros(1, dtype=float)
hltTauPt = n.zeros(1, dtype=float)
hltTauEta = n.zeros(1, dtype=float)
hltTauPhi = n.zeros(1, dtype=float)
hltTauNoCut = n.zeros(1, dtype=int)
hltTaudZ = n.zeros(1, dtype=int)
hltTauVLoose = n.zeros(1, dtype=int)
hltTauLoose = n.zeros(1, dtype=int)
hltTauMedium = n.zeros(1, dtype=int)
hltTauTight = n.zeros(1, dtype=int)
#Nvtx = n.zeros(1, dtype=float)

treeOut.Branch("bkgSubW", bkgSubW, "bkgSubW/D")
treeOut.Branch("tauPt", tauPt, "tauPt/D")
treeOut.Branch("tauEta", tauEta, "tauEta/D")
treeOut.Branch("tauPhi", tauPhi, "tauPhi/D")
treeOut.Branch("hltTauPt", hltTauPt, "hltTauPt/D")
treeOut.Branch("hltTauEta", hltTauEta, "hltTauEta/D")
treeOut.Branch("hltTauPhi", hltTauPhi, "hltTauPhi/D")
treeOut.Branch("hltTauNoCut", hltTauNoCut, "hltTauNoCut/I")
treeOut.Branch("hltTaudZ", hltTaudZ, "hltTaudZ/I")
treeOut.Branch("hltTauVLoose", hltTauVLoose, "hltTauVLoose/I")
treeOut.Branch("hltTauLoose", hltTauLoose, "hltTauLoose/I")
treeOut.Branch("hltTauMedium", hltTauMedium, "hltTauMedium/I")
treeOut.Branch("hltTauTight", hltTauTight, "hltTauTight/I")
#treeOut.Branch("Nvtx", Nvtx, "Nvtx/D")

def sort_PFTaus(old_PFTau_Pts):
    new_PFTau_Pts = []
    for i in range (0, len(old_PFTau_Pts)):
        i_hltTauPt = old_PFTau_Pts[i]
        temp_hltTauPt = 0
        for j in range (0, len(old_PFTau_Pts)):
            j_hltTauPt = old_PFTau_Pts[j]
            if j_hltTauPt > i_hltTauPt :
                temp_hltTauPt = j_hltTauPt
            else :
                temp_hltTauPt = i_hltTauPt
                new_PFTau_Pts.append(temp_hltTauPt)
    return new_PFTau_Pts

def Is_dZPass(hltTauau1Pt, hltTauau1_Z, hltTauau2Pt, hltTauau2_Z):
    dz = abs(hltTauau1_Z - hltTauau2_Z)
    #if dz < 0.40:
    if dz < 0.20:
        return True
    return False

nentries = treeIn.GetEntries()
print "nentries ", nentries

for ev in range (0, nentries):
    treeIn.GetEntry(ev)
    if (ev%10000 == 0) : print ev, "/", nentries
    bkgSubW[0] = 1. 
    
    gentauPt_ = []
    gentauEta_ = []
    gentauPhi_ = []
    #Nvtx_ = []
    Ngentau_ = 0
    
    # CV: read generator-level hadronic tau information from TTree
    for i in range(0, treeIn.genTauPt.size()):
        if abs(treeIn.genTauEta[i]) > double(etaMax):
            continue
        if abs(treeIn.genTauEta[i]) < double(etaMin):
            continue
        if abs(treeIn.genTauPt[i]) < double(tauPtMin):
            continue
        gentauPt_.append(treeIn.genTauPt[i])
        gentauEta_.append(treeIn.genTauEta[i])
        gentauPhi_.append(treeIn.genTauPhi[i])
        #Nvtx_.append(treeIn.l1VertexN)
        Ngentau_ = Ngentau_ + 1

    l1TauPt_ = []
    l1TauEta_ = []
    l1TauPhi_ = []
    l1TauZ_ = []
    Nl1Tau_ = 0
    isL1TauPair = False
    #isL1TauPair = True
    if(l1tauType=="NN"):
        for j in range(0, treeIn.l1nnTauPt.size()):
            if(treeIn.l1nnTauLooseIso[j]==0):
                continue
            if(treeIn.l1nnTauPt[j] < L1NNTauPtMin):
                continue
            l1TauPt_.append(treeIn.l1nnTauPt[j])
            l1TauEta_.append(treeIn.l1nnTauEta[j])
            l1TauPhi_.append(treeIn.l1nnTauPhi[j])
            l1TauZ_.append(treeIn.l1nnTauZ[j])
            Nl1Tau_ = Nl1Tau_ + 1
        if Nl1Tau_ >= 2:
            for i in range(0, Nl1Tau_):
                for j in range(0, Nl1Tau_):
                    if i == j:
                        continue
                    DeltaR = math.sqrt((l1TauEta_[i] - l1TauEta_[j])**2 + (l1TauPhi_[i] - l1TauPhi_[j])**2)
                    if DeltaR > 0.5:
                        isL1TauPair = True
    elif(l1tauType=="HPS"):
        for j in range(0, treeIn.l1hpsTauPt.size()):
            if(treeIn.l1hpsTauTightRelIso[j]==0):
                continue
            if(treeIn.l1hpsTauPt[j] < L1HPSTauPtMin):
                continue
            l1TauPt_.append(treeIn.l1hpsTauPt[j])
            l1TauEta_.append(treeIn.l1hpsTauEta[j])
            l1TauPhi_.append(treeIn.l1hpsTauPhi[j])
            l1TauZ_.append(treeIn.l1hpsTauZ[j])
            Nl1Tau_ = Nl1Tau_ + 1
        if Nl1Tau_ >= 2:
            for i in range(0, Nl1Tau_):
                for j in range(0, Nl1Tau_):
                    if i == j:
                        continue
                    dZ = l1TauZ_[i] - l1TauZ_[j]
                    if dZ < 0.4:
                        isL1TauPair = True
    hltTauPt_ = []
    hltTauEta_ = []
    hltTauPhi_ = []
    hltTauNoCut_ = []
    hltTaudZ_ = []
    hltTauVLoose_ = []
    hltTauLoose_ = []
    hltTauMedium_ = []
    hltTauTight_ = []
    hltTauZ_ = []
    NhltTau_ = 0

    # CV: read HLTTau information from TTree
    for i in range(0, treeIn.hltTauPt.size()):
        isHLTmatchedL1 = False
        if(l1tauType=="NN" or l1tauType=="HPS"):
            #if(isL1TauPair == True):
            for j in range(0, Nl1Tau_):
                DeltaR = math.sqrt((treeIn.hltTauEta[i] - l1TauEta_[j])**2 + (treeIn.hltTauPhi[i] - l1TauPhi_[j])**2)
                if DeltaR < 0.5:
                    isHLTmatchedL1 = True
        if(l1tauType=="HLT"):
            isHLTmatchedL1 = True
        if (isHLTmatchedL1==False):
            continue
        if (treeIn.hltTauLeadTrackPt < double(tauLeadTrack_Pt_min)):
            continue
        hltTauPt_.append(treeIn.hltTauPt[i])
        hltTauEta_.append(treeIn.hltTauEta[i])
        hltTauPhi_.append(treeIn.hltTauPhi[i]) 
        hltTauNoCut_.append(1)
        hltTaudZ_.append(1 if treeIn.hltTauPt[i] > (double)(pt_Threshold_dZ) else 0)
        if(isolation=="ChargedIso"):
            hltTauVLoose_.append(1 if treeIn.hltTauVLooseRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_VLoose) else 0)
            hltTauLoose_.append(1 if treeIn.hltTauLooseRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Loose) else 0)
            hltTauMedium_.append(1 if treeIn.hltTauMediumRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Medium) else 0)
            hltTauTight_.append(1 if treeIn.hltTauTightRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Tight) else 0)
        if(isolation=="DeepTau"):
            hltTauVLoose_.append(1 if treeIn.hltTauIso[i] > 0.1 and treeIn.hltTauPt[i] > (double)(pt_Threshold_VLoose) else 0)
            hltTauLoose_.append(1 if treeIn.hltTauIso[i] > 0.2 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Loose) else 0)
            hltTauMedium_.append(1 if treeIn.hltTauIso[i] > 0.3 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Medium) else 0)
            hltTauTight_.append(1 if treeIn.hltTauIso[i] > 0.35 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Tight) else 0)

        hltTauZ_.append(treeIn.hltTauZ[i])
        NhltTau_ = NhltTau_ + 1

    genTauToHLTTauMap = {} # key = index in gentau collection, value = index in hltTau collection

    for i in range(0, Ngentau_):

        minDeltaR = 0.5 # CV: maximum eta-phi distance for matching gentau to hltTau collection
        match = None
        for j in range(0, NhltTau_):
            DeltaR = math.sqrt((gentauEta_[i] - hltTauEta_[j])**2 + (gentauPhi_[i] - hltTauPhi_[j])**2)
            if DeltaR < minDeltaR:
                minDeltaR = DeltaR
                match = j

        genTauToHLTTauMap[i] = match

    pt_Threshold_tag = 20.0
    hltTau_tag = hltTauLoose_ 

    if Ngentau_ >0:
        for i in range(0, Ngentau_): 
            hist_GenHLTTau_Pt_Denominator.Fill(gentauPt_[i])
            #print "i ", i, " gentauPt_ ", gentauPt_[i]
            hlt = genTauToHLTTauMap[i]
            #print "hlt ", hlt
            if hlt is not None:
                if (hltTauVLoose_[hlt] == 1):
                    hist_GenHLTTau_Pt_Numerator_VLoose.Fill(gentauPt_[i])
                if (hltTauLoose_[hlt] == 1):
                    hist_GenHLTTau_Pt_Numerator_Loose.Fill(gentauPt_[i])
                if (hltTauMedium_[hlt] == 1):
                    hist_GenHLTTau_Pt_Numerator_Medium.Fill(gentauPt_[i])
                if (hltTauTight_[hlt] == 1):
                    hist_GenHLTTau_Pt_Numerator_Tight.Fill(gentauPt_[i])


    # For L1 Tau pair with dz or dR criteria
    hlt2TauPt_ = []
    hlt2TauEta_ = []
    hlt2TauPhi_ = []
    hlt2TauNoCut_ = []
    hlt2TaudZ_ = []
    hlt2TauVLoose_ = []
    hlt2TauLoose_ = []
    hlt2TauMedium_ = []
    hlt2TauTight_ = []
    hlt2TauZ_ = []
    Nhlt2Tau_ = 0
    for i in range(0, treeIn.hltTauPt.size()):
        isHLTmatchedL1 = True
        if(l1tauType=="NN" or l1tauType=="HPS"):
            if(isL1TauPair == True):
                for j in range(0, Nl1Tau_):
                    DeltaR = math.sqrt((treeIn.hltTauEta[i] - l1TauEta_[j])**2 + (treeIn.hltTauPhi[i] - l1TauPhi_[j])**2)
                    if DeltaR < 0.5:
                        isHLTmatchedL1 = True
        if(l1tauType=="HLT"):
            isHLTmatchedL1 = True
        if (isHLTmatchedL1==False):
            continue
        if (treeIn.hltTauLeadTrackPt < double(tauLeadTrack_Pt_min)):
            continue
        hlt2TauPt_.append(treeIn.hltTauPt[i])
        hlt2TauEta_.append(treeIn.hltTauEta[i])
        hlt2TauPhi_.append(treeIn.hltTauPhi[i])
        hlt2TauNoCut_.append(1)
        hlt2TaudZ_.append(1 if treeIn.hltTauPt[i] > (double)(pt_Threshold_dZ) else 0)
        if(isolation=="ChargedIso"):
            hlt2TauVLoose_.append(1 if treeIn.hltTauVLooseRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_VLoose) else 0)
            hlt2TauLoose_.append(1 if treeIn.hltTauLooseRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Loose) else 0)
            hlt2TauMedium_.append(1 if treeIn.hltTauMediumRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Medium) else 0)
            hlt2TauTight_.append(1 if treeIn.hltTauTightRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Tight) else 0)
        if(isolation=="DeepTau"):
            hlt2TauVLoose_.append(1 if treeIn.hltTauIso[i] > 0.1 and treeIn.hltTauPt[i] > (double)(pt_Threshold_VLoose) else 0)
            hlt2TauLoose_.append(1 if treeIn.hltTauIso[i] > 0.2 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Loose) else 0)
            hlt2TauMedium_.append(1 if treeIn.hltTauIso[i] > 0.3 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Medium) else 0)
            hlt2TauTight_.append(1 if treeIn.hltTauIso[i] > 0.35 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Tight) else 0)

        hlt2TauZ_.append(treeIn.hltTauZ[i])
        Nhlt2Tau_ = Nhlt2Tau_ + 1

    genTauToHLT2TauMap = {} # key = index in gentau collection, value = index in hltTau collection 
    for i in range(0, Ngentau_):
        minDeltaR = 0.5 # CV: maximum eta-phi distance for matching gentau to hltTau collection 
        match = None
        for j in range(0, Nhlt2Tau_):
            DeltaR = math.sqrt((gentauEta_[i] - hlt2TauEta_[j])**2 + (gentauPhi_[i] - hlt2TauPhi_[j])**2)
            if DeltaR < minDeltaR:
                minDeltaR = DeltaR
                match = j
        genTauToHLT2TauMap[i] = match


    if Ngentau_ == 2:
        for itag in range(0, Ngentau_):
            jtag = genTauToHLT2TauMap[itag]
            if jtag is None:
                continue
            for iprobe in range(0, Ngentau_):
                if itag == iprobe:
                    continue
                jprobe = genTauToHLT2TauMap[iprobe]
                if jprobe is None:
                    continue
                if (hlt2TauVLoose_[jtag] == 1 and hlt2TauVLoose_[jprobe] == 1):
                    hist_GenHLTTau_Pt_2D_Denominator_VLoose.Fill(gentauPt_[itag], gentauPt_[iprobe])
                    if (Is_dZPass(hlt2TauPt_[jtag], hlt2TauZ_[jtag], hlt2TauPt_[jprobe], hlt2TauZ_[jprobe])):
                        hist_GenHLTTau_Pt_2D_Numerator_VLoose.Fill(gentauPt_[itag], gentauPt_[iprobe])
                if (hlt2TauLoose_[jtag] == 1 and hlt2TauLoose_[jprobe] == 1):
                    hist_GenHLTTau_Pt_2D_Denominator_Loose.Fill(gentauPt_[itag], gentauPt_[iprobe])
                    if (Is_dZPass(hlt2TauPt_[jtag], hlt2TauZ_[jtag], hlt2TauPt_[jprobe], hlt2TauZ_[jprobe])):
                        hist_GenHLTTau_Pt_2D_Numerator_Loose.Fill(gentauPt_[itag], gentauPt_[iprobe])
                if (hlt2TauMedium_[jtag] == 1 and hlt2TauMedium_[jprobe] == 1):
                    hist_GenHLTTau_Pt_2D_Denominator_Medium.Fill(gentauPt_[itag], gentauPt_[iprobe])
                    if (Is_dZPass(hlt2TauPt_[jtag], hlt2TauZ_[jtag], hlt2TauPt_[jprobe], hlt2TauZ_[jprobe])):
                        hist_GenHLTTau_Pt_2D_Numerator_Medium.Fill(gentauPt_[itag], gentauPt_[iprobe])
                if (hlt2TauTight_[jtag] == 1 and hlt2TauTight_[jprobe] == 1):
                    hist_GenHLTTau_Pt_2D_Denominator_Tight.Fill(gentauPt_[itag], gentauPt_[iprobe])
                    if (Is_dZPass(hlt2TauPt_[jtag], hlt2TauZ_[jtag], hlt2TauPt_[jprobe], hlt2TauZ_[jprobe])):
                        hist_GenHLTTau_Pt_2D_Numerator_Tight.Fill(gentauPt_[itag], gentauPt_[iprobe])
#        treeOut.Fill()
hist_GenHLTTau_Pt_Efficiency_VLoose.Divide(hist_GenHLTTau_Pt_Numerator_VLoose, hist_GenHLTTau_Pt_Denominator)
hist_GenHLTTau_Pt_Efficiency_Loose.Divide(hist_GenHLTTau_Pt_Numerator_Loose, hist_GenHLTTau_Pt_Denominator)
hist_GenHLTTau_Pt_Efficiency_Medium.Divide(hist_GenHLTTau_Pt_Numerator_Medium, hist_GenHLTTau_Pt_Denominator)
hist_GenHLTTau_Pt_Efficiency_Tight.Divide(hist_GenHLTTau_Pt_Numerator_Tight, hist_GenHLTTau_Pt_Denominator)

hist_GenHLTTau_Pt_2D_Efficiency_VLoose.Divide(hist_GenHLTTau_Pt_2D_Numerator_VLoose, hist_GenHLTTau_Pt_2D_Denominator_VLoose)
hist_GenHLTTau_Pt_2D_Efficiency_Loose.Divide(hist_GenHLTTau_Pt_2D_Numerator_Loose, hist_GenHLTTau_Pt_2D_Denominator_Loose)
hist_GenHLTTau_Pt_2D_Efficiency_Medium.Divide(hist_GenHLTTau_Pt_2D_Numerator_Medium, hist_GenHLTTau_Pt_2D_Denominator_Medium)
hist_GenHLTTau_Pt_2D_Efficiency_Tight.Divide(hist_GenHLTTau_Pt_2D_Numerator_Tight, hist_GenHLTTau_Pt_2D_Denominator_Tight)

Nbin = hist_GenHLTTau_Pt_Efficiency_VLoose.GetNbinsX()
print hist_GenHLTTau_Pt_2D_Numerator_VLoose.GetBinContent(1,10), " ", hist_GenHLTTau_Pt_2D_Numerator_VLoose.GetBinContent(1, 20), " ", hist_GenHLTTau_Pt_2D_Numerator_VLoose.GetBinContent(1, 30)
for i in range(1, Nbin):
    Tau1Pt = i
    print "Tau1Pt ", Tau1Pt, " i ", i
    sum_Numerator_VLoose = 0
    sum_Denominator_VLoose = 0
    for j in range(1, Nbin):
        Tau2Pt = j
        Numerator_VLoose = hist_GenHLTTau_Pt_2D_Numerator_VLoose.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Numerator_VLoose += Numerator_VLoose
        Denominator_VLoose = hist_GenHLTTau_Pt_2D_Denominator_VLoose.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Denominator_VLoose += Denominator_VLoose
        print "Numerator_VLoose ", Numerator_VLoose, " sum_Numerator_VLoose ",sum_Numerator_VLoose, " Denominator_VLoose ", Denominator_VLoose, " sum_Denominator_VLoose ", sum_Denominator_VLoose
    if sum_Denominator_VLoose == 0:
        sum_Denominator_VLoose = 1
    efficiency_VLoose = sum_Numerator_VLoose/sum_Denominator_VLoose
    hist_GenHLTTau_Pt_1D_Efficiency_VLoose.SetBinContent(Tau1Pt, efficiency_VLoose)
    sum_Numerator_Loose = 0
    sum_Denominator_Loose = 0
    for j in range(1, Nbin):
        Tau2Pt = j
        Numerator_Loose = hist_GenHLTTau_Pt_2D_Numerator_Loose.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Numerator_Loose +=Numerator_Loose
        Denominator_Loose = hist_GenHLTTau_Pt_2D_Denominator_Loose.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Denominator_Loose += Denominator_Loose
    if sum_Denominator_Loose == 0:
        sum_Denominator_Loose = 1
    efficiency_Loose =sum_Numerator_Loose/sum_Denominator_Loose
    hist_GenHLTTau_Pt_1D_Efficiency_Loose.SetBinContent(Tau1Pt, efficiency_Loose)
    sum_Numerator_Medium = 0
    sum_Denominator_Medium = 0
    for j in range(1, Nbin):
        Tau2Pt = j
        Numerator_Medium = hist_GenHLTTau_Pt_2D_Numerator_Medium.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Numerator_Medium +=Numerator_Medium
        Denominator_Medium = hist_GenHLTTau_Pt_2D_Denominator_Medium.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Denominator_Medium += Denominator_Medium
    if sum_Denominator_Medium == 0:
        sum_Denominator_Medium = 1
    efficiency_Medium =sum_Numerator_Medium/sum_Denominator_Medium
    hist_GenHLTTau_Pt_1D_Efficiency_Medium.SetBinContent(Tau1Pt, efficiency_Medium)
    sum_Numerator_Tight = 0
    sum_Denominator_Tight = 0
    for j in range(1, Nbin):
        Tau2Pt = j
        Numerator_Tight = hist_GenHLTTau_Pt_2D_Numerator_Tight.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Numerator_Tight +=Numerator_Tight
        Denominator_Tight = hist_GenHLTTau_Pt_2D_Denominator_Tight.GetBinContent(Tau1Pt, Tau2Pt)
        sum_Denominator_Tight += Denominator_Tight
    if sum_Denominator_Tight == 0:
        sum_Denominator_Tight = 1
    efficiency_Tight =sum_Numerator_Tight/sum_Denominator_Tight
    hist_GenHLTTau_Pt_1D_Efficiency_Tight.SetBinContent(Tau1Pt, efficiency_Tight)



for i in range(1, Nbin):
    efficiencySingleTau_VLoose = hist_GenHLTTau_Pt_Efficiency_VLoose.GetBinContent(i)
    efficiency_dZ_VLoose = hist_GenHLTTau_Pt_2D_Efficiency_VLoose.GetBinContent(i, i)
    efficiency_VLoose = efficiencySingleTau_VLoose*math.sqrt(efficiency_dZ_VLoose)
    print "i= ", i, " efficiencySingleTau_VLoose ", efficiencySingleTau_VLoose, "  efficiency_dZ_VLoose ", efficiency_dZ_VLoose, " efficiency_VLoose ", efficiency_VLoose
    hist_GenHLTTau_Pt_Efficiency_with_dZ_VLoose.SetBinContent(i, efficiency_VLoose)

    efficiencySingleTau_Loose = hist_GenHLTTau_Pt_Efficiency_Loose.GetBinContent(i)
    efficiency_dZ_Loose = hist_GenHLTTau_Pt_2D_Efficiency_Loose.GetBinContent(i, i)
    efficiency_Loose = efficiencySingleTau_Loose*math.sqrt(efficiency_dZ_Loose)
    hist_GenHLTTau_Pt_Efficiency_with_dZ_Loose.SetBinContent(i, efficiency_Loose)

    efficiencySingleTau_Medium = hist_GenHLTTau_Pt_Efficiency_Medium.GetBinContent(i)
    efficiency_dZ_Medium = hist_GenHLTTau_Pt_2D_Efficiency_Medium.GetBinContent(i, i)
    efficiency_Medium = efficiencySingleTau_Medium*math.sqrt(efficiency_dZ_Medium)
    hist_GenHLTTau_Pt_Efficiency_with_dZ_Medium.SetBinContent(i, efficiency_Medium)

    efficiencySingleTau_Tight = hist_GenHLTTau_Pt_Efficiency_Tight.GetBinContent(i)
    efficiency_dZ_Tight = hist_GenHLTTau_Pt_2D_Efficiency_Tight.GetBinContent(i, i)
    efficiency_Tight = efficiencySingleTau_Tight*math.sqrt(efficiency_dZ_Tight)
    hist_GenHLTTau_Pt_Efficiency_with_dZ_Tight.SetBinContent(i, efficiency_Tight)




#treeOut.Write()
fileOut.Write()
#fileOut.Close()
