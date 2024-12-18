from setuptools import setup, find_packages

def read_requirements(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f if line and not line.startswith('#')]

setup(
    name='ESA_UNICEF_DengueForecastProject',
    version='0.1',
    packages=find_packages(where='src'),  # Specify 'src' as the package directory
    package_dir={'': 'src'},              # Map the root package to 'src'
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
)