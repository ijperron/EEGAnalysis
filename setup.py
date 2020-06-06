import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eeg-sleep-analysis-ijperron", # Replace with your own username
    version="0.0.1",
    author="Isaac Perron",
    author_email="ijperron@gmail.com",
    description="Package to analyze EEG-scored sleep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ijperron/EEGAnalysis",
    packages=setuptools.find_packages(),
    #classifiers=[
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",
    #    "Operating System :: OS Independent",
    #],
    python_requires='>=3.6',
)