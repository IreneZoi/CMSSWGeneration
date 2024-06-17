#!/bin/bash
export EOS_MGM_URL=root://eosuser.cern.ch
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
#Working on lhe step

# first of all, move the root file in input
# with the desire file name for GS config 

mv *.root SMP-RunIIWinter15pLHE-00016.root 

echo "Opening CMSSW_10_2_24_patch1"
tar -xzvf CMSSW_10_2_24_patch1.tgz
rm CMSSW_10_2_24_patch1.tgz
cd CMSSW_10_2_24_patch1/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIIFall18GS-00284_1_cfg.py


#Working on premix step

rm -rf CMSSW_10_2_24_patch1
echo "Opening CMSSW_10_2_5"
tar -xzvf CMSSW_10_2_5.tgz
rm CMSSW_10_2_5.tgz
cd CMSSW_10_2_5/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIIAutumn18DRPremix-00275_1_cfg.py


#Working on premix step

date
cmsRun SMP-RunIIAutumn18DRPremix-00275_2_cfg.py


#Working on miniAOD step

date
cmsRun SMP-RunIIAutumn18MiniAOD-00276_1_cfg.py


#Working on nanoAOD step

rm -rf CMSSW_10_2_5
echo "Opening CMSSW_10_2_22_ZV_EFT"
tar -xzvf CMSSW_10_2_22_ZV_EFT.tgz
rm CMSSW_10_2_22_ZV_EFT.tgz
cd CMSSW_10_2_22_ZV_EFT/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIIAutumn18NanoAODv7-00058_1_cfg.py


rm aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz SMP-RunIIWinter15pLHE-00016.root SMP-RunIIFall18GS-00284.root SMP-RunIIAutumn18DRPremix-00275.root SMP-RunIIAutumn18DRPremix-00275_0.root SMP-RunIIAutumn18MiniAOD-00276.root
rm -rf CMSSW_10_2_22_ZV_EFT *py
date
