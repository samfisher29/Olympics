import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Total'] = medal_tally['Total'].astype('int')
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')

    return medal_tally


def country_year_list(df):
    years =  df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country =  np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country =='Overall':
        temp_df = medal_df
    if year == 'Overall' and country !='Overall':
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    if year != 'Overall' and country =='Overall':
        temp_df = medal_df[medal_df["Year"] == int(year)]
    if year != 'Overall' and country !='Overall':
        temp_df = medal_df[(medal_df["Year"] == int(year)) & (medal_df["region"] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:        
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Total'] = x['Total'].astype('int')
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    
    return x

def data_overtime(df,col):
    Nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    Nations_over_time.rename(columns={'Year': 'Edition', 'count': col }, inplace = True)
    return Nations_over_time

def most_succesful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on ='Name', right_on='Name', how = 'left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace= True)
    return x

def yearwise_medaltally(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    final = new_df.groupby('Year').count()['Medal'].reset_index()
    return final

def countryEvent_heatmap(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc = 'count').fillna(0)
    return pt

def coutrywise_TopAtheletes(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on ='Name', right_on='Name', how = 'left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace= True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport']== sport]
        return temp_df
    else:
        return athlete_df

def men_v_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on= 'Year')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace = True)
    final.fillna(0, inplace=True)

    return final

