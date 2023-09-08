import argparse
import json
import subprocess
import os
import shutil
import platform
import stat
from configparser import ConfigParser

libPath='lib/{}'
externalPath='external/{}'

def updateAndObtainSubmodules():
    try:
        pass
        subprocess.check_call(["git", "submodule", "sync", "--recursive"])
        subprocess.check_call(["git", "submodule", "update", "--init", "--recursive"])
    except Exception as e:
        print(f"Submodule update exception of type {type(e)}. With message: {e}")
        exit(1)


def processBuildHeaderOnly(dependencyDetails,dependencyCatalog):
    pass

def processBuildNotHeaderOnly(dependencyDetails,dependencyCatalog):
    repoLinks = dependencyDetails["repository"]
    libInstallPath = libPath.format(dependencyCatalog)
    if os.path.isdir(libInstallPath):
        exit(1)

    os.mkdir(libInstallPath)

    if isinstance(repoLinks,dict):
        for dependencyName, details in repoLinks.items():
            sourceFile=externalPath.format(dependencyName)
            buildSingleNotHeaderOnly(dependencyDetails['cmakeCustomParams'],dependencyName,libInstallPath,sourceFile)
    else:
        sourceFile=externalPath.format(dependencyCatalog)
        buildSingleNotHeaderOnly(dependencyDetails['cmakeCustomParams'],dependencyCatalog,libInstallPath,sourceFile)

def buildSingleNotHeaderOnly(cmakeCustomParams,dependencyName,libInstallPath,sourceFile):
    try:
        print(dependencyName,sourceFile)
        command = f"cmake -DCMAKE_INSTALL_PREFIX={libInstallPath} -G Ninja {sourceFile} -B {sourceFile}"
        subprocess.run(command)
        print("test")
        buildCatalog=f"{sourceFile}/{dependencyName}-build"
        os.mkdir(buildCatalog)
        subprocess.run(["cmake", "--build", ".."], cwd=buildCatalog)
        subprocess.run(["cmake", "--install", ".."], cwd=buildCatalog)
    except Exception as e:
        print(f"Package building process error of type {type(e)} with message: {e}")
        exit(1)


def handleBuild(jsonData):
    for dependencyCatalog, dependencyDetails in jsonData["dependencies"].items():
        if dependencyDetails["isHeaderOnly"]:
            processBuildHeaderOnly(dependencyDetails,dependencyCatalog)
        else:
            processBuildNotHeaderOnly(dependencyDetails,dependencyCatalog)

def removeFromCatalog(directory_path):
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            if name != ".git-keep":
                file=os.path.join(root, name)
                os.chmod(file, stat.S_IWUSR)
                os.remove(file)
        for name in dirs:
            print(f"Deleting from {name}")
            shutil.rmtree(os.path.join(root, name))


def removeAllDependencies():
    removeFromCatalog(externalPath.format(""))
    removeFromCatalog(libPath.format(""))

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        try:
            print(e.stderr.decode('utf-8'))
        except UnicodeDecodeError:
            print("Could not decode error message.")

def removeOldSubModules():
    if not os.path.isfile('.gitmodules'):
        print("Plik .gitmodules nie istnieje w tym repozytorium.")
        return

    with open('.gitmodules', 'r') as file:
        lines = file.readlines()

    submodules = [line.split('=')[1].strip() for line in lines if line.startswith('path')]

    for submodule in submodules:
        subprocess.run(['git', 'config', '-f', '.git/config', '--remove-section', f'submodule.{submodule}'], stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'rm', '--cached', submodule])
        print(f"Deleted submoduł: {submodule}")

    removeFromCatalog('.git/modules')

    os.remove('.gitmodules')


def handleSubmodulesModification(jsonData):
    removeOldSubModules()
    with open('.gitmodules', 'w') as f:
        pass

    for dependencyCatalog, dependencyDetails in jsonData["dependencies"].items():
        repoLinks=dependencyDetails['repository']
        if dependencyDetails["isHeaderOnly"]:
            installationPath=libPath.format(dependencyCatalog)

            if isinstance(repoLinks,dict):
                for dependencyName, details in repoLinks.items():
                    finalPath=os.path.join(installationPath,dependencyName)
                    run_command(f"git submodule add -f --branch {dependencyDetails['branch']} {repoLinks[dependencyName]} {finalPath}")
            else:
                run_command(f"git submodule add -f --branch {dependencyDetails['branch']} {dependencyDetails['repository']} {installationPath}")
        else:
            if isinstance(repoLinks,dict):
                for dependencyName, details in repoLinks.items():
                    finalPath=externalPath.format(dependencyName)
                    run_command(f"git submodule add -f --branch {dependencyDetails['branch']} {repoLinks[dependencyName]} {finalPath}")
            else:
                installationPath=externalPath.format(dependencyCatalog)
                run_command(f"git submodule add -f --branch {dependencyDetails['branch']} {dependencyDetails['repository']} {installationPath}")
    updateAndObtainSubmodules()
def main(args):
    if args.force_rebuild:
        print("Removing previous dependencies!")
        removeAllDependencies()

    with open(args.dependenciesFile, "r") as file:
        print("Json file obtained!")
        jsonData = json.load(file)

    if args.update:
        handleSubmodulesModification(jsonData)
    else:
        updateAndObtainSubmodules()

    handleBuild(jsonData)


def parseInputFlags():
    parser = argparse.ArgumentParser(
        description="Download, build and install all project needed libraries specified in dependencies.json file. Without any flags provided script would only build currently tracked liblaries. To add, modify or remove a dependency. Modify json file and run this script with --update flag.")

    parser.add_argument("--force-rebuild", action="store_true",
                        help="Force rebuild all tracked libraries even if they are built in the current project")
    parser.add_argument("--update", action="store_true",
                        help="Update tracked files list with new dependencies.json data")
    parser.add_argument("--json", dest="dependenciesFile", action="store_const",
                        const="dependencies.json",default="dependencies.json",
                        help="Provide path to dependencies.json file. Default: dependencies.json")

    return parser.parse_args()


if __name__ == "__main__":
    inputFlags = parseInputFlags()
    main(inputFlags)
