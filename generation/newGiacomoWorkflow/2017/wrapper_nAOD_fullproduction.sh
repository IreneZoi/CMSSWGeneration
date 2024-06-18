#!/bin/bash
export EOS_MGM_URL=root://eosuser.cern.ch
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
#Working on GS step
xrdcp -f root://cmseos.fnal.gov//store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/{SAMPLE}/pLHE/pLHE_${1}.root  SMP-RunIIWinter15pLHE-00016.root
# first of all, move the root file in input
# with the desire file name for GS config 

echo "Opening CMSSW_9_3_19"
tar -xzvf CMSSW_9_3_19.tgz
rm CMSSW_9_3_19.tgz
cd CMSSW_9_3_19/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIIFall17GS-00271_1_cfg.py


#Working on premix step

rm -rf CMSSW_9_3_19
echo "Opening CMSSW_9_4_7"
tar -xzvf CMSSW_9_4_7.tgz
rm CMSSW_9_4_7.tgz
cd CMSSW_9_4_7/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIIFall17DRPremix-00331_1_cfg.py


#Working on premix step

date
cmsRun SMP-RunIIFall17DRPremix-00331_2_cfg.py


#Working on miniAOD step

date
cmsRun SMP-RunIIFall17MiniAODv2-00338_1_cfg.py


#Working on nanoAOD step

rm -rf CMSSW_9_4_7
echo "Opening CMSSW_10_2_24_patch1_ZV_EFT"
tar -xzvf CMSSW_10_2_24_patch1_ZV_EFT.tgz
rm CMSSW_10_2_24_patch1_ZV_EFT.tgz
cd CMSSW_10_2_24_patch1_ZV_EFT/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIIFall17NanoAODv7-00268_1_cfg.py
xrdcp -f SMP-RunIIFall17NanoAODv7-00268.root root://cmseos.fnal.gov//store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/{SAMPLE}/nAOD/nano_${1}.root 


rm SMP-RunIIWinter15pLHE-00016.root SMP-RunIIFall17GS-00271.root  SMP-RunIIFall17DRPremix-00331.root SMP-RunIIFall17DRPremix-00331_0.root SMP-RunIIFall17MiniAODv2-00338.root
rm -rf CMSSW_10_2_24_patch1_ZV_EFT *py
date
