# python Downloader.py -y 2017 -s lhe premix miniAOD nanoAOD


import requests
import argparse 
import subprocess
import os
import json 
import glob
import sys
def download(path, link, run=True):
    r = requests.get(link, verify=False)
    if r.status_code!=200:
        print("Bad response from server")
        sys.exit(1)
    lines = r.text.split("\n")
    begin = lines.index(list(filter(lambda k: 'export SCRAM_ARCH' in k, lines))[0])
    scram = lines[begin].split("=")[-1]
    end = lines.index(list(filter(lambda k: 'EndOfTestFile' == k, lines))[0])
    lines = lines[begin:end]
    lines = list(map(lambda k: k+'\n', lines))
    if not os.path.isdir(path):
        os.makedirs(path)
    fileName = "script.sh" 
    pathToFile = path + "/" + fileName
    with open(pathToFile, "w") as file:
        file.writelines(lines)

    process = subprocess.Popen("chmod +x {}".format(pathToFile),shell=True)
    process.wait()
    if run:
        process = subprocess.Popen("cd {}; ./{}; cd -".format(path, fileName),shell=True)
        process.wait()
        fs = glob.glob(path+"/*.py")
        print()
        if len(fs)==0:
            print("No .py generateed")
            sys.exit(1)
        elif len(fs)==1:
            name = fs[0].split("/")[-1]
            process = subprocess.Popen("cd {}; cp {} ../; cd -".format(path, name),shell=True)
            process.wait()
        else:
            name = list(map(lambda k: k.split("/")[-1], fs))
            for n in name:
                process = subprocess.Popen("cd {}; cp {} ../; cd -".format(path, n),shell=True)
                process.wait()
        fs = glob.glob(path+"/CMSSW*")
        if len(fs)==1:
            name = {"release": fs[0].split("/")[-1], "filename": name}
        print("\n\nDeleting folder\n\n")
        process = subprocess.Popen("rm -r {}".format(path),shell=True)
        process.wait()
        return scram,name
    return scram,""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y","--year", help="Year" , required=True)
    parser.add_argument("-s","--steps", help="Step to download", nargs="+", required=True)


    args = parser.parse_args()
    with open("Steps.json") as file:
        Steps = json.load(file) 
    totalYears = ["2018", "2017", "2016"]
    if args.year not in totalYears:
        print("Year not valid")
        print("Valid years are: {}".format(", ".join(totalYears)))
        sys.exit(1)
    totalSteps = ["lhe", "premix", "miniAOD", "nanoAOD"]
    if len(list(filter(lambda k: k not in totalSteps, args.steps)))>0:
        print("Steps not valid")
        print("Valid steps are: {}".format(", ".join(totalSteps)))
        sys.exit(1)
    print("\n\nSteps to be performed for year {}".format(args.year))
    for step in args.steps:
        print(step)
    print("\n\n")
    for step in args.steps:
        print("\n\nNow dowloading config for step: {} and year: {}\n\n".format(step, args.year))
        scram,name = download("data/input_{}/{}".format(args.year, step),Steps[args.year][step]['link'])
        print(name)
        if isinstance(name, str) or isinstance(name, list):
            Steps[args.year][step]['filename'] = name
        else:
            Steps[args.year][step]['filename'] = name["filename"]
            Steps[args.year][step]['release'] = name["release"]
        Steps[args.year][step]['SCRAM_ARCH'] = scram 
        

    
    with open("Steps.json", "w") as file:
        json.dump(Steps,file,indent=4, sort_keys=True)