## EEG Analysis in both MATLAB and Python

These scripts will read in scored EEG files and output key metrics into Excel. These metrics inlcude:
- Total time in wake, NREM, or REM sleep (of user-specified bin size; default = 2 hours)
- Total number of wake, NREM, and REM sleep bouts (of user-specified bin size; default is 12 hours)
- Average length of wake, NREM, and REM sleep bouts (of user-specified bin size; default is 12 hours)
- Wake bout distribution
--- Histogram of number of wake bouts of a fixed length (e.g., 0-16 seconds, 16-32 seconds, 32-64 seconds, etc.)

This code was used to analyze EEG for the following manuscripts:
Perron IJ et al. Diet/Energy Balance Affect Sleep and Wakefulness Independent of Body Weight. PMID: 26158893.
