import pandas as pd
import streamlit as st
import pickle
import requests

movies_list= pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)

st.title('Movie Recommender System')
option=st.selectbox(
    'What is your Comfort Movie?',
    movies['title'].values
)
similarity = pickle.load(open('similarity.pkl','rb'))
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?&append_to_response=videos&api_key={paste_your_tmdb_api_key}'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id)) #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movies_posters
if st.button('Recommend'):
    names,posters= recommend(option)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
