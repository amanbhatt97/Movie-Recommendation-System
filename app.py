#Importing libraries
import streamlit as st #for frontend operations
import pickle #for dumping files from jupyter notebook
import pandas as pd
import requests #for requesting posters from API

#function to fetch movie posters
def fetch_poster(movie_id):
    #from API of tmdb, url for poster based on movie titles
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json() #converting into json
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path'] #full path of posters
    return full_path

#function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0] #finding index of selected movie
    distances = similarity[movie_index] #finding distancies using similarity
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6] #fetch first 5 movies based on distances

    recommended_movies = [] #to append recommended movie names
    recommended_movie_posters = [] #to append recommended movie posters
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id #since enumerate() will give tuple(movie_id, similarity), we will fetch only movie_id that;s why i[0] is used
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

#Load the created dataframe new_df and open it in 'read binary' mode
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
#Create dataframe from movies_dict
movies = pd.DataFrame(movies_dict)

#Load similarity dataframe that contains distance matrix for every movie
similarity = pickle.load(open('similarity.pkl','rb'))

#Front_end operations:
#Creating Title for server (https://docs.streamlit.io/library/api-reference/text/st.title)
st.title("Movie Recommender System")

#Create selectbox to type or select movie (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)
selected_movie_name = st.selectbox(
'Type or select a movie from dropdown',
movies['title'].values)

#Creating button (https://docs.streamlit.io/library/api-reference/widgets/st.button)
if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)
    #Layout of results (https: // docs.streamlit.io / library / api - reference / layout / st.columns)
    col1, col2, col3, col4, col5 = st.columns(5)
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
