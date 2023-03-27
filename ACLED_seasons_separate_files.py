import csv
from datetime import datetime
import os

# open the csv file

fn = '2012-2022_acled_kenya'

with open(fn + '.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)

    # create a directory for writing the output files
    output_dir = fn
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # create a dictionary of output files, with one file per year
    output_files = {}
    for row in reader:
        if '-' in row['event_date']:
            date_string = row['event_date']
            date_obj = datetime.strptime(date_string, '%d-%b-%y')
            year = date_obj.year
            if year not in output_files:
                output_file_path = os.path.join(output_dir, f'{year}.csv')
                output_file = open(output_file_path, 'w', newline='')
                fieldnames = ['event_date', 'season'] + [col for col in reader.fieldnames if col != 'event_date']
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                output_files[year] = {'file': output_file, 'writer': writer}
            writer = output_files[year]['writer']
            row['event_date'] = date_obj.strftime('%m/%d/%Y')
            if date_obj.month in [1, 2, 6, 7, 8, 9]:
                row['season'] = 'dry'
            else:
                row['season'] = 'rainy'
            writer.writerow({k: v for k, v in row.items() if k in fieldnames})

    # close all output files
    for year in output_files:
        output_files[year]['file'].close()