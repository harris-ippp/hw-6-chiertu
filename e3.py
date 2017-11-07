#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import shutil
shutil.copy2('president_general_2016.csv', '2016.csv')
years = [str(each)+".csv" for each in list(range(1924,2017,4))]
dflist = []
for each in years:
    header = pd.read_csv(each, nrows = 1).dropna(axis = 1)
    d = header.iloc[0].to_dict()
    df = pd.read_csv(each, index_col = 0, thousands = ",", skiprows = [1])
    df.rename(inplace = True, columns = d)
    df.dropna(inplace = True, axis = 1)
    df['Year'] = int(each.partition('.')[0])
    df = df[['Democratic', 'Republican', 'Total Votes Cast', 'Year']]
    dflist.append(df)
df = pd.concat(dflist)
df.index = [item.partition('(')[0] for item in list(df.index)]
df = df.reset_index().groupby(['index','Year']).sum().reset_index()
df['Republican Share'] = df['Republican']/df['Total Votes Cast']
counties = ['Accomack County', 'Albemarle County', 'Alexandria City', 'Alleghany County']
for county in counties:
    name = county.lower().replace(" ", "_")
    df_plot = df[df['index'].str.contains(county)][['Year','Republican Share']].groupby('Year').sum()
    df_plot.index= [pd.to_datetime(year, format='%Y').date() for year in df_plot.index.tolist()]
    ax = df_plot.plot( kind = 'line', marker = 'o')
    ax.set_ylim([0,1])
    ax.yaxis.grid()
    ax.xaxis.set_major_locator(mdates.YearLocator(8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.grid(True, which='major')
    ax.xaxis.set_minor_locator(mdates.YearLocator(4))
    ax.xaxis.grid(True, which='minor',linewidth=0.5)
    ax.set(xlabel='Year of Presidential Election',
           ylabel='Republican Vote Share',
           title='Republican Vote Share in ' + county)
    plt.gcf().autofmt_xdate()
    plt.savefig(name+'.pdf')
