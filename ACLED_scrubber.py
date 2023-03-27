import pandas as pd

# insert raw csv here
df = pd.read_csv("acled_no_protests_no_urban.csv")

# convert to date format
df['Date'] = pd.to_datetime(df['event_date'], errors='coerce')

# group by date, sum
# df_monthly = (df.groupby([pd.Grouper(key='Date', freq='MS')])['count']).sum()

# group by date, number of events
df_monthly = (df.groupby([pd.Grouper(key='Date', freq='MS')])['data_id']).count()

# export to csv
df_monthly.to_csv('acled_monthly_kenya_no_urban_no_protests.csv')