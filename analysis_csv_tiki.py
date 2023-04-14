import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
from datetime import date
from variables_for_tiki_analysis import *

df = pd.read_csv('bills.csv', skiprows=3, sep='\t')
df = df[["Открыт", "Сумма по чеку, руб."]]
df.columns = [date_of_bill, amount]

df[date_of_bill] = pd.to_datetime(df[date_of_bill], format='%d-%m-%Y %H:%M')
df = df[df[date_of_bill].notnull()]
df['day_of_week'] = df[date_of_bill].dt.day_name()

df[time] = df[date_of_bill].dt.strftime('%H')
df[time] = pd.to_numeric(df[time])
df = df[(df[time] >= start_hour) & (df[time] <= end_hour)]

df[amount] = df[amount].astype(str)
df[amount] = df[amount].apply(lambda x: x.replace(',', ''))
df[amount] = pd.to_numeric(df[amount])

df = df.groupby(['day_of_week', time])[amount].sum()
df = df.to_frame().reset_index()

df = df[['day_of_week', time, amount]]
count_of_weeks = abs(date(2022, 12, 1) - date(2023, 3, 23)).days // 7
df[amount] = df[amount].apply(lambda x: x / count_of_weeks)
df.sort_values(by=[time], inplace=True)
df = df.pivot_table(index=time, columns='day_of_week', values=amount, fill_value=0)

df.info()
display(df)

plot = df.plot(title='Plot')

xtick = np.arange(float(start_hour), float(end_hour)+1, 0.5)
ytick = range(0, 56, 2)
plot.set_xticks(xtick)
plot.set_yticks(ytick)
plot.grid('on', which='minor', axis='x')
plot.grid('off', which='major', axis='x')

plot.grid('on', which='minor', axis='y')
plot.grid('off', which='major', axis='y')

plt.show()

