import pickle

import pandas as pd
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={your api key}&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append({
            'title': movies.iloc[i[0]]['title'],
            'poster': fetch_poster(movie_id)
        })
    return recommended_movies

# Custom CSS styles
custom_styles = """
<style>
.movie-container {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    margin: 10px;
}

.poster-image {
    width: 200px;
    height: auto;
    border-radius: 5px;
}

.movie-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}

.movie-overview {
    font-size: 16px;
    margin-bottom: 10px;
}
</style>
"""

st.header('Movie Recommender System')
st.markdown(custom_styles, unsafe_allow_html=True)  # Inject custom CSS styles

movies_dict= pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Recommend"):
    recommended_movies = recommend(selected_movie)
    for movie in recommended_movies:
        st.markdown(
            f"<div class='movie-container'>"
            f"<div class='movie-title'>{movie['title']}</div>"
            f"<img class='poster-image' src='{movie['poster']}' alt='{movie['title']}'/>"
            "</div>",
            unsafe_allow_html=True
        )
