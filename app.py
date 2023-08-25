#----- dependencies -----#

# for frontend operations
import streamlit as st  

# for loading model files
import joblib   

# data processing, CSV file I/O
import pandas as pd

# for requesting posters from API
import requests 

# to work with operating system-related functionality
import os



#----- paths -----#

# Get the parent directory
parent_directory = os.getcwd()

# model path
model_path = os.path.join(parent_directory, 'models') 



#----- function to fetch movie posters -----#

def fetch_poster(movie_id):

    # from API of tmdb, url for poster based on movie titles
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)

    # HTTP GET request 
    response = requests.get(url)

    # converting into json
    data = response.json() 

    # full path of posters
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path'] 

    return full_path



#----- function to recommend movies -----#

def recommend(movie):

    # finding index of selected movie
    movie_index = movies[movies['title'] == movie].index[0] 

    # finding distances using similarity
    distances = similarity[movie_index] 

    #fetch top movies based on distances
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:7] 

    #to append recommended movie names
    recommended_movies = [] 

    #to append recommended movie posters
    recommended_movie_posters = [] 

    for i in movies_list:
        # since enumerate() will give tuple(movie_id, similarity), we will fetch only movie_id that;s why i[0] is used
        movie_id = movies.iloc[i[0]].movie_id 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters



#----- load models -----#

# load the created dataframe new_df and open it in 'read binary' mode
movies_dict = joblib.load(os.path.join(model_path, 'movie_dict.pkl'))

# create dataframe from movies_dict
movies = pd.DataFrame(movies_dict)

# load similarity dataframe that contains distance matrix for every movie
similarity = joblib.load(os.path.join(model_path, 'similarity.pkl'))



#----- front_end operations -----#

# title for server 
st.title("Movie Recommender System")

# selectbox to type or select movie
selected_movie_name = st.selectbox(
'Type or select a movie from dropdown',
movies['title'].values)


# show recommendations button 
if st.button('Show Recommendations'):

    names, posters = recommend(selected_movie_name)

    # layout of results 
    col1, col2, col3 = st.columns(3)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    # layout of results 
    col4, col5, col6 = st.columns(3)

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

    with col6:
        st.text(names[5])
        st.image(posters[5])
