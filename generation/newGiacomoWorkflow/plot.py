#
#   python -m venv myenv #!(only first time)
#   source myenv/bin/activate
#   pip install uproot[http] xrootd #!(only first time)
#   pip install fsspec-xrootd #!(only first time)
#   pip install coffea #!(only first time)
#
# python plot.py /eos/uscms/store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10/nAOD aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10_2017
#

import numpy as np
import awkward as ak
from coffea.nanoevents import NanoEventsFactory
from matplotlib import pyplot as plt
import mplhep as hep
import os
from glob import  glob
import uproot
import sys

plt.style.use(hep.style.CMS)

# comparing histograms more than graphically
def compare_histograms(histograms):
    for i in range(len(histograms)):
        for j in range(i+1, len(histograms)):
            difference = np.sum((histograms[i] - histograms[j]) ** 2)
            if difference !=0:
                print(f"DANGER: Found difference between histogram {i+1} and histogram {j+1} : {difference}")

# remove corrupted file number 19
def generate_filenames(base, start, end):
    return [f"{base}{i}.root" for i in range(start, end+1)]# if i != 49]


### new samples

fs00p00_all = []
fs10p00_all = []
fs20p00_all = []
ft00p00_all = []
ft10p00_all = []
ft20p00_all = []
ft30p00_all = []
ft40p00_all = []
ft50p00_all = []
ft60p00_all = []
ft70p00_all = []
ft80p00_all = []
ft90p00_all = []
fm00p00_all = []
fm10p00_all = []
fm20p00_all = []
fm30p00_all = []
fm40p00_all = []
fm50p00_all = []
fm70p00_all = []

# Initialize a dictionary to store the number of LHEReweightingWeights for each file
weights_count = {}

if len(sys.argv) < 2:
   print("Usage python plot.py <folder_nAOD> <Name of proc>")
   sys.exit(0)


fnames = glob(sys.argv[1] + "/*")
print("fnames ",fnames)
for fname in fnames:
    print(fname)

    f = uproot.open(fname)
    t = f["Events"]
    events = t.arrays()
    # events = NanoEventsFactory.from_root(fname).events()

    #selection = (ak.num(events.GenJetAK8)>0)
    weights = events['LHEReweightingWeight']

    """
# Check if all events have the same maximum index "i" for the LHEReweightingWeight
    max_indices = ak.Array([len(w) for w in weights])
    if ak.all(max_indices == max_indices[0]):
        print("All events have the same maximum index.")
        print(f"Max index for file: {max_indices[0]}")
    else:
        print("WARNING: Not all events have the same maximum index.")

# Check if any weight array is corrupted (contains NaN or infinite values)
    if ak.any(ak.is_none(weights)) or ak.any(ak.is_none(weights)):
        print("WARNING: The weight array contains NaN or infinite values.")
    #else:
    #    print("The weight array does not contain any NaN or infinite values.")
    """

# fill lhe rew weights for some specific position we now should map SM
#    fs00p00 = events['LHEReweightingWeight'][:,40]
#    ft00p00 = events['LHEReweightingWeight'][:,850]
#    ft30p00 = events['LHEReweightingWeight'][:,1093]
#    fm30p00 = events['LHEReweightingWeight'][:,526]
#
#    fs00p00_all = np.concatenate((fs00p00_all, fs00p00))
#    ft00p00_all = np.concatenate((ft00p00_all, ft00p00))
#    ft30p00_all = np.concatenate((ft30p00_all, ft30p00))
#    fm30p00_all = np.concatenate((fm30p00_all, fm30p00))

    fs00p00 = events['LHEReweightingWeight'][:,40]
    fs10p00 = events['LHEReweightingWeight'][:,121]
    fs20p00 = events['LHEReweightingWeight'][:,202]
    
    ft00p00 = events['LHEReweightingWeight'][:,850] 
    ft10p00 = events['LHEReweightingWeight'][:,931]
    ft20p00 = events['LHEReweightingWeight'][:,1012]
    ft30p00 = events['LHEReweightingWeight'][:,1093]
    ft40p00 = events['LHEReweightingWeight'][:,1174]
    ft50p00 = events['LHEReweightingWeight'][:,1255]
    ft60p00 = events['LHEReweightingWeight'][:,1336]
    ft70p00 = events['LHEReweightingWeight'][:,1417]
    ft80p00 = events['LHEReweightingWeight'][:,1498]
    ft90p00 = events['LHEReweightingWeight'][:,1579]
    
    fm00p00 = events['LHEReweightingWeight'][:,283]
    fm10p00 = events['LHEReweightingWeight'][:,364]
    fm20p00 = events['LHEReweightingWeight'][:,445]
    fm30p00 = events['LHEReweightingWeight'][:,526]
    fm40p00 = events['LHEReweightingWeight'][:,607]
    fm50p00 = events['LHEReweightingWeight'][:,688]
    fm70p00 = events['LHEReweightingWeight'][:,769]

    fs00p00_all = np.concatenate((fs00p00_all, fs00p00))
    fs10p00_all = np.concatenate((fs10p00_all, fs10p00))
    fs20p00_all = np.concatenate((fs20p00_all, fs20p00))
    ft00p00_all = np.concatenate((ft00p00_all, ft00p00))
    ft10p00_all = np.concatenate((ft10p00_all, ft10p00))
    ft20p00_all = np.concatenate((ft20p00_all, ft20p00))
    ft30p00_all = np.concatenate((ft30p00_all, ft30p00))
    ft40p00_all = np.concatenate((ft40p00_all, ft40p00))
    ft50p00_all = np.concatenate((ft50p00_all, ft50p00))
    ft60p00_all = np.concatenate((ft60p00_all, ft60p00))
    ft70p00_all = np.concatenate((ft70p00_all, ft70p00))
    ft80p00_all = np.concatenate((ft80p00_all, ft80p00))
    ft90p00_all = np.concatenate((ft90p00_all, ft90p00))
    fm00p00_all = np.concatenate((fm00p00_all, fm00p00))
    fm10p00_all = np.concatenate((fm10p00_all, fm10p00))
    fm20p00_all = np.concatenate((fm20p00_all, fm20p00))
    fm30p00_all = np.concatenate((fm30p00_all, fm30p00))
    fm40p00_all = np.concatenate((fm40p00_all, fm40p00))
    fm50p00_all = np.concatenate((fm50p00_all, fm50p00))
    fm70p00_all = np.concatenate((fm70p00_all, fm70p00))

