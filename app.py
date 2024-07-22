import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import preprocessor,helper
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preproccess(df,region_df)
st.sidebar.header("Olympics Analysis")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/en/b/b1/Olympic_Rings.svg')

user_menu  = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athelete-Wise Analysis')
)


if user_menu == 'Medal Tally':
    
    years,country = helper.country_year_list(df)

    Selected_year = st.sidebar.selectbox("Select Year", years)
    Selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,Selected_year,Selected_country)
    if (Selected_year == 'Overall') & (Selected_country == 'Overall'):
        st.title('Overall Medal Tally')
    if (Selected_year != 'Overall') & (Selected_country == 'Overall'):
        st.title('Medal Tally in ' + str(Selected_year) + ' Olympics')
    if (Selected_year == 'Overall') & (Selected_country != 'Overall'):
        st.title('Overall Medal Tally ' + Selected_country)
    if (Selected_year != 'Overall') & (Selected_country != 'Overall'):
        st.title(Selected_country + ' Perfomance in ' + str(Selected_year)+ ' Olympics')

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.header("Top Statisctics", divider= 'rainbow')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.title(editions)
    with col2:
        st.subheader("Hosts")
        st.title(cities)
    with col3:
        st.subheader("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Nations")
        st.title(nations)
    with col3:
        st.subheader("Athletes")
        st.title(athletes)
    
    st.header("Particiating Nation Over the Years", divider = 'green')
    nations_over_time = helper.data_overtime(df, 'region')
    fig = px.line(nations_over_time, x = 'Edition', y= 'region')
    st.plotly_chart(fig)

    st.header("Events Over the Years", divider = 'red')
    events_over_time = helper.data_overtime(df, 'Event')
    fig = px.line(events_over_time, x = 'Edition', y= 'Event')
    st.plotly_chart(fig)

    st.header("Athletes Over the Years", divider = 'blue')
    athletes_over_time = helper.data_overtime(df, 'Name')
    fig = px.line(athletes_over_time, x = 'Edition', y= 'Name')
    st.plotly_chart(fig)

    st.header('No of Events over time (Each sport)',divider='orange')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values = 'Event', aggfunc='count').fillna(0).astype('int'), annot= True)
    st.pyplot(fig)

    st.title('Most Succesful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    Selected_Sport =  st.selectbox('Select Sport', sport_list)
    x = helper.most_succesful(df,Selected_Sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':
    
    country_list = df['region'].astype('str').dropna().unique().tolist()
    country_list.sort()
    #country_list.insert(0,'Overall')
    Selected_country  = st.sidebar.selectbox('Select country', country_list)
    st.header(Selected_country + " Medal Tally Over the years", divider='rainbow')

    country_df = helper.yearwise_medaltally(df,Selected_country)
    fig = px.line(country_df, x = 'Year', y= 'Medal')
    st.plotly_chart(fig)
    #Selected_Country = st.selectbox('Select Country',country)

    st.header(Selected_country + " Excels in following Sports", divider='rainbow')
    fig,x = plt.subplots(figsize=(20,20))
    x = helper.countryEvent_heatmap(df,Selected_country)
    sns.heatmap(x,annot= True)
    st.pyplot(fig)

    st.header('Top 10 Athletes of '+ Selected_country, divider='rainbow')
    top_df = helper.coutrywise_TopAtheletes(df,Selected_country)
    st.table(top_df)

if user_menu == 'Athelete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    st.header('Distribution of Age',divider='rainbow')
    
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age', 'Gold Medalist', 'Silver Medalist','Bronze Medalist'],show_hist = False,show_rug = False)
    fig.update_layout(autosize=False,width=1000, height=500)
    st.plotly_chart(fig)

    x =[]
    name=[]
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    for sport in famous_sports:
        temp_df= athlete_df[athlete_df['Sport']== sport]
        x.append(temp_df[temp_df['Medal']== 'Gold']['Age'].dropna())
        name.append(sport)
    
    st.header('Distribution of Age wrt Sport (Gold Medalist)', divider='rainbow')
    fig = ff.create_distplot(x,name,show_hist = False,show_rug = False)
    fig.update_layout(autosize=False,width=1000, height=500)
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.header('Distribution of Weight vs Height',divider='rainbow')
    Selected_Sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, Selected_Sport)
    
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df, x='Weight',y='Height',hue ='Medal', size='Sex')
    st.pyplot(fig)

    st.header('Distribution of Age Men vs Women',divider='rainbow')
    final = helper.men_v_women(df)
    fig=px.line(final, x='Year', y=['Male','Female'])
    st.plotly_chart(fig)