import pickle
import pandas as pd
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    print(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

# Load movie data from pickled dictionary file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity2.pkl','rb'))

# Set up Streamlit title
st.title('Movie Recommender System')

# Create dropdown menu for movie selection
selected_movie = st.selectbox('Select a movie:', movies['title'].values)


# Custom CSS styles
custom_css = """
    <style>
        body {
            background-color: #FFB6C1; /* black background color */
        }
        .stButton>button {
            background-color: black; /* Black background color inside the button */
            color: white; /* White text color for the button */
        }
    </style>
"""

# Apply custom CSS styles
st.markdown(custom_css, unsafe_allow_html=True)


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
