import pandas as pd

def concatenate_csv_files(file_paths, output_path):
    """
    Reads multiple CSV files, concatenates them into one DataFrame,
    and writes the result to a new CSV file.

    Parameters:
    file_paths (list of str): List of file paths to the CSV files to be concatenated.
    output_path (str): The file path where the concatenated CSV will be saved.

    Returns:
    None
    """
    # Read and concatenate CSV files
    dataframes = [pd.read_csv(file_path) for file_path in file_paths]
    concatenated_df = pd.concat(dataframes, ignore_index=True)

    # Write the concatenated dataframe to a new CSV file
    concatenated_df.to_csv(output_path, index=False)

# Define file paths
file_paths = [
    '..//..//..//Output/Ver_2/No_Wind/A321/A321-231/Emissions_Summary_PF_0.1.csv',
    '..//..//..//Output/Ver_2/No_Wind/A321/A321-231/Emissions_Summary_PF_0.3.csv',
    '..//..//..//Output/Ver_2/No_Wind/A321/A321-231/Emissions_Summary_PF_0.5.csv',
    '..//..//..//Output/Ver_2/No_Wind/A321/A321-231/Emissions_Summary_PF_0.7.csv'
]

# Define output path
output_path = 'data/A321_231_Emissions_Summary_Combined.csv'

# Call the function
concatenate_csv_files(file_paths, output_path)
