import pandas as pd
import streamlit as st
import pickle
import requests


# Fetch poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    # Get similarity scores for the selected movie
    distance = similarity[movie_index]

    # Sort movies based on similarity scores
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])

    # Retrieve the top recommended movies (excluding the selected movie itself)
    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list[1:6]:  # Skip the first item as it's the movie itself
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movie_posters


# Load the movie dictionary and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Title for the app
st.title("Movie Recommender System")

# Selectbox for movies
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

# Recommendation button
if st.button('Show Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Display the recommended movies and posters in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
