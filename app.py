#----- dependencies -----#

import streamlit as st
import joblib
import pandas as pd
import requests
import os


#----- page config -----#

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


#----- paths -----#

parent_directory = os.getcwd()
model_path = os.path.join(parent_directory, "models")


#----- function to fetch movie posters -----#

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"


#----- function to recommend movies -----#

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters


#----- load models -----#

movies_dict = joblib.load(os.path.join(model_path, "movie_dict.pkl"))
movies = pd.DataFrame(movies_dict)
similarity = joblib.load(os.path.join(model_path, "similarity.pkl"))


#----- sidebar -----#

with st.sidebar:
    st.title("🎬 Movie Recommender")
    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("1. Type or select a movie from the dropdown.")
    st.markdown("2. Click **Show Recommendations**.")
    st.markdown("3. Explore your personalised picks!")
    st.markdown("---")
    st.markdown("**About**")
    st.markdown(
        "Content-based filtering using cosine similarity on movie metadata "
        "(genres, cast, crew, keywords)."
    )
    st.markdown("---")
    st.markdown("**Contact**")
    st.markdown("amanbhatt.1997.ab@gmail.com")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/amanbhatt1997/) | [GitHub](https://github.com/amanbhatt97) | [Portfolio](https://amanbhatt97.github.io/portfolio/)")


#----- main content -----#

st.title("🎬 Movie Recommendation System")
st.markdown("Discover movies similar to the ones you love — powered by content-based filtering.")
st.markdown("---")

selected_movie_name = st.selectbox(
    "Search or select a movie:",
    movies["title"].values
)

if st.button("Show Recommendations", type="primary"):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie_name)

    st.markdown(f"#### Movies similar to *{selected_movie_name}*")
    st.markdown("---")

    cols = st.columns(6)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.caption(f"**{names[idx]}**")
