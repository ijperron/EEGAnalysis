import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eeg-sleep-analysis",
    version="1.1.4",
    author="Isaac J. Perron",
    author_email="ijperron@gmail.com",
    description="Package to analyze EEG-scored sleep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ijperron/EEGAnalysis",
    packages=["EEGAnalysis"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True,
    install_requires=["PySimpleGUI"],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "sleep_analysis=EEGAnalysis.__main__:main",
        ]
    }
)