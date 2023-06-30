import os 
import pandas as pd
from wattsup_data_processor import WattsupDataProcessor
from smartwatts_data_processor import SmartwattsDataProcessor

def main():
    # Process Watts Up Pro power measurements
    current_directory = os.path.abspath(os.getcwd())
    parent_directory = os.path.dirname(current_directory)
    root_directory = os.path.join(parent_directory, "raw_data")

    wattsup_data_processor = WattsupDataProcessor(root_directory)
    wattsup_data_processor.process_runs()

    smartwatts_processor = SmartwattsDataProcessor(root_directory)
    smartwatts_processor.process_runs()

    # Align wattsup and smartwatts measurements based on timestamp
    wattsup_dir = f'{root_directory}/processed-results/wattsup/'
    smartwatts_dir = f'{root_directory}/processed-results/smartwatts/'

    # Destination directory for the aligned data
    merged_dir = f'{root_directory}/processed-results/merged-power-measurements/'

    run_numbers = []
    for i in range(0,3):
        if i not in [2,9,13,14,16,20,29,33,46,49,54]:
            run_numbers.append(i)

    workload_levels = ['HIGH', 'MEDIUM', 'LOW']

    for run_number in run_numbers:
        for workload in workload_levels:
            wattsup_subdir = os.path.join(wattsup_dir, f'run_{run_number}/')
            smartwatts_subdir = os.path.join(smartwatts_dir, f'run_{run_number}/')

            wattsup_files = [file for file in os.listdir(wattsup_subdir) if workload in file]
            smartwatts_files = [file for file in os.listdir(smartwatts_subdir) if workload in file]
            for sw_file in smartwatts_files:
                sample_name = sw_file[:-4]  # Remove the '.csv' extension

                watts_file = next((file for file in wattsup_files if sample_name in file), None)

                if watts_file:
                    file_wattsup = os.path.join(wattsup_subdir, watts_file)
                    file_smartwatts = os.path.join(smartwatts_subdir, sw_file)

                    df_wattsup = pd.read_csv(file_wattsup)
                    df_smartwatts = pd.read_csv(file_smartwatts)

                    # Align the data based on timestamp
                    merged_df = pd.merge(df_wattsup, df_smartwatts, on='timestamp', how='inner')
                    merged_df.rename(columns={'power': 'wattsup_power', 'total_power': 'smartwatts_power'}, inplace=True)

                    output_dir = os.path.join(merged_dir, f'run_{run_number}')
                    os.makedirs(output_dir, exist_ok=True)
                    output_file = os.path.join(output_dir, f'{sample_name}.csv')

                    merged_df.to_csv(output_file, index=False)
                    print(f"Merged DataFrame for sample '{sample_name}' has been saved.")


if __name__ == "__main__":
    main()
