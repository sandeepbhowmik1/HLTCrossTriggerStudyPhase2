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

fileName_In = "/home/sbhowmik/RootTree/HLTTau/Phase2/rootTree_test_L1andHLTTauAnalyzer_Signal_VBFHToTauTau_DeepTau_20210208.root"
treeName_In = "L1andHLTTauAnalyzer/L1andHLTTauAnalyzer"
fileName_In_txt = "/home/sbhowmik/HLTTau/HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/ratePlot/results/hist_Rate_for_HPSL1andHLTTau_Background_DeepTau_All_Stitching_20211012.txt"
fileName_Out = "/home/sbhowmik/RootTree/HLTTau/Phase2/rootTree_Signal_Efficiency_for_Double_Gen_HPSL1andHLTTau_DeepTau_All_Stitching_20211012.root"
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

#pt_Threshold_NoCut = 30.0
#pt_Threshold_dZ = 30.0
#pt_Threshold_VLoose = 30.0
#pt_Threshold_Loose = 30.0
#pt_Threshold_Medium = 30.0
#pt_Threshold_Tight = 30.0

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

    if Ngentau_ > 0:
        for itag in range(0, Ngentau_): 
            tauPt[0] = gentauPt_[itag]
            tauEta[0] = gentauEta_[itag]
            tauPhi[0] = gentauPhi_[itag]
            #Nvtx[0] = Nvtx_[itag]
            hltTauPt[0] = -1
            hltTauEta[0] = -5
            hltTauPhi[0] = -5
            hltTauNoCut[0] = 0
            hltTaudZ[0] = 0
            hltTauVLoose[0] = 0
            hltTauLoose[0] = 0
            hltTauMedium[0] = 0
            hltTauTight[0] = 0

            jtag = genTauToHLTTauMap[itag]
            if jtag is not None:           
                hltTauPt[0] = hltTauPt_[jtag]
                hltTauEta[0] = hltTauEta_[jtag]
                hltTauPhi[0] = hltTauPhi_[jtag]
                hltTauNoCut[0] = hltTauNoCut_[jtag]
                hltTaudZ[0] = hltTaudZ_[jtag]
                hltTauVLoose[0] = hltTauVLoose_[jtag]
                hltTauLoose[0] = hltTauLoose_[jtag]
                hltTauMedium[0] = hltTauMedium_[jtag]
                hltTauTight[0] = hltTauTight_[jtag]

            treeOut.Fill()

treeOut.Write()
fileOut.Close()
