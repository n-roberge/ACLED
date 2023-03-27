import csv
from datetime import datetime
import os

### Convert date to something Arc can read ###
# open the csv file

fn = '2012-2022_acled_kenya'
with open(fn + '.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)

    # create a new csv file for writing the output
    with open(fn + '_scrubbed.csv', 'w', newline='') as output_file:
        fieldnames = ['event_date', 'season'] + reader.fieldnames
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        # iterate through each row in the input file
        for row in reader:

            # check if the row contains a date in the correct format
            if '-' in row['event_date']:
                date_string = row['event_date']
                date_obj = datetime.strptime(date_string, '%d-%b-%y')
                new_date_string = date_obj.strftime('%m/%d/%Y')
                row['event_date'] = new_date_string

            # add season
            if date_obj.month in [1, 2, 6, 7, 8, 9]:
                row['season'] = 'dry'
            else:
                row['season'] = 'rainy'

            # write the updated row to the output file
            writer.writerow(row)