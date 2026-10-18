
import streamlit as st
import pickle
import requests
import os
import gdown

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- TMDB CONFIG ----------------
try:
    TMDB_API_KEY = st.secrets["99acca2faf1d0533b474c893b35b6b59"]
except Exception:
    TMDB_API_KEY = "99acca2faf1d0533b474c893b35b6b59"
# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #101019 0%, #171326 50%, #101019 100%);
    color: #F5F3FF;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

.hero {
    padding: 38px 35px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    background: linear-gradient(120deg, #251B3D, #171725 70%);
    margin-bottom: 28px;
}

.eyebrow {
    color: #C4B5FD;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero h1 {
    color: #FFFFFF;
    font-size: clamp(36px, 5vw, 58px);
    font-weight: 800;
    line-height: 1.1;
    margin: 15px 0;
}

.hero p {
    color: #C4BED5;
    font-size: 16px;
    line-height: 1.8;
    max-width: 650px;
}

.section-title {
    font-size: 25px;
    font-weight: 800;
    color: #FFFFFF;
    margin-top: 20px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #A7A1B8;
    font-size: 14px;
    margin-bottom: 22px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 12px;
}

.stSelectbox label {
    color: #DDD6FE !important;
    font-weight: 600 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #211D30;
    border-color: #49405F;
    border-radius: 12px;
    color: white;
}

.stButton > button {
    background: linear-gradient(90deg, #8B5CF6, #6D4AFF);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #A78BFA, #8B5CF6);
    border: none;
    color: white;
    transform: translateY(-2px);
}

.movie-title {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 700;
    line-height: 1.5;
    min-height: 46px;
    margin-top: 12px;
}

.movie-number {
    color: #C4B5FD;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 8px;
}

.footer {
    text-align: center;
    color: #827B96;
    font-size: 12px;
    padding-top: 35px;
}

div[data-testid="stImage"] img {
    border-radius: 12px;
}

@media (max-width: 768px) {
    .hero {
        padding: 25px 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------
@st.cache_resource
def load_data():
    similarity_path = "similarity.pkl"
    file_id = "1gVk6KPg5q0WhYFzmm_xmu-nWpozicxbh"

    # Download only when the file is not already present
    if not os.path.exists(similarity_path):
        with st.spinner("Downloading recommendation data..."):
            downloaded_file = gdown.download(
                id=file_id,
                output=similarity_path,
                quiet=False,
                fuzzy=False
            )

        if not downloaded_file or not os.path.exists(similarity_path):
            raise RuntimeError(
                "Could not download similarity.pkl. "
                "Check that Google Drive sharing is set to "
                "'Anyone with the link'."
            )

    with open("movies.pkl", "rb") as file:
        movie_data = pickle.load(file)

    with open(similarity_path, "rb") as file:
        similarity_data = pickle.load(file)

    return movie_data, similarity_data


movies_list, similarity = load_data()



# ---------------- FETCH POSTER ----------------
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_poster(movie_id):
    if not TMDB_API_KEY or TMDB_API_KEY == "YOUR_TMDB_API_KEY":
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(
            url,
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            },
            timeout=12
        )
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except requests.exceptions.RequestException:
        return None

    return None


# ---------------- RECOMMEND MOVIES ----------------
def recommend(movie):
    matches = movies_list.index[
        movies_list["title"] == movie
    ]

    if len(matches) == 0:
        return []

    movie_index = matches[0]
    distances = similarity[movie_index]

    movie_indices = sorted(
        enumerate(distances),
        key=lambda item: item[1],
        reverse=True
    )[1:6]

    recommendations = []

    for index, score in movie_indices:
        movie_row = movies_list.iloc[index]

        recommendations.append({
            "title": movie_row["title"],
            "movie_id": movie_row["movie_id"],
            "score": float(score)
        })

    return recommendations


# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">🎬 YOUR PERSONAL MOVIE GUIDE</div>
    <h1>Find your next<br>favourite movie.</h1>
    <p>
        One movie is all it takes. Discover five recommendations
        picked by our similarity-based recommendation engine.
        Sit back, explore, and find something worth watching.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- SEARCH SECTION ----------------
st.markdown(
    '<div class="section-title">Discover Movies</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="section-subtitle">'
    'Choose a movie you already love to discover similar titles.'
    '</div>',
    unsafe_allow_html=True
)

left, middle, right = st.columns([5, 1, 2])

with left:
    selected_movie_name = st.selectbox(
        "Choose your movie",
        movies_list["title"].dropna().sort_values().unique(),
        label_visibility="visible"
    )

with right:
    st.write("")
    st.write("")
    find_movies = st.button(
        "✨ Find My Movies",
        use_container_width=True
    )


# ---------------- RESULTS SECTION ----------------
if find_movies:
    recommendations = recommend(selected_movie_name)

    if not recommendations:
        st.warning("No recommendations found for this movie.")

    else:
        st.markdown(
            '<div class="section-title">Made for your taste ✨</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-subtitle">'
            'Here are five movies similar to your selection.'
            '</div>',
            unsafe_allow_html=True
        )

        with st.spinner("Finding your next favourite movies..."):
            columns = st.columns(5)

            for number, (col, movie) in enumerate(
                zip(columns, recommendations), start=1
            ):
                with col:
                    poster = fetch_poster(movie["movie_id"])

                    with st.container(border=True):
                        st.markdown(
                            f'<div class="movie-number">'
                            f'PICK {number:02d}</div>',
                            unsafe_allow_html=True
                        )

                        if poster:
                            st.image(
                                poster,
                                width="stretch"
                            )
                        else:
                            st.markdown(
                                "🎞️",
                                unsafe_allow_html=True
                            )
                            st.caption("Poster unavailable")

                        st.markdown(
                            f'<div class="movie-title">'
                            f'{movie["title"]}</div>',
                            unsafe_allow_html=True
                        )


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    CINEMATCH · YOUR NEXT MOVIE IS WAITING
</div>
""", unsafe_allow_html=True)


