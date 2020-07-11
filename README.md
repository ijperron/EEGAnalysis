## Python scripts to analyze sleep-scored EEG files

#### Overview
EEG-based murine sleep studies use waveform signature to define three behavioral states--wake, rapid eye movement (REM) sleep, and non-REM (NREM) sleep. These recordings are long (typically 6-48 hours) and broken down into short epochs (usually 4-10 seconds). Either automatic or manual scoring is required to label each epoch as wake, NREM, or REM (and this package does not assist with this scoring).

These scripts will read in scored EEG files and output key metrics into Excel. These metrics inlcude:
- Total time in wake, NREM, or REM sleep of user-specified bin size (default = 2 hours)
- Total number of wake, NREM, and REM sleep bouts of user-specified bin size (default = 12 hours)
- Average length of wake, NREM, and REM sleep bouts of user-specified bin size (default = 12 hours)
- Wake bout distribution, or a frequency of wake bouts by their duration. This binning can be specified by user; default is power of 2 (16 seconds - 2048 seconds).
- Spectral analysis (to be completed)

This code was originally built in MATLAB, which was first used to analyze results in 
[Perron IJ et al.](https://pubmed.ncbi.nlm.nih.gov/26158893/).

If you use this analysis package, please cite this repo.

#### Detailed installation istructions for first time users

**For users comfortable with python/anaconda, skip to last step**

1. Download and [install anaconda](https://www.anaconda.com/products/individual), if you have not done so already.

2. On your local machine, open anaconda shell. If you see (base), that means python is active in root environment. 

3. Non-first time users skip to step 4.. First time users should create new virtual environment:
> conda create --name env3

In this example, env3 is the virutal environment name; it can be named whatever you prefer.

4. Activate virutal environment:
> conda activate env3

The terminal should now show (env3) instead of (base) if this worked correctly.

5. Install eeg-sleep-analysis package: 
> pip install eeg-sleep-analysis

#### Detailed user instructions
6. In terminal, navigate to your preferred directory.
To list directory routes:
> ls -la (for mac/linux)
>
> dir (for windows)

To change directory:
> cd <directory route> (for mac/linux/windows)

7. Type the command to launch the GUI
> python -m EEGAnalysis

8. For a new experiment, create a config.txt file. This will be created in your current directory. You must open and edit this config file with correct file directories and experiment details.

9. In the GUI, navigate to the correct config.txt file.

10. Create a new conditions.csv. If the config.txt file is setup properly, this should be generated automatically and correctly. However, it is highly recommended to double check conditions.csv before running analysis. 

11. In the GUI, navigate to the correct conditions.csv file.

12. Run the analysis. Results will be output into the specified directory in the config.txt file.

#### Contact information
Please direct any questions or suggestions to ijperron@gmail.com

#### Acknowledgements
Thank you to the members of the [University of Pennsylvania Center for Sleep and Circadian Neurobiology](https://www.med.upenn.edu/sleepctr/), especially Drs. Allan Pack and Sigrid Veasey. 
Thank you to Cameron Jones for his help to debug this program.

