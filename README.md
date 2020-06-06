## Python scripts to analyze sleep-scored EEG files

EEG-based murine sleep studies use waveform signature to define three behavioral states--wake, rapid eye movement (REM) sleep, and non-REM (NREM) sleep. These recordings are long (typically 6-48 hours) and broken down into short epochs (usually 4-10 seconds). Either automatic or manual scoring is required to label each epoch as wake, NREM, or REM (and this package does not assist with this scoring).

These scripts will read in scored EEG files and output key metrics into Excel. These metrics inlcude:
- Total time in wake, NREM, or REM sleep of user-specified bin size (default = 2 hours)
- Total number of wake, NREM, and REM sleep bouts of user-specified bin size (default = 12 hours)
- Average length of wake, NREM, and REM sleep bouts of user-specified bin size (default = 12 hours)
- Wake bout distribution, or a frequency of wake bouts by their duration. This binning can be specified by user; default is power of 2 (16 seconds - 2048 seconds).
- Spectral analysis (to be completed)

This code was originally built in MATLAB, which was first used to analyze results in Perron IJ et al. (PMID: 26158893.)

If you use this analysis package, please cite this repo.


