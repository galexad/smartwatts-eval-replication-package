import matplotlib.pyplot as plt
import pandas as pd
import os
import random


class PowerDataAnalyzer:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.workloads = ['HIGH', 'MEDIUM', 'LOW']
        self.run_numbers = []

        # Filtering the successful runs
        for i in range(0,61):
            if i not in [2,9,13,14,16,20,29,33,46,49,54]:
                self.run_numbers.append(i)

    def plot_power_comparison(self, data_files, num_data_points=200):
        fig, axs = plt.subplots(1, len(data_files), figsize=(6 * len(data_files), 6))
        plt.subplots_adjust(wspace=0.4)

        for i, (workload, data_file) in enumerate(data_files.items()):
            df = pd.read_csv(data_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['time_elapsed'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

            axs[i].plot(df['time_elapsed'][:num_data_points], df['smartwatts_power'][:num_data_points], label='Smartwatts')
            axs[i].plot(df['time_elapsed'][:num_data_points], df['wattsup_power'][:num_data_points], label='Watts Up Pro')

            axs[i].set_ylabel('Power (Watts)')
            axs[i].set_xlabel('Time (seconds)')
            axs[i].set_title(f'{workload.capitalize()} Workload')

            x_min = df['time_elapsed'][:num_data_points].min()
            x_max = df['time_elapsed'][:num_data_points].max()
            axs[i].set_xlim(x_min, x_max)

            y_upper_bound = df['wattsup_power'][:num_data_points].max() + 20
            axs[i].set_ylim(0, y_upper_bound)

            axs[i].legend()

        return fig

    
    def get_files_by_workload(self, run_number, workload):
        run_directory = os.path.join(self.root_directory, f'run_{run_number}')
        return os.path.join(run_directory, f'run_{run_number}-{workload}.csv')

    # Calculate the error rate for each workload
    def compute_error_rate(self, workload_files):
        dfs = {}
        for workload, files in workload_files.items():
            workload_dfs = []
            for file in files:
                df = pd.read_csv(file)
                df = df.drop(df.columns[0], axis=1)
                df['workload'] = workload
                workload_dfs.append(df)
            merged_df = pd.concat(workload_dfs)
            dfs[workload] = merged_df

        for workload, df in dfs.items():
            df['error_rate'] = abs(df['smartwatts_power'] - df['wattsup_power'])/df['wattsup_power'] * 100    
 
        return dfs

    def plot_error_rate_boxplot(self, dfs):
        plt.figure()
        plt.boxplot([df['error_rate'] for df in dfs.values()], labels = list(dfs.keys()), whis=3.5)
        plt.ylabel('Error Rate (%)')
        plt.show()
    

    def get_error_df(self):
        sample_files = {workload: [] for workload in self.workloads}
        for run_number in self.run_numbers:
            for workload in self.workloads:
                sample_files[workload].append(self.get_files_by_workload(run_number, workload))

        # Read the CSV files for each workload and create separate DataFrames
        workload_files = {
            'High': sample_files['HIGH'],
            'Medium': sample_files['MEDIUM'],
            'Low': sample_files['LOW']
        }

        dfs = self.compute_error_rate(workload_files)
        return dfs

    def plot_random_sample(self, elapsed_time):
        random_number = random.choice([0,1])

        data_files = {}
        for workload in self.workloads:
            data_file = f'{self.root_directory}run_{random_number}/run_{random_number}-{workload}.csv'
            data_files[workload] = data_file

        self.plot_power_comparison(data_files, elapsed_time)
