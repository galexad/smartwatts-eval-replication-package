# Assessing CPU Energy as Proxy for Machine Energy Consumption in Containerized Applications

This repository contains raw data and complete data analysis of the results obtained in the empirical experiments conducted with the aim to assess the CPU energy as proxy for machine energy consumption in containerized applications


The repository consists of three main directories:
- **figures**: figures in *pdf* format created as a result of the data analysis. All figures in this directory are illustrated in the paper, where they are described in detail;
- **raw_data**: raw data obtained from the experiment in *csv* format. The entire content of this directory is the direct output of the experiment conducted via the Experiment Runner(ER) experiment orchestration tool. For tool configuration and further details, refer to the [ER GitHub repository](https://github.com/S2-group/experiment-runner);
- **data_analysis**: directory containing the source code of Python Jupyter notebooks documenting the complete data analysis process and the source code used for statistical analysis. The analysis is conducted with Python version 3.8.10 on Ubuntu 20.04.

## Repository structure

For the data processing, one should first run the ``` main.py ``` Python file. Following this, it is then possible to visualize and analyze the data using the ``` data-analysis.ipynb ``` scripts.
