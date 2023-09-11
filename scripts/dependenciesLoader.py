import argparse
import json
import subprocess
import os
import shutil
import stat

LIB_PATH = 'lib/{}'
EXTERNAL_PATH = 'external/{}'


def update_and_obtain_submodules():
    """Updates and initializes the submodules present in the repository."""
    try:
        subprocess.check_call(["git", "submodule", "sync", "--recursive"])
        subprocess.check_call(["git", "submodule", "update", "--init", "--recursive"])
    except Exception as e:
        print(f"Submodule update exception of type {type(e)}. With message: {e}")
        exit(1)


def process_build(json_data):
    """Processes the build based on the data present in the JSON configuration file."""
    for dependency_catalog, dependency_details in json_data["dependencies"].items():
        if dependency_details["isHeaderOnly"]:
            process_build_header_only(dependency_details, dependency_catalog)
        else:
            process_build_not_header_only(dependency_details, dependency_catalog)


def process_build_header_only(dependency_details, dependency_catalog):
    """Processes the build for header-only dependencies.

    Args:
        dependency_details (dict): Details of the dependency.
        dependency_catalog (str): Name of the dependency.
    """
    pass


def process_build_not_header_only(dependency_details, dependency_catalog):
    """Processes the build for non-header-only dependencies.

    Args:
        dependency_details (dict): Details of the dependency.
        dependency_catalog (str): Name of the dependency.
    """
    repo_links = dependency_details["repository"]
    lib_install_path = LIB_PATH.format(dependency_catalog)

    if os.path.isdir(lib_install_path):
        print(f"{dependency_catalog} already installed. Skipped.")
        return

    os.mkdir(lib_install_path)
    process_repository_links(repo_links, dependency_details, dependency_catalog, lib_install_path)


def process_repository_links(repo_links, dependency_details, dependency_catalog, lib_install_path):
    """Processes repository links and initiate the build process for each link.

    Args:
        repo_links (str/dict): Repository links.
        dependency_details (dict): Details of the dependency.
        dependency_catalog (str): Name of the dependency.
        lib_install_path (str): Path to install the library.
    """
    if isinstance(repo_links, dict):
        for dependency_name, details in repo_links.items():
            source_file = EXTERNAL_PATH.format(dependency_name)
            build_single_not_header_only(dependency_details['cmakeCustomParams'], dependency_name, lib_install_path, source_file)
    else:
        source_file = EXTERNAL_PATH.format(dependency_catalog)
        build_single_not_header_only(dependency_details['cmakeCustomParams'], dependency_catalog, lib_install_path, source_file)


def build_single_not_header_only(cmake_custom_params, dependency_name, lib_install_path, source_file):
    """Builds a single non-header-only dependency.

    Args:
        cmake_custom_params (str): Custom parameters for the CMake.
        dependency_name (str): Name of the dependency.
        lib_install_path (str): Path to install the library.
        source_file (str): Path to the source file.
    """
    try:
        print(dependency_name, source_file)
        execute_build_commands(cmake_custom_params, dependency_name, lib_install_path, source_file)
    except Exception as e:
        print(f"Package building process error of type {type(e)} with message: {e}")
        exit(1)


def execute_build_commands(cmake_custom_params, dependency_name, lib_install_path, source_file):
    """Executes the build commands using subprocess.

    Args:
        cmake_custom_params (str): Custom parameters for the CMake.
        dependency_name (str): Name of the dependency.
        lib_install_path (str): Path to install the library.
        source_file (str): Path to the source file.
    """
    command = f"cmake -DCMAKE_INSTALL_PREFIX={lib_install_path} -G Ninja {source_file} -B {source_file}"
    subprocess.run(command)
    print("test")
    build_catalog = f"{source_file}/{dependency_name}-build"
    os.mkdir(build_catalog)
    subprocess.run(["cmake", "--build", ".."], cwd=build_catalog)
    subprocess.run(["cmake", "--install", ".."], cwd=build_catalog)


def remove_from_catalog(directory_path):
    """Removes files and directories from a given path, excluding .git-keep files.

    Args:
        directory_path (str): The path to remove files and directories from.
    """
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            if name != ".git-keep":
                file_path = os.path.join(root, name)
                os.chmod(file_path, stat.S_IWUSR)
                os.remove(file_path)
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))


def remove_all_dependencies():
    """Removes all dependencies by deleting files and directories in the specified paths."""
    remove_from_catalog(EXTERNAL_PATH.format(""))
    remove_from_catalog(LIB_PATH.format(""))


def run_command(command):
    """Runs a shell command and prints the output or error message.

    Args:
        command (str): The shell command to run.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        try:
            print(e.stderr.decode('utf-8'))
        except UnicodeDecodeError:
            print("Could not decode error message.")


def remove_old_submodules():
    """Removes old submodules from the repository."""
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

    remove_from_catalog('.git/modules')
    os.remove('.gitmodules')


def handle_submodules_modification(json_data):
    """Handles the modifications to submodules based on the data present in the JSON configuration file."""
    remove_old_submodules()
    with open('.gitmodules', 'w') as f:
        pass

    for dependency_catalog, dependency_details in json_data["dependencies"].items():
        repo_links = dependency_details['repository']
        if dependency_details["isHeaderOnly"]:
            installation_path = LIB_PATH.format(dependency_catalog)
        else:
            installation_path = EXTERNAL_PATH.format(dependency_catalog)

        handle_repository_links(installation_path, repo_links, dependency_details)


def handle_repository_links(installation_path, repo_links, dependency_details):
    """Handles repository links and modifies submodules accordingly.

    Args:
        installation_path (str): Path to install the submodule.
        repo_links (str/dict): Repository links.
        dependency_details (dict): Details of the dependency.
    """
    if isinstance(repo_links, dict):
        for dependency_name, details in repo_links.items():
            final_path = os.path.join(installation_path, dependency_name)
            run_command(f"git submodule add -f --branch {dependency_details['branch']} {details['repository']} {final_path}")
    else:
        run_command(f"git submodule add -f --branch {dependency_details['branch']} {repo_links} {installation_path}")


def main(args):
    """Main function that processes input arguments and initiates appropriate functions.

    Args:
        args (argparse.Namespace): Parsed command line arguments.
    """
    if args.force_rebuild:
        print("Removing previous dependencies!")
        remove_all_dependencies()

    json_data = load_json_data(args.dependencies_file)

    if args.update:
        handle_submodules_modification(json_data)
    else:
        update_and_obtain_submodules()

    process_build(json_data)


def load_json_data(dependencies_file):
    """Loads JSON data from the specified file path.

    Args:
        dependencies_file (str): Path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(dependencies_file, "r") as file:
        print("Json file obtained!")
        return json.load(file)


def parse_input_flags():
    """Parses input flags from the command line.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Download, build and install all project needed libraries specified in dependencies.json file. Without any flags provided script would only build currently tracked libraries. To add, modify or remove a dependency modify json file and run this script with --update flag.")

    parser.add_argument("--force-rebuild", action="store_true", help="Force rebuild all tracked libraries even if they are built in the current project")
    parser.add_argument("--update", action="store_true", help="Update tracked files list with new dependencies.json data")
    parser.add_argument("--json", dest="dependencies_file", action="store_const", const="dependencies.json", default="dependencies.json", help="Provide path to dependencies.json file. Default: dependencies.json")

    return parser.parse_args()


if __name__ == "__main__":
    input_flags = parse_input_flags()
    main(input_flags)
