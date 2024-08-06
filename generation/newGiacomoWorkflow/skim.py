#
#   python -m venv myenv #!(only first time)
#   source myenv/bin/activate
#   pip install uproot[http] xrootd #!(only first time)
#   pip install fsspec-xrootd #!(only first time)
#
# python skim.py /store/user/mpresill/aQGC_VVJJ_Private_Production_2016_GiacomoChain/aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10/nAOD /ceph/mpresill/privateProduction_aQGC_VBS_semileptonic_nanov7/2016_skimmed --debug
# nice -n 15 python skim.py /store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10/nAOD/ /eos/uscms/store/group/lnujj/aQGC_VVJJ_Private_Production_2017_GiacomoChain/hadded/aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10
# nice -n 15 python skim.py /store/group/lnujj/aQGC_VVJJ_Private_Production_2018_GiacomoChain/aQGC_WPhadWMlepJJ_EWK_LO_SM_mjj100_pTj10/ /eos/uscms/store/group/lnujj/aQGC_VVJJ_Private_Production_2018_GiacomoChain/hadded/aQGC_WPhadWMlepJJ_EWK_LO_SM_mjj100_pTj10


import sys
import os
import uproot
import subprocess
from multiprocessing import Pool

def list_files_xrootd(xrootd_url, directory):
    import subprocess
    
    result = subprocess.run(['xrdfs', xrootd_url, 'ls', directory], stdout=subprocess.PIPE) # Matteo
    #`xrdfsls -u /store/user/username/rootFiles | grep '\.root'`
    # result = subprocess.run(['xrdfsls','-u',directory], stdout=subprocess.PIPE) #Irene FNAL (TBC)
    files = result.stdout.decode('utf-8').splitlines()
    return files

def skim(file):
    fname__ = os.path.basename(file)
    print(f"Processing {fname__}")
    
    xrootd_url = "root://cmseos.fnal.gov/" # "root://cmsdcache-kit-disk.gridka.de:1094" Matteo
    file_url = f"{xrootd_url}/{file}"
    
    with uproot.open(file_url) as f:
        t = f["Events"]
        aka = t.arrays()
        print(f"Before: {len(aka)} events")

        ev = aka[aka["nLHEReweightingWeight"] == 1620]
        if len(ev) > 0:
            print(f"Input file {file_url} is good.")
            return file_url
        else:
            print(f"No events passed the filter in {fname__}. Skipping...")
            return None

def run_hadd_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Hadd command output:", result.stdout)
        print("Hadd command error output:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error while running hadd command: {e.stderr}")
        print("Command that failed:", ' '.join(command))  # Print the command that failed

def save_command_to_file(command, file_path):
    with open(file_path, 'a') as f:
        f.write(' '.join(command) + '\n')

def hadd(input_files, final_output_dir, batch_size=10, command_file=None):
    # Verifica se la directory di output esiste, altrimenti la crea
    if not os.path.exists(final_output_dir):
        os.makedirs(final_output_dir)
    
    # Itera sui file di input in blocchi di dimensione batch_size
    for i in range(0, len(input_files), batch_size):
        # Seleziona i file del batch corrente
        batch_files = [f for f in input_files[i:i+batch_size] if f]
        print("These are the batch files included:", batch_files)
        if not batch_files:
            continue
        
        # Crea il nome del file di output per il batch corrente
        batch_output = os.path.join(final_output_dir, f"hadd_{i//batch_size}.root")
        
        # Crea il comando da eseguire
        command = ["hadd", "-f", batch_output] + batch_files
        print(f"Running command: {' '.join(command)}")  # Stampa il comando per il debugging
        
        # Salva il comando nel file di testo
        if command_file:
            save_command_to_file(command, command_file)
        
        # Esegui il comando
        # run_hadd_command(command)

    print(f"Created {final_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python skim.py <input_dir> <output_dir> [--debug]")
        sys.exit(0)

    xrootd_url = "root://cmseos.fnal.gov/" # "root://cmsdcache-kit-disk.gridka.de:1094"
    in_ = sys.argv[1]
    out_ = sys.argv[2]
    debug = len(sys.argv) > 3 and sys.argv[3] == '--debug'

    if in_ == out_:
        print("[ERROR] in and out directories equal...")
        sys.exit(0)

    if not os.path.isdir(out_): #for lpc eos it should not be handled like this..
        os.mkdir(out_)

    ls = list_files_xrootd(xrootd_url, in_)

    if debug:
        ls = ls[:20]
        out_ = os.path.join(out_, "debug")
        if not os.path.isdir(out_):
            os.mkdir(out_)
        print(f"Debug mode: processing only {len(ls)} files")

    with Pool(processes=8) as pool:
        output_files = pool.map(skim, ls)

    valid_files = [f for f in output_files if f]
    print("Valid files for hadd:", valid_files)

    final_output_dir = os.path.join(out_, "combined")
    if not os.path.isdir(final_output_dir):
        os.mkdir(final_output_dir)

    command_file = "hadd_commands.txt"  # File to save commands

    debug_batch_size = 5  # o qualsiasi numero tu ritenga opportuno per i batch in modalità debug
    hadd(valid_files, final_output_dir, batch_size=100 if not debug else debug_batch_size, command_file=command_file)
