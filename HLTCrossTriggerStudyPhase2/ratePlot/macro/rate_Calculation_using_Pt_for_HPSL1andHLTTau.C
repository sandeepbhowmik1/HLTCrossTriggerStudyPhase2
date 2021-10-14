#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <iostream>
#include <TLorentzVector.h>
#include <TH1.h>
#include <TH2.h>
#include <TH3.h>
#include <TMath.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TStyle.h>
#include <TROOT.h>
#include <sstream>
#include <TBranchElement.h>
#include <fstream>
#include <map>

using namespace std;

void rate_Calculation_using_Pt_for_HPSL1andHLTTau()
{
  TString fileName_In = "/home/sbhowmik/RootTree/HLTTau/Phase2/rootTree_test_L1andHLTTauAnalyzer_Background_DeepTau_Stitching_20210611_2.root";
  TString treeName_In = "L1andHLTTauAnalyzer/L1andHLTTauAnalyzer"; 
  TString fileName_Out = "/home/sbhowmik/HLTTau/HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/ratePlot/results/hist_Rate_for_HPSL1andHLTTau_Background_DeepTau_All_Stitching_20211012.root";
  TString isolation = "DeepTau";
  TString etaRange =  "All";
  TString weight = "Stitching";
//void rate_Calculation_using_Pt_for_HPSL1andHLTTau(TString fileName_In, TString treeName_In, TString fileName_Out, TString isolation, TString etaRange, TString weight)
//{
  double targetRate_singleTau = 500.0 ; //Hz
  double targetRate_DoubleoTau = 170.0 ; //Hz 
  double tau_eta_min = 0;
  double tau_eta_max = 0;
  if (etaRange == "Barrel"){
    tau_eta_min = 0;
    tau_eta_max = 1.5;
  }else if (etaRange == "Endcap"){
    tau_eta_min = 1.5;
    tau_eta_max = 2.4;
  }else{
    tau_eta_min = 0;
    tau_eta_max = 2.1;
  }
  double tau_Pt_min = 0.0;
  //double l1Tau_Pt_min = 17.0; // DoubleTau Tight 5917 Hz 17 GeV
  double l1Tau_Pt_min = 21.0; // DoubleTau Tight 8.93 kHz 21 GeV  
  double tauLeadTrack_Pt_min = 5.0;
  double dzMax = 0.20;
  double dzMax_L1Taus = 0.40;
  //float freq = 434.625; // for DYToLL-M50
  //float freq = 4274.25; // for WJetsToLNu
  //float freq = 73.8375; //for TT
  float freq = 28.0E6;
  float pu = 200;
  float scale = freq;
  Int_t Denominator = 0;
  double Weight =1;
  double deltaR_max = 0.5;
  double deepTau_VLoose = 0.10;
  double deepTau_Loose = 0.20;
  double deepTau_Medium = 0.30;
  double deepTau_Tight = 0.350;

  TFile fileIn(fileName_In.Data(),"READ");
  TTree* treeIn = (TTree*)fileIn.Get(treeName_In);
  TFile fileOut(fileName_Out, "RECREATE");
  TTree* treeOut = new TTree("HLTTauAnalyzer", "HLTTauAnalyzer");
  char outfile[200];
  char outfilx[200];
  int len = strlen(fileName_Out);
  strncpy(outfilx, fileName_Out, len-4);
  outfilx[len-4]='\0';
  sprintf (outfile,"%stxt",outfilx);
  ofstream fileOut_txt(outfile);

  ULong64_t       EventNumber =  0;
  Int_t           RunNumber =  0;
  Int_t           lumi =  0;
  vector<float>   *hltTauPt =  0;
  vector<float>   *hltTauEta =  0;
  vector<float>   *hltTauPhi =  0;
  vector<int>   *hltTauTightIso =  0;
  vector<int>   *hltTauMediumIso =  0;
  vector<int>   *hltTauLooseIso =  0;
  vector<int>   *hltTauVLooseIso =  0;
  vector<int>   *hltTauTightRelIso =  0;
  vector<int>   *hltTauMediumRelIso =  0;
  vector<int>   *hltTauLooseRelIso =  0;
  vector<int>   *hltTauVLooseRelIso =  0;
  vector<float>   *hltTauZ =  0;
  vector<float>   *hltTauLeadTrackPt =  0;
  double         stitching_weight = 1;
  vector<float>   *hltTauIso = 0;

  vector<float>   *l1hpsTauPt =  0;
  vector<float>   *l1hpsTauEta =  0;
  vector<float>   *l1hpsTauPhi =  0;
  vector<int>   *l1hpsTauTightIso =  0;
  vector<int>   *l1hpsTauMediumIso =  0;
  vector<int>   *l1hpsTauLooseIso =  0;
  vector<int>   *l1hpsTauVLooseIso =  0;
  vector<int>   *l1hpsTauTightRelIso =  0;
  vector<int>   *l1hpsTauMediumRelIso =  0;
  vector<int>   *l1hpsTauLooseRelIso =  0;
  vector<int>   *l1hpsTauVLooseRelIso =  0;
  vector<float>   *l1hpsTauZ =  0;
  vector<float>   *l1hpsTauLeadTrackPt =  0;
  vector<float>   *l1hpsTauIso = 0;

  treeIn->SetBranchAddress("EventNumber", &EventNumber);
  treeIn->SetBranchAddress("RunNumber", &RunNumber);
  treeIn->SetBranchAddress("lumi", &lumi);
  treeIn->SetBranchAddress("hltTauPt", &hltTauPt);
  treeIn->SetBranchAddress("hltTauEta", &hltTauEta);
  treeIn->SetBranchAddress("hltTauPhi", &hltTauPhi);
  treeIn->SetBranchAddress("hltTauTightIso", &hltTauTightIso);
  treeIn->SetBranchAddress("hltTauMediumIso", &hltTauMediumIso);
  treeIn->SetBranchAddress("hltTauLooseIso", &hltTauLooseIso);
  treeIn->SetBranchAddress("hltTauVLooseIso", &hltTauVLooseIso);
  treeIn->SetBranchAddress("hltTauTightRelIso", &hltTauTightRelIso);
  treeIn->SetBranchAddress("hltTauMediumRelIso", &hltTauMediumRelIso);
  treeIn->SetBranchAddress("hltTauLooseRelIso", &hltTauLooseRelIso);
  treeIn->SetBranchAddress("hltTauVLooseRelIso", &hltTauVLooseRelIso);
  treeIn->SetBranchAddress("hltTauZ", &hltTauZ);
  treeIn->SetBranchAddress("hltTauLeadTrackPt", &hltTauLeadTrackPt);
  treeIn->SetBranchAddress("stitching_weight", &stitching_weight);
  treeIn->SetBranchAddress("hltTauIso", &hltTauIso);

  treeIn->SetBranchAddress("l1hpsTauPt", &l1hpsTauPt);
  treeIn->SetBranchAddress("l1hpsTauEta", &l1hpsTauEta);
  treeIn->SetBranchAddress("l1hpsTauPhi", &l1hpsTauPhi);
  treeIn->SetBranchAddress("l1hpsTauTightIso", &l1hpsTauTightIso);
  treeIn->SetBranchAddress("l1hpsTauMediumIso", &l1hpsTauMediumIso);
  treeIn->SetBranchAddress("l1hpsTauLooseIso", &l1hpsTauLooseIso);
  treeIn->SetBranchAddress("l1hpsTauVLooseIso", &l1hpsTauVLooseIso);
  treeIn->SetBranchAddress("l1hpsTauTightRelIso", &l1hpsTauTightRelIso);
  treeIn->SetBranchAddress("l1hpsTauMediumRelIso", &l1hpsTauMediumRelIso);
  treeIn->SetBranchAddress("l1hpsTauLooseRelIso", &l1hpsTauLooseRelIso);
  treeIn->SetBranchAddress("l1hpsTauVLooseRelIso", &l1hpsTauVLooseRelIso);
  treeIn->SetBranchAddress("l1hpsTauZ", &l1hpsTauZ);
  treeIn->SetBranchAddress("l1hpsTauLeadTrackPt", &l1hpsTauLeadTrackPt);
  treeIn->SetBranchAddress("l1hpsTauIso", &l1hpsTauIso);

  treeOut -> Branch("EventNumber",&EventNumber,"EventNumber/l");
  treeOut -> Branch("RunNumber",&RunNumber,"RunNumber/I");
  treeOut -> Branch("lumi",&lumi,"lumi/I");

  TH1F* hist_Single_hltTauPt_NoCut    = new TH1F("Pt_Single_HLTTau_NoCut","Pt_Single_HLTTau_NoCut",250,0.,250.);
  TH1F* hist_Single_hltTauPt_dZ        = new TH1F("Pt_Single_HLTTau_dZ","Pt_Single_HLTTau_dZ",250,0.,250.);
  TH1F* hist_Single_hltTauPt_Tight     = new TH1F("Pt_Single_HLTTau_Tight","Pt_Single_HLTTau_Tight",250,0.,250.);
  TH1F* hist_Single_hltTauPt_Medium    = new TH1F("Pt_Single_HLTTau_Medium","Pt_Single_HLTTau_Medium",250,0.,250.);
  TH1F* hist_Single_hltTauPt_Loose     = new TH1F("Pt_Single_HLTTau_Loose","Pt_Single_HLTTau_Loose",250,0.,250.);
  TH1F* hist_Single_hltTauPt_VLoose    = new TH1F("Pt_Single_HLTTau_VLoose","Pt_Single_HLTTau_VLoose",250,0.,250.);

  TH1F* hist_Rate_Single_hltTauPt_NoCut    = new TH1F("Rate_Single_HLTTau_NoCut","Rate_Single_HLTTau_NoCut",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_dZ        = new TH1F("Rate_Single_HLTTau_dZ","Rate_Single_HLTTau_dZ",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_Tight     = new TH1F("Rate_Single_HLTTau_Tight","Rate_Single_HLTTau_Tight",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_Medium    = new TH1F("Rate_Single_HLTTau_Medium","Rate_Single_HLTTau_Medium",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_Loose     = new TH1F("Rate_Single_HLTTau_Loose","Rate_Single_HLTTau_Loose",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_VLoose    = new TH1F("Rate_Single_HLTTau_VLoose","Rate_Single_HLTTau_VLoose",250,0.,250.);

  TH2F* hist_Double_hltTauPt_NoCut    = new TH2F("Pt_Double_HLTTau_NoCut","Pt_Double_HLTTau_NoCut",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_dZ        = new TH2F("Pt_Double_HLTTau_dZ","Pt_Double_HLTTau_dZ",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_Tight     = new TH2F("Pt_Double_HLTTau_Tight","Pt_Double_HLTTau_Tight",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_Medium    = new TH2F("Pt_Double_HLTTau_Medium","Pt_Double_HLTTau_Medium",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_Loose     = new TH2F("Pt_Double_HLTTau_Loose","Pt_Double_HLTTau_Loose",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_VLoose    = new TH2F("Pt_Double_HLTTau_VLoose","Pt_Double_HLTTau_VLoose",250,0.,250., 250,0.,250.);

  TH1F* hist_Rate_Double_hltTauPt_NoCut    = new TH1F("Rate_Double_HLTTau_NoCut","Rate_Double_HLTTau_NoCut",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_dZ        = new TH1F("Rate_Double_HLTTau_dZ","Rate_Double_HLTTau_dZ",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_Tight     = new TH1F("Rate_Double_HLTTau_Tight","Rate_Double_HLTTau_Tight",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_Medium    = new TH1F("Rate_Double_HLTTau_Medium","Rate_Double_HLTTau_Medium",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_Loose     = new TH1F("Rate_Double_HLTTau_Loose","Rate_Double_HLTTau_Loose",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_VLoose    = new TH1F("Rate_Double_HLTTau_VLoose","Rate_Double_HLTTau_VLoose",250,0.,250.);

  bool firstTrue_SingleTau_NoCut = true;
  bool firstTrue_SingleTau_dZ = true;
  bool firstTrue_SingleTau_VLoose = true;
  bool firstTrue_SingleTau_Loose = true;
  bool firstTrue_SingleTau_Medium = true;
  bool firstTrue_SingleTau_Tight = true;

  bool firstTrue_DoubleTau_NoCut = true;
  bool firstTrue_DoubleTau_dZ = true;
  bool firstTrue_DoubleTau_VLoose = true;
  bool firstTrue_DoubleTau_Loose = true;
  bool firstTrue_DoubleTau_Medium = true;
  bool firstTrue_DoubleTau_Tight = true;

  for(UInt_t i_event = 0 ; i_event < treeIn->GetEntries() ; ++i_event){
    treeIn->GetEntry(i_event);
    //if(i_event%10000==0) cout<<"Entry #"<<i_event<<endl; 

    ++Denominator;

    if(weight == "Stitching"){
      Weight = stitching_weight;
    }else{
      Weight=1;
    }

    // Start For Single Tau
    float max_HLTTau_Pt_NoCut = 0.;
    float max_HLTTau_Pt_dZ = 0.;
    float max_HLTTau_Pt_Tight = 0.;
    float max_HLTTau_Pt_Medium = 0.;
    float max_HLTTau_Pt_Loose = 0.;
    float max_HLTTau_Pt_VLoose = 0.;

    for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
      if(fabs(hltTauEta->at(iHLTTau))>tau_eta_max) continue;
      if(fabs(hltTauEta->at(iHLTTau))<tau_eta_min) continue;
      if (hltTauPt->at(iHLTTau) <= tau_Pt_min) continue;
      if (hltTauLeadTrackPt->at(iHLTTau) <= tauLeadTrack_Pt_min) continue;

      for(UInt_t mL1HPSTau = 0; mL1HPSTau < l1hpsTauPt->size(); ++mL1HPSTau){
        if (!l1hpsTauTightRelIso->at(mL1HPSTau)) continue;
        double deltaR = sqrt(pow((hltTauEta->at(iHLTTau) - l1hpsTauEta->at(mL1HPSTau)),2) + pow((hltTauPhi->at(iHLTTau) - l1hpsTauPhi->at(mL1HPSTau)),2));
        if (deltaR > deltaR_max) continue;

	if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_NoCut ) max_HLTTau_Pt_NoCut = hltTauPt->at(iHLTTau);
	if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_dZ ) max_HLTTau_Pt_dZ = hltTauPt->at(iHLTTau);
	if (((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > 0.8)) || ((isolation=="ChargedIso") && (hltTauTightRelIso->at(iHLTTau)==1))){
	  if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_Tight ) max_HLTTau_Pt_Tight = hltTauPt->at(iHLTTau);
	}
	if (((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > 0.7)) || ((isolation=="ChargedIso") && (hltTauMediumRelIso->at(iHLTTau)==1))){
	  if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_Medium ) max_HLTTau_Pt_Medium = hltTauPt->at(iHLTTau);
	}
	if (((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > 0.6)) || ((isolation=="ChargedIso") && (hltTauLooseRelIso->at(iHLTTau)==1))){
	  if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_Loose ) max_HLTTau_Pt_Loose = hltTauPt->at(iHLTTau);
	}
	if (((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > 0.5)) || ((isolation=="ChargedIso") && (hltTauVLooseRelIso->at(iHLTTau)==1))){
	  if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_VLoose ) max_HLTTau_Pt_VLoose = hltTauPt->at(iHLTTau);
	}
      }
    }
    if(max_HLTTau_Pt_NoCut!=0){
      hist_Single_hltTauPt_NoCut->Fill(max_HLTTau_Pt_NoCut, Weight);
    }
    if(max_HLTTau_Pt_dZ!=0){
      hist_Single_hltTauPt_dZ->Fill(max_HLTTau_Pt_dZ, Weight);
    }
    if(max_HLTTau_Pt_Tight!=0){
      hist_Single_hltTauPt_Tight->Fill(max_HLTTau_Pt_Tight, Weight);
    }
    if(max_HLTTau_Pt_Medium!=0){
      hist_Single_hltTauPt_Medium->Fill(max_HLTTau_Pt_Medium, Weight);
    }
    if(max_HLTTau_Pt_Loose!=0){
      hist_Single_hltTauPt_Loose->Fill(max_HLTTau_Pt_Loose, Weight);
    }
    if(max_HLTTau_Pt_VLoose!=0){
      hist_Single_hltTauPt_VLoose->Fill(max_HLTTau_Pt_VLoose, Weight);
    }
    // End For Single Tau 
    
    
    // Start For Di Tau
 
    bool isFilled_NoCut=false;
    bool isFilled_dZ=false;
    bool isFilled_Tight=false;
    bool isFilled_Medium=false;
    bool isFilled_Loose=false;
    bool isFilled_VLoose=false;
    bool isFilled_Tight_Pt40=false;
    
    for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
      if(fabs(hltTauEta->at(iHLTTau))>tau_eta_max) continue;
      if(fabs(hltTauEta->at(iHLTTau))<tau_eta_min) continue;
      if (hltTauPt->at(iHLTTau) <= tau_Pt_min) continue;
      if (hltTauLeadTrackPt->at(iHLTTau) <= tauLeadTrack_Pt_min) continue;

      int rank_mL1HPSTau = -1;
      for(UInt_t mL1HPSTau = 0; mL1HPSTau < l1hpsTauPt->size(); ++mL1HPSTau){
	if (!l1hpsTauTightRelIso->at(mL1HPSTau)) continue;
	if (l1hpsTauPt->at(mL1HPSTau) <= l1Tau_Pt_min) continue;
	double deltaR = sqrt(pow((hltTauEta->at(iHLTTau) - l1hpsTauEta->at(mL1HPSTau)),2) + pow((hltTauPhi->at(iHLTTau) - l1hpsTauPhi->at(mL1HPSTau)),2));
	if (deltaR > deltaR_max) continue;
	rank_mL1HPSTau = mL1HPSTau;

	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
	  if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
	  if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
	  if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;

	  int rank_nL1HPSTau = -1;
	  for(UInt_t nL1HPSTau = 0; nL1HPSTau < l1hpsTauPt->size(); ++nL1HPSTau){
	    if (!l1hpsTauTightRelIso->at(nL1HPSTau)) continue;
	    if (l1hpsTauPt->at(nL1HPSTau) <= l1Tau_Pt_min) continue;
	    double deltaR =sqrt(pow((hltTauEta->at(kHLTTau) - l1hpsTauEta->at(nL1HPSTau)),2) + pow((hltTauPhi->at(kHLTTau) - l1hpsTauPhi->at(nL1HPSTau)),2));
	    if (deltaR > deltaR_max) continue;
	    rank_nL1HPSTau = nL1HPSTau;

            double dz_L1Taus = TMath::Abs(l1hpsTauZ->at(rank_mL1HPSTau) - l1hpsTauZ->at(rank_nL1HPSTau));
            if (dz_L1Taus > dzMax_L1Taus) continue;

	    if (!isFilled_NoCut){	  
	      hist_Double_hltTauPt_NoCut->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau), Weight);
	      isFilled_NoCut=true;
	    }

	    double dz = TMath::Abs(hltTauZ->at(iHLTTau) - hltTauZ->at(kHLTTau));
	    if(dz > dzMax) continue;

	    if (!isFilled_dZ){
	      hist_Double_hltTauPt_dZ->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau), Weight);
	      isFilled_dZ=true;
	    }

	    if ( (!isFilled_Tight) && ( ((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > deepTau_Tight)) || ((isolation=="ChargedIso") && (hltTauTightRelIso->at(iHLTTau)==1)))
		 && ( ((isolation=="DeepTau") && (hltTauIso->at(kHLTTau) > deepTau_Tight)) || ((isolation=="ChargedIso") && (hltTauTightRelIso->at(kHLTTau)==1))) ){
	      hist_Double_hltTauPt_Tight->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau), Weight);
	      isFilled_Tight=true;
	    }
	    if ( (!isFilled_Medium) && ( ((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > deepTau_Medium)) || ((isolation=="ChargedIso") && (hltTauMediumRelIso->at(iHLTTau)==1)))
		 && ( ((isolation=="DeepTau") && (hltTauIso->at(kHLTTau) > deepTau_Medium)) || ((isolation=="ChargedIso") && (hltTauMediumRelIso->at(kHLTTau)==1))) ){
	      hist_Double_hltTauPt_Medium->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau), Weight);
              isFilled_Medium=true;
	      if(hltTauPt->at(iHLTTau) >= 60 && hltTauPt->at(kHLTTau) >= 60){
                cout<<"Weight = "<<Weight<<endl;//" hltTauPt->at(iHLTTau) = "<<hltTauPt->at(iHLTTau)<<endl;
	      }
	    }
	    if ( (!isFilled_Loose) && ( ((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > deepTau_Loose)) || ((isolation=="ChargedIso") && (hltTauLooseRelIso->at(iHLTTau)==1))) 
		 && ( ((isolation=="DeepTau") && (hltTauIso->at(kHLTTau) > deepTau_Loose)) || ((isolation=="ChargedIso") && (hltTauLooseRelIso->at(kHLTTau)==1))) ){
	      hist_Double_hltTauPt_Loose->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau), Weight);
              isFilled_Loose=true;
	    }
	    if ( (!isFilled_VLoose) && ( ((isolation=="DeepTau") && (hltTauIso->at(iHLTTau) > deepTau_VLoose)) || ((isolation=="ChargedIso") && (hltTauVLooseRelIso->at(iHLTTau)==1)))
		 && ( ((isolation=="DeepTau") && (hltTauIso->at(kHLTTau) > deepTau_VLoose)) || ((isolation=="ChargedIso") && (hltTauVLooseRelIso->at(kHLTTau)==1))) ){
	      hist_Double_hltTauPt_VLoose->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau), Weight);
              isFilled_VLoose=true;
	    }
	  }
	}
      }

    } //for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
    
      // End For Di Tau 
    
    
  } // for(UInt_t i = 0 ; i < treeIn->GetEntries() ; ++i)
  
  cout<<"Denominator = "<<Denominator<<endl;

  if (weight == "Stitching"){
    Denominator = 1;
    freq = 1;
  }
  


  for(UInt_t i_PtBin = 1 ; i_PtBin <= 251 ; ++i_PtBin){
    hist_Rate_Single_hltTauPt_NoCut->SetBinContent(i_PtBin, hist_Single_hltTauPt_NoCut->Integral(i_PtBin,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_dZ->SetBinContent(i_PtBin, hist_Single_hltTauPt_dZ->Integral(i_PtBin,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_VLoose->SetBinContent(i_PtBin, hist_Single_hltTauPt_VLoose->Integral(i_PtBin,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_Loose->SetBinContent(i_PtBin, hist_Single_hltTauPt_Loose->Integral(i_PtBin,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_Medium->SetBinContent(i_PtBin, hist_Single_hltTauPt_Medium->Integral(i_PtBin,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_Tight->SetBinContent(i_PtBin, hist_Single_hltTauPt_Tight->Integral(i_PtBin,251)/Denominator*freq);
    
    if(firstTrue_SingleTau_NoCut && hist_Rate_Single_hltTauPt_NoCut->GetBinContent(i_PtBin) <= targetRate_singleTau){
      cout << "SingleTau NoCut " << hist_Rate_Single_hltTauPt_NoCut->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau NoCut " << hist_Rate_Single_hltTauPt_NoCut->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_NoCut = false;
    }
    if(firstTrue_SingleTau_dZ && hist_Rate_Single_hltTauPt_dZ->GetBinContent(i_PtBin) <= targetRate_singleTau){
      cout << "SingleTau dZ " << hist_Rate_Single_hltTauPt_dZ->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau dZ " << hist_Rate_Single_hltTauPt_dZ->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_dZ = false;
    }
    if(firstTrue_SingleTau_VLoose && hist_Rate_Single_hltTauPt_VLoose->GetBinContent(i_PtBin) <= targetRate_singleTau){
      cout << "SingleTau VLoose " << hist_Rate_Single_hltTauPt_VLoose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau VLoose " << hist_Rate_Single_hltTauPt_VLoose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_VLoose = false;
    }
    if(firstTrue_SingleTau_Loose && hist_Rate_Single_hltTauPt_Loose->GetBinContent(i_PtBin) <= targetRate_singleTau){
      cout << "SingleTau Loose " << hist_Rate_Single_hltTauPt_Loose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau Loose " << hist_Rate_Single_hltTauPt_Loose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_Loose = false;
    }
    if(firstTrue_SingleTau_Medium && hist_Rate_Single_hltTauPt_Medium->GetBinContent(i_PtBin) <= targetRate_singleTau){
      cout << "SingleTau Medium " << hist_Rate_Single_hltTauPt_Medium->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau Medium " << hist_Rate_Single_hltTauPt_Medium->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_Medium = false;
    }
    if(firstTrue_SingleTau_Tight && hist_Rate_Single_hltTauPt_Tight->GetBinContent(i_PtBin) <= targetRate_singleTau){
      cout << "SingleTau Tight " << hist_Rate_Single_hltTauPt_Tight->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau Tight " << hist_Rate_Single_hltTauPt_Tight->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_Tight = false;
    }
    
    hist_Rate_Double_hltTauPt_NoCut->SetBinContent(i_PtBin, hist_Double_hltTauPt_NoCut->Integral(i_PtBin,251,i_PtBin,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_dZ->SetBinContent(i_PtBin, hist_Double_hltTauPt_dZ->Integral(i_PtBin,251,i_PtBin,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_VLoose->SetBinContent(i_PtBin, hist_Double_hltTauPt_VLoose->Integral(i_PtBin,251,i_PtBin,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_Loose->SetBinContent(i_PtBin, hist_Double_hltTauPt_Loose->Integral(i_PtBin,251,i_PtBin,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_Medium->SetBinContent(i_PtBin, hist_Double_hltTauPt_Medium->Integral(i_PtBin,251,i_PtBin,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_Tight->SetBinContent(i_PtBin, hist_Double_hltTauPt_Tight->Integral(i_PtBin,251,i_PtBin,251)/Denominator*freq);

    if(firstTrue_DoubleTau_NoCut && hist_Rate_Double_hltTauPt_NoCut->GetBinContent(i_PtBin) <= targetRate_DoubleoTau){
      cout << "DoubleTau NoCut " << hist_Rate_Double_hltTauPt_NoCut->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau NoCut " << hist_Rate_Double_hltTauPt_NoCut->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_NoCut = false;
    }
    if(firstTrue_DoubleTau_dZ && hist_Rate_Double_hltTauPt_dZ->GetBinContent(i_PtBin) <= targetRate_DoubleoTau){
      cout << "DoubleTau dZ " << hist_Rate_Double_hltTauPt_dZ->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau dZ " << hist_Rate_Double_hltTauPt_dZ->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_dZ = false;
    }
    if(firstTrue_DoubleTau_VLoose && hist_Rate_Double_hltTauPt_VLoose->GetBinContent(i_PtBin) <= targetRate_DoubleoTau){
      cout << "DoubleTau VLoose " << hist_Rate_Double_hltTauPt_VLoose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau VLoose " << hist_Rate_Double_hltTauPt_VLoose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_VLoose = false;
    }
    if(firstTrue_DoubleTau_Loose && hist_Rate_Double_hltTauPt_Loose->GetBinContent(i_PtBin) <= targetRate_DoubleoTau){
      cout << "DoubleTau Loose " << hist_Rate_Double_hltTauPt_Loose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau Loose " << hist_Rate_Double_hltTauPt_Loose->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_Loose = false;
    }
    if(firstTrue_DoubleTau_Medium && hist_Rate_Double_hltTauPt_Medium->GetBinContent(i_PtBin) <= targetRate_DoubleoTau){
      cout << "DoubleTau Medium " << hist_Rate_Double_hltTauPt_Medium->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau Medium " << hist_Rate_Double_hltTauPt_Medium->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_Medium = false;
    }
    if(firstTrue_DoubleTau_Tight && hist_Rate_Double_hltTauPt_Tight->GetBinContent(i_PtBin) <= targetRate_DoubleoTau){
      cout << "DoubleTau Tight " << hist_Rate_Double_hltTauPt_Tight->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau Tight " << hist_Rate_Double_hltTauPt_Tight->GetBinContent(i_PtBin) << " Hz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_Tight = false;
    }
  }


  hist_Single_hltTauPt_NoCut->Write();
  hist_Single_hltTauPt_dZ->Write();
  hist_Single_hltTauPt_Tight->Write();
  hist_Single_hltTauPt_Medium->Write();
  hist_Single_hltTauPt_Loose->Write();
  hist_Single_hltTauPt_VLoose->Write();

  hist_Rate_Single_hltTauPt_NoCut->Write();
  hist_Rate_Single_hltTauPt_dZ->Write();
  hist_Rate_Single_hltTauPt_Tight->Write();
  hist_Rate_Single_hltTauPt_Medium->Write();
  hist_Rate_Single_hltTauPt_Loose->Write();
  hist_Rate_Single_hltTauPt_VLoose->Write();

  hist_Double_hltTauPt_NoCut->Write();
  hist_Double_hltTauPt_dZ->Write();
  hist_Double_hltTauPt_Tight->Write();
  hist_Double_hltTauPt_Medium->Write();
  hist_Double_hltTauPt_Loose->Write();
  hist_Double_hltTauPt_VLoose->Write();

  hist_Rate_Double_hltTauPt_NoCut->Write();
  hist_Rate_Double_hltTauPt_dZ->Write();
  hist_Rate_Double_hltTauPt_Tight->Write();
  hist_Rate_Double_hltTauPt_Medium->Write();
  hist_Rate_Double_hltTauPt_Loose->Write();
  hist_Rate_Double_hltTauPt_VLoose->Write();

  fileOut.Write();


  return;
}
