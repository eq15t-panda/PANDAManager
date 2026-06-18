# About 

PANDAManager is a small Python-based laboratory data-acquisition and plotting project (notebooks + helpers) used to 
control instruments, acquire datasets (power meter, oscilloscope, temperature controller, etc.), and produce reproducible 
plots. 
The repository groups Jupyter notebooks for interactive acquisition and plotting, instrument configuration JSONs, 
raw/processed data, and small utility modules that implement common helpers.

# Repository layout


- `launch_pyrpl.ipynb`: Jupyter notebook to launch the Pyrpl GUI and configure the Pyrpl instrument;
- `requirements_base.txt `: Base requirements for the project, different from the PYRPL kernel;
- `requirements_pyrpl.txt`: Requirements for the PYRPL kernel;
 

- `utils/`:
  - `naming.py`: Helper functions to generate names for files and directories;
  - `oc3.py`: Helper functions to control the OC3 temperature controller;
  - `plot_style.py`: Helper functions to set plot style;
  - `pm100a.py`: Helper functions to control the PM100A power meter;
  - `temperature.py`: Helper functions to generate temperature lists;


- `acquisition/`:
  - `acquisition_knife`: Notebook for knife-edge data acquisition;
  - `acquisition_nkt`: Notebook for NKT laser data acquisition;
  - `acquisition_oscillo`: Notebook for oscilloscope data acquisition;
  - `acquisition_pm100a`: Notebook for PM100A power meter data acquisition;
  - `acquisition_shg`: Notebook for SHG data acquisition;
  - `acquisition_rigol`: Notebook for Rigol function generator data acquisition;


- `plot/`:
  - `figure/`: Save folder for figures;
  - `plot_oscillo`: Notebook for oscilloscope data plotting;
  - `plot_pm100a`: Notebook for PM100A power meter data plotting;
  - `plot_shg`: Notebook for SHG data plotting;

# Data management

## Naming system

It is essential to keep a consistent way of naming datafiles.
Not only for tracking, but also to easily plot them in the plotting notebook.
The method is in `utils/naming.py` under the name `make_run_dir(data_dir: str, meas: str, sample: str)`.

## Acquisition

For acquisition notebook proceed as follow:

1. First, setup at the beginning of the notebook the run directory
```python
DATA_DIR = "data/some_name"
os.makedirs(DATA_DIR, exist_ok=True)
```

2. Second, define what is the measurement and what is it you are measuring
```python
MEAS = "some_measurement"
SAMPLE = "some_sample"

RUN_DIR = make_run_dir(data_dir=DATA_DIR, meas=MEAS, sample=SAMPLE)
ACQ_CELL = f"{MEAS}_{SAMPLE}"
```

3. Once everything is ready, you need to start the acquisition in a dedicated cell
```python
aqm = AcquisitionAnalysisManager(RUN_DIR)
aqm.acquisition_cell(ACQ_CELL)
# code follows here
```

4. The acquisition ends by saving the data recorded. It works like a dictionnary
```python
aqm.save_acquisition(data1=data1, data2=data2, ...)
```

## Plot

There are two situations when plotting data: either you want to plot an individual file, or your measurement involves separate files.
Either way, to load data, you can first do:
```python
# Folder
path_folder_data = r"./data/some_name/some_acquisition_folder/"
folder_data_files = os.listdir(path_folder_data)
print(folder_data_files)
# Run names
name_exp = 'some_run_name'
# List all files in the folder
folder_data_files = os.listdir(path_folder_data + '/' + name_exp)
print(folder_data_files)
```

Then you can load individual file:
```python
# Choose file
name = "data_filename.h5"

full_path = os.path.join(path_folder_data, name_exp, name)
print(full_path)

# Init acquisition analysis manager
aqm = AcquisitionAnalysisManager(full_path)
aqm.analysis_cell(filename=full_path)
print(aqm.data)
```

Or load several files. 
In this case, you can do a simple `for` loop, and at each iteration, call the `analysis_cell`:

```python
aqm = AcquisitionAnalysisManager(full_path)

data_to_grab = []

for filename in folder_data_files:
    aqm.analysis_cell(filename=os.path.join(full_path, filename))
    data_to_grab.append(aqm.data["some_data_name"])
    ...
```

# Remote control and PyVISA

Every electronic in the room is connected via PYVISA expect for the OC3 temperature controller which communicates via pyserial and the NKT laser which use the NKT DLL library.

## Thorlabs PM

The thorlabs powermeters sometimes failed to connect via pyvisa, even though they are properly listed in the ressource manager. By default, they use a USB protocole instead of the NI-visa. To change this:

1. Open the software called **Optical Parameter Monitor**
2. Double click on the rectangle with the device's name (if you do not see any device, add one using the plus sign)

![alt text](image.png)

3. The **driver switcher** pannel should open. You might need to restart it as admin.
4. Rescan, and click on **switch all to NI-VISA**.

![alt text](image-1.png)

5. Go back in the notebook, refresh the `rm = pv.ResourceManager()`, the powermeter should connect via pyvisa now.