import argparse
import os
import pandas as pd


def split_file(file_path, max_lines):
    # get the name and the extension of the input file
    file_name, file_extension = os.path.splitext(file_path)
    if file_extension == ".xlsx":
        # read the Excel file and get the first sheet
        df = pd.read_excel(file_path, sheet_name=0)
    elif file_extension == ".csv":
        # read the CSV file
        df = pd.read_csv(file_path)
    else:
        print("Invalid file format. Only XLSX and CSV files are supported.")
        return
    # extract the header row
    header = df[:1]
    # extract the data rows
    data_rows = df[1:]
    chunk_number = 0
    start_row_index = 0
    while start_row_index < len(data_rows):
        # get the end row index of the chunk
        end_row_index = min(start_row_index + max_lines, len(data_rows))
        # create a new chunk DataFrame
        chunk_df = pd.concat(
            [header, data_rows[start_row_index:end_row_index]])
        # save the chunk DataFrame to a new file
        chunk_df.to_csv(
            f"{file_name}_{chunk_number}.csv", index=False)
        # increment the chunk number and start row index
        chunk_number += 1
        start_row_index = end_row_index


# parse command line arguments
parser = argparse.ArgumentParser(
    description='Split a CSV or XLSX file into multiple smaller files.')
parser.add_argument('file_path', help='Path to the input file')
parser.add_argument('max_lines', type=int,
                    help='Maximum number of rows per output file', default=10000)

args = parser.parse_args()

# call the split_file function with the command line argument values
split_file(args.file_path, args.max_lines)
