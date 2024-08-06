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
xrdcp -f SMP-RunIIFall17DRPremix-00331_0.root root://cmseos.fnal.gov//store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/{SAMPLE}/Premix/premix1_${1}.root 


rm SMP-RunIIWinter15pLHE-00016.root SMP-RunIIFall17GS-00271.root SMP-RunIIFall17DRPremix-00331_0.root 
rm -rf *py CMSSW_9_4_7
date
