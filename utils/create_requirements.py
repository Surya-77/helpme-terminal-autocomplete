import os
import sys
import importlib.util
from importlib.metadata import version, PackageNotFoundError

def find_project_root():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.exists(os.path.join(current_dir, '.git')):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise Exception("Project root not found. Make sure you're in a git repository.")
        current_dir = parent_dir

def get_installed_version(module_name):
    try:
        return version(module_name)
    except PackageNotFoundError:
        return None

def is_local_module(module_name, project_root):
    return os.path.exists(os.path.join(project_root, module_name)) or \
           os.path.exists(os.path.join(project_root, module_name + '.py'))

def generate_requirements_file():
    project_root = find_project_root()
    modules = set()

    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    try:
                        for line in f:
                            if line.strip().startswith('import ') or line.strip().startswith('from '):
                                parts = line.split()
                                if parts[0] == 'import':
                                    modules.add(parts[1].split('.')[0])
                                elif parts[0] == 'from' and parts[1] != '.':
                                    modules.add(parts[1].split('.')[0])
                    except UnicodeDecodeError:
                        print(f"Warning: Unable to read {file_path}. Skipping.")

    # Remove standard library modules and local modules
    modules = {m for m in modules if not is_local_module(m, project_root) and importlib.util.find_spec(m) is not None}

    # Format the modules for requirements.txt with installed versions
    formatted_modules = []
    for module in modules:
        version = get_installed_version(module)
        if version:
            formatted_modules.append(f'{module}=={version}')
        else:
            formatted_modules.append(module)

    # Sort the modules alphabetically
    formatted_modules.sort()

    # Write to requirements.txt in the project root
    requirements_path = os.path.join(project_root, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        for module in formatted_modules:
            f.write(f"{module}\n")

    print(f"Requirements file generated at: {requirements_path}")

if __name__ == "__main__":
    generate_requirements_file()