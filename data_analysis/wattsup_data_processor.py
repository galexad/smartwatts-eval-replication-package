import os 
import pandas as pd

class WattsupDataProcessor:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.runs_dict = self.populate_runs_dict()

    def convertEpochToTimestamp(self, epochSinceMs):
        timestamp = pd.to_datetime(int(epochSinceMs), unit='ms')
        return timestamp.replace(microsecond=0)

    def process(self, file1, file2, run_number, sample):
        GL2_df = pd.read_csv(file1, delimiter="\s+", names=["timestamp", "power"], usecols=[0, 2])
        GL3_df = pd.read_csv(file2, delimiter="\s+", names=["timestamp", "power"], usecols=[0, 2])

        GL2_df["timestamp"] = GL2_df["timestamp"].apply(self.convertEpochToTimestamp)
        GL3_df["timestamp"] = GL3_df["timestamp"].apply(self.convertEpochToTimestamp)

        merged_df = pd.merge(GL2_df, GL3_df, left_on="timestamp", right_on="timestamp")
        merged_df["power"] = merged_df["power_x"] + merged_df["power_y"]
        sample_name = sample[:-4]

        result_df = merged_df[["timestamp", "power"]]
   
        os.makedirs(f"{self.root_directory}/processed-results/wattsup/{run_number}/", exist_ok=True)

        result_df.to_csv(f'{self.root_directory}/processed-results/wattsup/{run_number}/{sample_name}.csv')

    def process_runs(self):
        for run_number, samples in self.runs_dict.items():
            root_dir1 = f"{self.root_directory}/wattsup/GL3/{run_number}/"

            for sample in samples:
                file_path = f"{self.root_directory}/wattsup/GL2/{run_number}/{sample}"
                file_path1 = f"{root_dir1}/{sample}"
                self.process(file_path, file_path1, run_number, sample)

    def populate_runs_dict(self):
        runs_dict = {}
        gl2_dir = os.path.join(self.root_directory, 'wattsup', 'GL2')

        directories = [name for name in os.listdir(gl2_dir) if os.path.isdir(os.path.join(gl2_dir, name))]

        for directory in directories:
            directory_path = os.path.join(gl2_dir, directory)
            files = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
            runs_dict[directory] = files

        return runs_dict

