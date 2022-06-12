import streamlit as st
import pandas as pd

st.title('Simple Movie Recommendation System')
st.markdown("""
This simple app recommends Filipino movies based on a user's top 3 genre preferences.
""")

topGenre = pd.read_csv(r"C:\Users\Alex\Documents\Programming\Projects\Movie Recommendation System\userpreferences.csv")
# userpref['UserID']= userpref['UserID'].astype(str)
userlist = sorted(topGenre.UserID.unique())
selected_user = st.sidebar.selectbox('Select User', userlist)

nummovies = st.sidebar.slider('Number of Movies to Suggest:', 1,30)
filmovie = pd.read_csv(r"C:\Users\Alex\Documents\Programming\Projects\Movie Recommendation System\finalFilipinoFilms.csv")
st.header(f"Movie Recommendation for User {selected_user}")

def gettopGenre(user):
    #if multiselect option is in the column
    df_selguy = topGenre[(topGenre.UserID == user)] #gets the top 3 genre of user from the preferences csv
    #looking aat the filipino movies df w/o the user ID
    #I WANT TO LOOK AT DATA FROM THE SPECIFIC USER ID BITCH
    thedict = {}
    collateddf = pd.DataFrame()
    all3 = filmovie[(filmovie['genre'].str.contains(*df_selguy['First_Genre']))& (filmovie['genre'].str.contains(*df_selguy['Second_Genre'][:])) & (filmovie['genre'].str.contains(*df_selguy['Third_Genre'][:]))].sort_values('rating', ascending = False)
    # findall12 = filmovie[((filmovie['genre'].str.contains(df_selguy['First_Genre'][:])) & (filmovie['genre'].str.contains(df_selguy['Second_Genre'][:])))]]
    findall12 = filmovie[((filmovie['genre'].str.contains(*df_selguy['First_Genre'][:])) & (filmovie['genre'].str.contains(*df_selguy['Second_Genre'][:])))]
    first12 = findall12[findall12['genre'].str.count(',')==1].sort_values('rating', ascending = False)
    findall13 = filmovie[((filmovie['genre'].str.contains(*df_selguy['First_Genre'])) & (filmovie['genre'].str.contains(*df_selguy['Third_Genre'])))]
    first13 = findall13[findall13['genre'].str.count(',')==1].sort_values('rating', ascending = False)
    findall23 = filmovie[((filmovie['genre'].str.contains(*df_selguy['Second_Genre'])) & (filmovie['genre'].str.contains(*df_selguy['Third_Genre'])))]
    first23 = findall23[findall23['genre'].str.count(',')==1].sort_values('rating', ascending = False)
    findone = filmovie[((filmovie['genre'].str.contains(*df_selguy['First_Genre'])) | (filmovie['genre'].str.contains(*df_selguy['Second_Genre'])) | (filmovie['genre'].str.contains(*df_selguy['Third_Genre'])))]
    findoneonly = findone[findone['genre'].str.count(',')==0].sort_values(['genre','rating'], ascending = False)





    nana = pd.concat([all3,first12,first13, first23, findoneonly])
    biglist = nana.to_dict('list')
    try:
        thedict['title'] = {**thedict['title'], **biglist['title']}
        thedict['yearReleased'] = {**thedict['yearReleased'], **biglist['yearReleased']}
        thedict['runtimeinmins'] = {**thedict['runtimeinmins'], **biglist['runtimeinmins']}
        thedict['genre'] = {**thedict['genre'], **biglist['genre']}
        thedict['rating'] = {**thedict['rating'], **biglist['rating']}

    except:
        thedict['title'] = biglist['title']
        thedict['yearReleased'] = biglist['yearReleased']
        thedict['runtimeinmins'] = biglist['runtimeinmins']
        thedict['genre'] = biglist['genre']
        thedict['rating'] = biglist['rating']
    results = pd.DataFrame.from_dict(thedict)[:nummovies]
    st.dataframe(results)


gettopGenre(selected_user)
# st.dataframe()
