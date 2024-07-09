from setuptools import setup, find_packages
import os

# Read the contents of requirements.txt
def read_requirements():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(current_dir, 'requirements.txt'), encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("Warning: requirements.txt not found. Using default requirements.")
        return ["google-generativeai", "click", "python-dotenv", "groq"]

setup(
    name="helpme",
    version="0.1.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={"console_scripts": ["helpme=cli.main:run_process"]},
)

