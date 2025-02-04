import pandas as pd

def filter_clients_by_ou_code(input_file: str, ou_codes: list, output_file: str) -> None:
    """
    Filters a masterlist of clients based on the provided OU codes, which may be substrings of 
    the 'OU_code' field, and saves the resulting dataframe to an output file.

    :param input_file: Path to the input CSV file containing the masterlist of clients. The file 
                        should be a CSV with a column 'OU_code' that contains the codes as part 
                        of a string.
    :type input_file: str
    :param ou_codes: List of OU codes (substrings) to filter the 'OU_code' column by.
    :type ou_codes: list of str
    :param output_file: Path to the output CSV file where the filtered list will be saved.
    :type output_file: str

    :return: None
    :raises FileNotFoundError: If the input file does not exist.
    :raises ValueError: If the 'OU_code' column is missing in the input file.
    """
    try:
        # Load the input dataframe
        df = pd.read_csv(input_file)
        
        # Check if 'OU_code' column exists
        if 'OU_code' not in df.columns:
            raise ValueError("The input file must contain an 'OU_code' column.")
        
        # Filter the dataframe by checking if any of the OU codes in the list are substrings of the 'OU_code'
        filtered_df = df[df['OU_code'].apply(lambda x: any(ou_code in x for ou_code in ou_codes))]
        
        # Save the filtered dataframe to the output file
        filtered_df.to_csv(output_file, index=False)
    
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except ValueError as e:
        print(e)
