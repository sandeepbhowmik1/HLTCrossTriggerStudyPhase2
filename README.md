# HLTCrossTriggerStudyPhase2

git clone https://github.com/sandeepbhowmik1/HLTCrossTriggerStudyPhase2


go to inside of any $CMSSW_BASE/src/

cmsenv


# To make Rate plots

cd HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/ratePlot/macro

root -l rate_Calculation_using_Pt_for_HPSL1andHLTTau.C

python plot_Rate_for_All_WorkingPoints.py

see plots in HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/ratePlot/plots



# To make Efficiency plots

cd HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/efficiencyPlot/macro

python convertTreeFor_EfficiencyPlot_for_Double_Gen_L1andHLTTau.py



cd HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/efficiencyPlot/fitTurnon

make clean

rm obj/*

make


./fit.exe run/parameter_file_Efficiency_Fitter_vs_Pt_for_Double_Gen_HPSL1andHLTTau_DeepTau_All_Stitching_20211012.par


cd HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/efficiencyPlot/macro

python plot_Efficiency_vs_Pt_for_All_WorkingPoints.py

see plots in HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/efficiencyPlot/plots






# All the files can be run using the script 

HLTCrossTriggerStudyPhase2/HLTCrossTriggerStudyPhase2/script/commandsToMakePlots.py


