import os
import pandas as pd

class SmartwattsDataProcessor:
    def __init__(self, root_directory):
        self.root_directory = root_directory

    def convertEpochToTimestamp(self, epochSinceMs):
        timestamp = pd.to_datetime(int(epochSinceMs), unit='ms')
        return timestamp.replace(microsecond=0)

    def computeTotalPower(self, run_number, workload):
        os.makedirs(f"{self.root_directory}/processed-results/smartwatts/run_{run_number}/", exist_ok=True)

        output_file = f'{self.root_directory}/processed-results/smartwatts/run_{run_number}/run_{run_number}-{workload}.csv'
        timestamp_power = {}

        subdirectories_path = os.path.join(self.root_directory, f'smartwatts/run_{run_number}/run_{run_number}-{workload}')
        subdirectories = [subdir for subdir in os.listdir(subdirectories_path) if subdir.startswith('cpu-train-ticketing-system')]

        for subdir in subdirectories:
            subdir_path = os.path.join(subdirectories_path, subdir)
            power_report_file = os.path.join(subdir_path, 'PowerReport.csv')
            df = pd.read_csv(power_report_file)
            df["timestamp"] = df["timestamp"].apply(self.convertEpochToTimestamp)
            df_resampled = df.set_index('timestamp').resample('1S').first()

            for timestamp, power in zip(df_resampled.index, df_resampled['power']):
                if not pd.isna(power): 
                    if timestamp in timestamp_power:
                        timestamp_power[timestamp] += power
                    else:
                        timestamp_power[timestamp] = power

        output_df = pd.DataFrame(list(timestamp_power.items()), columns=['timestamp', 'total_power'])
        output_df.sort_values(by='timestamp', inplace=True)

        output_df.to_csv(output_file, index=False)
        print(f"Output file '{output_file}' has been created.")

    def process_runs(self):
        for run_number in range(0, 61):
            if run_number not in [2, 9, 13, 14, 16, 20, 29, 33, 46, 49, 54]:
                self.computeTotalPower(run_number, 'HIGH')
                self.computeTotalPower(run_number, 'MEDIUM')
                self.computeTotalPower(run_number, 'LOW')
