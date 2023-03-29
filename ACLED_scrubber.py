import pandas as pd

# insert raw csv here 
fn = "2012-2022_acled_kenya_scrubbed"
df = pd.read_csv(fn + ".csv")

writer = pd.ExcelWriter(fn + '_monthly_count.xlsx', engine='xlsxwriter')

# convert to date format
df['Date'] = pd.to_datetime(df['event_date'], errors='coerce')

# group by date, sum
# df_monthly = (df.groupby([pd.Grouper(key='Date', freq='MS')])['count']).sum()

# group by date, number of events
#df_monthly = (df.groupby([pd.Grouper(key='Date', freq='MS')])['event_id_cnty']).count()
df_monthly = df.groupby(df['Date'].dt.strftime('%Y-%m'))['event_id_cnty'].count().reset_index(name='count')

# group by season
df['year'] = pd.DatetimeIndex(df['event_date']).year

df_season = df.groupby(['year', 'season']).size().reset_index(name='count')

df_season.to_excel(writer, sheet_name='season count', index=False)

#print sum of seasons
# pivot the DataFrame so that the 'Dry' and 'Rainy' seasons are in separate columns
df_pivot = df_season.pivot_table(index='year', columns='season', values='count', fill_value=0)

# sum the counts for the 'Dry' and 'Rainy' seasons separately
dry_sum = df_pivot['dry'].sum()
rainy_sum = df_pivot['rainy'].sum()

# print the sums
print('Dry season count:', dry_sum)
print('Rainy season count:', rainy_sum)

# export to xlsx
df_monthly.to_excel(writer, sheet_name='monthly count', index=False)

writer.save()