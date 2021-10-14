import os, subprocess, sys


# ----------- *** Start Modification *** -------------------------------------

pathRootTree = '/home/sbhowmik/RootTree/HLTTau/Phase2/'

tagNTuple = ''
tagRootTree = '20210611_2'
#tagRootTree = '20210208'
tagPlot = '20211012'

workingDir = os.getcwd()

pathPlot = os.path.join(workingDir, "plots")

tauType = 'genTau' 
#tauType = 'recoGMTau'

#sampleType=["Signal", "Background"]
sampleType=["Signal"]
sampleType=["Background"] 

#nTau=["Single", "Double"]
nTau=["Double"]

#recoType=["Gen", "Reco"]
recoType=["Gen"]

####algoType=["L1"]
#algoType=["L1Tau"]
#algoType=["HLTTau"]
algoType=["L1andHLTTau"]

######l1tauType=["", "NN", "HPS"]
#l1tauType=[""]  # for algoType=["HLTTau"]
l1tauType=["HPS"]
#l1tauType=["NN"]

#fileType=["rootTree", "bdt", "hist"] 
fileType=["rootTree"]

#objType=["Pt", "Eta", "Nvtx"]
#objType=["Pt", "Eta"]
objType=["Pt"]
#objType=["Eta"]

dzType=["with_dZ", "without_dZ"]
#dzType=["without_dZ"]

isolation=["DeepTau", "ChargedIso"]
isolation=["DeepTau"]
#isolation=["ChargedIso"]

etaRange=["Barrel", "Endcap", "All"]
etaRange=["Barrel"]
etaRange=["All"]

weight=["Stitching", "MC"]
weight=["Stitching"]
#weight=["MC"]

# ------------ *** End Modification *** --------------------------------------



# ------------ Define command to execute -------------------------------------
def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout


# -------------- plot rate vs tau pt ----------------------------------

for i in range (0, len(algoType)):
  for j in range (0, len(l1tauType)): 
    for k in range (0, len(isolation)):
      for l in range (0, len(etaRange)):
        for m in range (0, len(weight)):
          scriptFile = os.path.join(workingDir, "ratePlot/macro", "rate_Calculation_using_Pt_for_"+l1tauType[j]+algoType[i]+".C")
          #scriptFile = os.path.join(workingDir, "ratePlot/macro", "rate_Calculation_using_loop_for_"+algoType[i]+".C")
          if weight[m] == "MC":
            fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[i]+"Analyzer_Background_"+isolation[k]+"_"+tagRootTree+".root")
            fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[i]+"Analyzer_Background_DYToLL_"+isolation[k]+"_"+tagRootTree+".root")
            fileName_In = os.path.join(pathRootTree, "rootTree_test_L1andHLTTauAnalyzer_Background_MinBias_chargedIso_20201219.root")
          else:
            #fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[i]+"Analyzer_Background_"+isolation[k]+"_"+weight[m]+"_"+tagRootTree+".root")
            fileName_In = os.path.join(pathRootTree, "rootTree_test_"+"L1andHLTTau"+"Analyzer_Background_"+isolation[k]+"_"+weight[m]+"_"+tagRootTree+".root")
          #treeName_In = algoType[i]+'Analyzer/'+algoType[i]+'Analyzer'
          treeName_In = "L1andHLTTau"+'Analyzer/'+"L1andHLTTau"+'Analyzer'
          fileName_Out = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+l1tauType[j]+algoType[i]+"_Background_"+isolation[k]+"_"+etaRange[l]+"_"+weight[m]+"_"+tagPlot+".root")
          #fileName_Out = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+l1tauType[j]+algoType[i]+"_Background_DYToLL_"+isolation[k]+"_"+etaRange[l]+"_"+weight[m]+"_"+tagPlot+".root")
          run_cmd('root -b -n -q -l \'%s(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\" )\'' % (scriptFile, fileName_In, treeName_In, fileName_Out, isolation[k], etaRange[l], weight[m]))
          scriptPlot = os.path.join(workingDir, "ratePlot/macro", "plot_Rate_for_All_WorkingPoints.py")
          fileName_Out_Plot = os.path.join(workingDir, "ratePlot/plots", "plot_Rate_for_All_WorkingPoints_"+l1tauType[j]+algoType[i]+"_"+isolation[k]+"_"+etaRange[l]+"_"+weight[m]+"_"+tagPlot)
          #fileName_Out_Plot = os.path.join(workingDir, "ratePlot/plots", "plot_Rate_for_All_WorkingPoints_"+l1tauType[j]+algoType[i]+"_DYToLL_"+isolation[k]+"_"+etaRange[l]+"_"+weight[m]+"_"+tagPlot)
          if(l1tauType[j]==""):
            run_cmd('python %s %s %s %s %s %s' % (scriptPlot, fileName_Out, fileName_Out_Plot, "HLT", isolation[k], etaRange[l]))
          else:
            run_cmd('python %s %s %s %s %s %s' % (scriptPlot, fileName_Out, fileName_Out_Plot, l1tauType[j], isolation[k], etaRange[l]))



