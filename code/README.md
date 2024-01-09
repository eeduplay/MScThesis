# Argon LTP Project Code - Analysis and Modeling
This directory contains the python code used for various models and for data processing/analysis. You can access the dataset associated with this thesis here:

Duplay, Emmanuel, Gabriel Dubé, and Siera Riel. “Argon Laser-Sustained Plasma Footage, Pressure Data, and Spectral Data.” 4TU.ResearchData, 2023. https://doi.org/10.4121/04ad8110-e3c4-4971-99ce-8a6c537166d6.


## Setup
Running the scripts and jupyter notebooks in this project will require some setup. This codebase requires Python 3.11 or greater.

### 1. Installing packages
You can install the project's environment using [pipenv](https://pipenv.pypa.io/en/latest/) by executing the following command in this directory (i.e., `MScThesis/code/.`):
```
pipenv install
```

### 2. Setting up the .env file (optional)
To keep this repository clean, the experimental data collected throughout this project is not included. This data should be downloaded (see introduction) in a directory of your choosing. You should then indicate the full path to the dataset with an environment variable named `DATAPATH` using a `.env` file.

For example, if this repo and the dataset are saved to your computer as follows:
```python
C:\My Repositories\
└── MScThesis\
    ├── .vscode\
    ├── cachedata\
    ├── code\
    │   ├── .env  # Environment variable file (added manually)
    │   ├── README.md  # The file you're reading right now
    │   └── ...
    └── ...
D:\
├── ArgonLSPData\  # Root directory of dataset
│   ├── LSP\
│   ├── Pressure Data\
│   ├── Pulse Shapes\
│   ├── Spectra\
│   └── README.md
└── ...
```

The *full path* to the dataset is `D:\ArgonLSPData\`. Therefore, to properly communicate this to the analysis scripts, a file named `.env` must be created in `C:\MScThesis\code\` with the following contents:
```properties
DATAPATH=D:\ArgonLSPData\
```

You're all set!

#### Aside: Accessing the value of DATAPATH
If you intend on writing your own code in this repo and would like to access the value of this environment variable, you can do so as follows:
```python
from dotenv import load_dotenv
load_dotenv()
from os import getenv

my_data_path = getenv('DATAPATH')

print(my_data_path)
# OUTPUT:
# D:\ArgonLSPData\
```

## Usage
Make sure to activate the `pipenv` environment (in your IDE or in the command-line) before running the scripts.

Most of the scripts in this repo are designed to be run from the root directory (i.e., `MScThesis/.`), because VSCode's default behavior when running code is to run it from the repo root. This should not be an issue if you are also using VSCode. If not, just make sure to run the scripts (say we're running `efficiency.py`) as follows:
```powershell
C:\My Repositories\MScThesis\code> pipenv shell  # activates the pipenv environment
C:\My Repositories\MScThesis\code> cd ../
C:\My Repositories\MScThesis> python ./code/efficiency.py
```