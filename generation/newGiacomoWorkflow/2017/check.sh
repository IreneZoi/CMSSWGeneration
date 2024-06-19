#!bin/bash/

samples=(
aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPlepWMhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPhadZlepJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPhadWMlepJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WMlepZhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPlepZhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WMlepWMhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPlepWPhadJJ_EWK_LO_SM_mjj100_pTj10
)

for sample in ${samples[*]}; do
    echo "---------------------------"
    python resubmitJobs.py -d $sample
    echo "---------------------------"
done