# List of all histograms and compare them (not only graphically)
histograms = [fs00p00_all, fs10p00_all, fs20p00_all, ft00p00_all, ft10p00_all, ft20p00_all, ft30p00_all, ft40p00_all, ft50p00_all, ft60p00_all, ft70p00_all, ft80p00_all, ft90p00_all, fm00p00_all, fm10p00_all, fm20p00_all, fm30p00_all, fm40p00_all, fm50p00_all, fm70p00_all]
print("histograms ",histograms)
compare_histograms(histograms)

# superimposing weights that should give the SM - they have to be identical.
f, ax = plt.subplots(figsize=(8, 8))

print(ft00p00_all.to_numpy())
# Superimpose the histograms of ft00p00_all and fs00p00_all in the first subplot
#hep.histplot(np.histogram(ft00p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='r', label="$f_\mathrm{T0} = 0.00 \mathrm{TeV}^{-4}$")
#hep.histplot(np.histogram(fs00p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='b', label="$f_\mathrm{S0} = 0.00 \mathrm{TeV}^{-4}$")
#hep.histplot(np.histogram(ft30p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='g', label="$f_\mathrm{T3} = 0.00 \mathrm{TeV}^{-4}$")
#hep.histplot(np.histogram(fm30p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='orange', label="$f_\mathrm{M3} = 0.00 \mathrm{TeV}^{-4}$")
# Superimpose the histograms of ft00p00_all and fs00p00_all in the first subplot
hep.histplot(np.histogram(ft00p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='r', label="$f_\mathrm{T0} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fs00p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='b', label="$f_\mathrm{S0} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft30p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='g', label="$f_\mathrm{T3} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fm30p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='orange', label="$f_\mathrm{M3} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fs10p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='cyan', label="$f_\mathrm{S1} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fs20p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='magenta', label="$f_\mathrm{S2} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft10p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='yellow', label="$f_\mathrm{T1} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft20p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='brown', label="$f_\mathrm{T2} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft40p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='grey', label="$f_\mathrm{T4} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft50p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='pink', label="$f_\mathrm{T5} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft60p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='lime', label="$f_\mathrm{T6} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft70p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='purple', label="$f_\mathrm{T7} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft80p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='navy', label="$f_\mathrm{T8} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(ft90p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='olive', label="$f_\mathrm{T9} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fm00p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='coral', label="$f_\mathrm{M0} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fm10p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='teal', label="$f_\mathrm{M1} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fm20p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='maroon', label="$f_\mathrm{M2} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fm40p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='violet', label="$f_\mathrm{M4} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fm50p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='orchid', label="$f_\mathrm{M5} = 0.00 \mathrm{TeV}^{-4}$")
hep.histplot(np.histogram(fm70p00_all.to_numpy(), np.linspace(0, 1.15, 200)), ax=ax, color='gold', label="$f_\mathrm{M7} = 0.00 \mathrm{TeV}^{-4}$")

ax.legend()
ax.legend(ncol=1, bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 6})  # Adjust the parameters here
ax.set_xlabel('LHEReweighting Weights EFT->SM')
ax.set_yscale('log')
ax.set_xlim(-0.1, 1.2)

plt.tight_layout()


# # Extract the plot name from the base_url
#plot_name = file_name.split('/')[-2]
## Define the directory where you want to save the plot
#output_dir = "/eos/user/m/mpresill/www/VBS/EFTplots/validation/privateSamples_LHERew/"
## Ensure the output directory exists
#os.makedirs(output_dir, exist_ok=True)
## Define the full path to the output file
#output_file = os.path.join(output_dir, f"{plot_name}.pdf")
## Save the plot to the output file
##plt.savefig(output_file)
#plt.savefig(output_file) # Use bbox_inches='tight' to include the legend properly
#
#plt.show()
#

# Extract the plot name from the base_url
# plot_name = base_url.split('/')[-3]+'_'+'_'+base_url.split('/')[-1]
# Define the directory where you want to save the plot
# output_dir = "/eos/user/m/mpresill/www/VBS/EFTplots/validation/debugLHEReweightingWeights_officialv2"
# Ensure the output directory exists
output_dir = "plots"
plot_name = sys.argv[2]
os.makedirs(output_dir, exist_ok=True)

# Define the full path to the output file
output_file = os.path.join(output_dir, f"{plot_name}.pdf")
# Save the plot to the output file
plt.savefig(output_file)

plt.show()
