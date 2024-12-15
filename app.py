import pickle
import pandas as pd
import streamlit as st
import requests
import openai



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=be9a4568a4d3269c96bf596d3c31ab65&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def get_movie_description_from_chatgpt(movie):
    openai.api_key = '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'
    messages = [{"role": "system", "content":
                 "You are a intelligent assistant."}]
    if movie:
        messages.append(
            {
                "role": "user",
                "content": "Give a catchy description of %s in 40 words" % (movie)
            },
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
    return reply


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')
# movies = pickle.load(open('model/movie_list.pkl','rb'))
# similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        expander = st.expander("Why you should watch?", expanded=True)
        expander.write(get_movie_description_from_chatgpt(
            recommended_movie_names[0]))

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        expander = st.expander("Why you should watch?", expanded=True)
        expander.write(get_movie_description_from_chatgpt(
            recommended_movie_names[1]))
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        expander = st.expander("Why you should watch?", expanded=True)
        expander.write(get_movie_description_from_chatgpt(
            recommended_movie_names[2]))

    col4, col5 = st.columns(2)

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        expander = st.expander("Why you should watch?", expanded=True)
        expander.write("""
            It is a captivating action-packed movie that offers a unique blend of sci-fi, romance, and adventure. 
            It has great special effects, an engaging plot, and memorable characters that will leave you wanting more.
        """)

    col15 = st.columns(1)

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        expander = st.expander("Why you should watch?", expanded=True)
        expander.write("""
            It is a hilarious and entertaining animated adventure featuring the beloved feline hero from the Shrek franchise. It has fantastic animation, a fun story, and great voice acting.
        """)




