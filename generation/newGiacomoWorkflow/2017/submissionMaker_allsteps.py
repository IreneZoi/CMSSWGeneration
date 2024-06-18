import os
import fileinput

submitNano = True
year    = "2017"
samples = [
"aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_WPlepWMhadJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_WPhadZlepJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_WPhadWMlepJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_WMlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_WPlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
# # "aQGC_WMlepWMhadJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_WPlepWPhadJJ_EWK_LO_SM_mjj100_pTj10"
]

cwd = os.getcwd()
for sample in samples:
    print ("sample: ",sample)
    directory = '{}_{}/'.format(year,sample)
    try:
        os.mkdir(directory)
    except:
        print("directory {} exists".format(directory))
    os.system("source /cvmfs/cms.cern.ch/cmsset_default.sh")
    os.system("mkdir /eos/uscms/store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/{}/".format(sample))
    os.system("mkdir /eos/uscms/store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/{}/pLHE".format(sample))
    os.system("mkdir /eos/uscms/store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/{}/nAOD".format(sample))
    
    
    # submit pLHE
    wrapperFile = 'wrapper_pLHE_fullproduction.sh'
    # jdlFile     = 'submit_pLHE_fullproduction.jdl'
    if submitNano == True:
        print(" Submitting Nano!!!")
        # submit nano
        wrapperFile = 'wrapper_nAOD_fullproduction.sh'
        # jdlFile     = 'submit_nAOD_fullproduction.jdl'

    wrapperFile_new = '{}'.format(wrapperFile)
    filein = open('{}'.format(wrapperFile))
    fileout = open('{}{}'.format(directory,wrapperFile_new),"wt")
    for line in filein:
        fileout.write(line.replace('{SAMPLE}',sample))
    filein.close()
    fileout.close()


    jdlFile="submit_allsteps.jdl"
    jdlFile_new = '{}'.format(jdlFile)
    filein = open('{}'.format(jdlFile))
    fileout = open('{}{}'.format(directory,jdlFile_new),"wt")
    for line in filein:
        fileout.write(line.replace('{SAMPLE}',sample))
    filein.close()
    fileout.close()
    os.system("cp wrapper_allsteps.sh {}".format(directory))
    os.chdir(directory)
    
    os.system("condor_submit {}".format(jdlFile_new))
    os.chdir(cwd)
    
    
    


