#!/bin/bash
export EOS_MGM_URL=root://eosuser.cern.ch
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
#Working on lhe step

export LC_ALL=C; unset LANGUAGE


# run pLHE step from singularity container
chmod +x wrapper_pLHE_fullproduction.sh
cmssw-cc6 --command-to-run ./wrapper_pLHE_fullproduction.sh $1 $2
# singularity  -s exec -B /cvmfs/cms.cern.ch/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el6:x86_64 ./wrapper_pLHE.sh $1 $2 $3

# run everything else up to nAOD from slc7 singularity container
chmod +x wrapper_nAOD_fullproduction.sh
cmssw-cc7 --command-to-run ./wrapper_nAOD_fullproduction.sh $1
# singularity  -s exec -B /cvmfs/cms.cern.ch/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el7:x86_64 ./wrapper_nAOD.sh

echo "Done!"