# -----------Convert root tree for efficiency plot ------------
'''
for i in range (0, len(nTau)):
  for j in range (0, len(recoType)):
    for k in range (0, len(algoType)):
      for m in range (0, len(isolation)):
        for n in range (0, len(etaRange)): 
          for o in range (0, len(weight)):
            for p in range (0, len(l1tauType)):
              scriptFile = os.path.join(workingDir, "efficiencyPlot/macro", "convertTreeFor_EfficiencyPlot_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+".py")
              #fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[k]+"Analyzer_Signal_VBFHToTauTau_"+isolation[m]+"_"+tagRootTree+".root")
              fileName_In = os.path.join(pathRootTree, "rootTree_test_L1andHLTTauAnalyzer_Signal_VBFHToTauTau_"+isolation[m]+"_"+tagRootTree+".root")
              #treeName_In = algoType[k]+'Analyzer/'+algoType[i]+'Analyzer'
              treeName_In = 'L1andHLTTauAnalyzer/'+'L1andHLTTauAnalyzer'
              fileName_In_txt = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+l1tauType[p]+algoType[k]+"_Background_"+isolation[m]+"_"+etaRange[n]+"_"+weight[o]+"_"+tagPlot+".txt")
              fileName_Out = os.path.join(pathRootTree, "rootTree_Signal_Efficiency_for_"+nTau[i]+"_"+recoType[j]+"_"+l1tauType[p]+algoType[k]+"_"+isolation[m]+"_"+etaRange[n]+"_"+weight[o]+"_"+tagPlot+".root")
              if(l1tauType[p]==""):
                run_cmd('python %s %s %s %s %s %s %s %s' % (scriptFile, fileName_In, treeName_In, fileName_In_txt, fileName_Out, isolation[m], etaRange[n], "HLT"))
              else:
                run_cmd('python %s %s %s %s %s %s %s %s' % (scriptFile, fileName_In, treeName_In, fileName_In_txt, fileName_Out, isolation[m], etaRange[n], l1tauType[p]))
'''


# -------------- Plot efficiency turn-on vs Pt -------------------------------
'''
scriptDir = os.path.join(workingDir, "efficiencyPlot/fitTurnon/run")
for i in range (0, len(objType)):
  scriptFile = os.path.join(scriptDir, "create_parameter_file_Efficiency_Fitter_vs_"+objType[i]+".sh")
  for j in range (0, len(nTau)):
    for k in range (0, len(recoType)):
      for l in range (0, len(algoType)):
        for m in range (0, len(isolation)):
          for n in range (0, len(etaRange)):
            for o in range (0, len(weight)):
              for p in range (0, len(l1tauType)):
                fileName_In = os.path.join(pathRootTree, "rootTree_Signal_Efficiency_for_"+nTau[j]+"_"+recoType[k]+"_"+l1tauType[p]+algoType[l]+"_"+isolation[m]+"_"+etaRange[n]+"_"+weight[o]+"_"+tagPlot+".root")
                fileName_Out = os.path.join(workingDir, "efficiencyPlot/results", "fitOutput_Efficiency_vs_"+objType[i]+"_for_"+nTau[j]+"_"+recoType[k]+"_"+l1tauType[p]+algoType[l]+"_"+isolation[m]+"_"+etaRange[n]+"_"+weight[o]+"_"+tagPlot+".root")
                scriptOut = "parameter_file_Efficiency_Fitter_vs_"+objType[i]+"_for_"+nTau[j]+"_"+recoType[k]+"_"+l1tauType[p]+algoType[l]+"_"+isolation[m]+"_"+etaRange[n]+"_"+weight[o]+"_"+tagPlot+".par"
                run_cmd('bash %s %s %s %s' % (scriptFile, fileName_In, fileName_Out, scriptOut))
                run_cmd('mv %s %s' % (scriptOut, scriptDir))
                scriptFit = os.path.join(workingDir, "efficiencyPlot/fitTurnon", "fit.exe")
                parFile = os.path.join(scriptDir, scriptOut)
                run_cmd('%s %s' %(scriptFit, parFile))

                scriptPlot = os.path.join(workingDir, "efficiencyPlot/macro", "plot_Efficiency_vs_"+objType[i]+"_for_All_WorkingPoints.py")
                fileName_In_txt = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+l1tauType[p]+algoType[k]+"_Background_"+isolation[m]+"_"+etaRange[n]+"_"+weight[o]+"_"+tagPlot+".txt")
                fileName_Out_Plot = os.path.join(workingDir, "efficiencyPlot/plots", "plot_Efficiency_vs_"+objType[i]+"_for_"+nTau[j]+"_"+recoType[k]+"_"+l1tauType[p]+algoType[l]+"_"+isolation[m]+"_"+etaRange[n]+"_"+weight[o]+"_"+tagPlot)
                if(l1tauType[p]==""):
                  run_cmd('python %s %s %s %s %s %s %s' % (scriptPlot, fileName_Out, fileName_In_txt, fileName_Out_Plot, isolation[m], etaRange[n], "HLT"))
                else:
                  run_cmd('python %s %s %s %s %s %s %s' % (scriptPlot, fileName_Out, fileName_In_txt, fileName_Out_Plot, isolation[m], etaRange[n], l1tauType[p]))


'''




