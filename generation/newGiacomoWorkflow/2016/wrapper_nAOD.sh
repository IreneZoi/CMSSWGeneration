#!/bin/bash
export EOS_MGM_URL=root://eosuser.cern.ch
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
#Working on lhe step

export LC_ALL=C; unset LANGUAGE

mv *.root SMP-RunIISummer15GS-00266.root

ls

echo "Opening CMSSW_8_0_31"
tar -xzf CMSSW_8_0_31.tgz
rm CMSSW_8_0_31.tgz
cd CMSSW_8_0_31/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date

# step 1
cmsRun SMP-RunIISummer16DR80Premix-00645_1_cfg.py

# step 2
cmsRun SMP-RunIISummer16DR80Premix-00645_2_cfg.py

# singularity exec --contain --ipc --pid --home $PWD --bind /cvmfs  /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest ./Premix.sh


# now run MINIAOD step
echo "Opening CMSSW_9_4_9"
tar -xzf CMSSW_9_4_9.tgz
rm CMSSW_9_4_9.tgz
cd CMSSW_9_4_9/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date

cmsRun SMP-RunIISummer16MiniAODv3-00478_1_cfg.py

# now run NANOAOD step
echo "Opening CMSSW_10_2_24_patch1_ZV_EFT"
tar -xzf CMSSW_10_2_24_patch1_ZV_EFT.tgz
rm CMSSW_10_2_24_patch1_ZV_EFT.tgz
cd CMSSW_10_2_24_patch1_ZV_EFT/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date

cmsRun SMP-RunIISummer16NanoAODv7-00422_1_cfg.py  

#########

rm SMP-RunIISummer15GS-00266.root SMP-RunIISummer16DR80Premix-00645.root SMP-RunIISummer16DR80Premix-00645_0.root SMP-RunIISummer16MiniAODv3-00478.root
rm -rf CMSSW_8_0_31 CMSSW_9_4_9 CMSSW_10_2_24_patch1_ZV_EFT *py
date

echo "Done"
