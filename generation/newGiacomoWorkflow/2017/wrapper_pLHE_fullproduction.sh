#!/bin/bash
export EOS_MGM_URL=root://eosuser.cern.ch
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
#Working on lhe step

export LC_ALL=C; unset LANGUAGE
gridpack={SAMPLE}_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz
xrdcp -f root://cmseos.fnal.gov//store/group/lnujj/aQGC_VVJJ_Private_Production_gridpack/${gridpack} .
 
# first argument is $(Step)
let seed=$1+1

mkdir temp_dir; tar -axvf ${gridpack} --directory temp_dir; cd temp_dir

# number of events requested, seed, number of cpus
# third argument is $(nevents_x_job)
# here 2 is the number of core requested
./runcmsgrid.sh $3 $seed 2

mv cmsgrid_final.lhe ..; cd ..

ls

#cleaning 
rm -rf temp_dir

# now convert the LHE in a EDM tuple via pLHE step
# this needs to run on sl6 therefore we create a script that runs the following

echo "Opening CMSSW_7_1_32"
tar -xzvf CMSSW_7_1_32.tgz
rm CMSSW_7_1_32.tgz
cd CMSSW_7_1_32/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIIWinter15pLHE-00016_1_cfg.py
xrdcp -f SMP-RunIIWinter15pLHE-00016.root root://cmseos.fnal.gov//store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/{SAMPLE}/pLHE/pLHE_${1}.root

echo "Done"