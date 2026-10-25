# 🎬 CineMatch — Movie Recommendation System

Discover your next favourite movie with **CineMatch**, a movie recommendation web app that suggests five similar movies based on a title you select.

## 🚀 Live Demo

**Try the application:** [CineMatch — Movie Recommendation System](https://movie-recommendation-system-m0fm.onrender.com/)

> The app is hosted on Render. If it has been inactive, the first visit may take a little time to load.

## ✨ Features

- **Movie selection:** Choose a movie from the available movie collection.
- **Similar-movie recommendations:** Get five recommendations based on the selected movie and the precomputed similarity data.
- **Movie posters:** Fetch poster images using The Movie Database (TMDB) API when available.
- **Clean, responsive interface:** A dark, cinematic Streamlit UI with movie cards.
- **Cached data and poster requests:** Reduce repeated loading and API requests during a session.

## 🧰 Tech Stack

- **Language:** Python
- **Web application:** Streamlit
- **Data handling:** Pandas
- **Recommendation logic:** Precomputed movie-similarity data
- **Movie metadata and posters:** TMDB API
- **Serialized artifacts:** Pickle (`.pkl`)
- **Deployment:** Render

## 📁 Project Structure

```text
Movie-recommendation-System/
├── app.py
├── movies.pkl
├── requirements.txt
├── .gitignore
└── similarity.pkl   # Downloaded at runtime if not already present
```

`similarity.pkl` is downloaded by the application from Google Drive when it is not present locally. The Google Drive file must be accessible to the application.

## ⚙️ Run Locally

### 1. Prerequisites

- Python 3.10 or a compatible version supported by the dependencies
- Git
- Access to the required `.pkl` artifacts
- A TMDB API key if you want the app to fetch movie posters

### 2. Clone the repository

```bash
git clone https://github.com/HarshGupta4511/Movie-recommendation-System.git
cd Movie-recommendation-System
```

### 3. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure the TMDB API key

The application uses the TMDB API to retrieve movie posters. Configure your key using Streamlit secrets or an environment variable, and read it from that secure configuration in `app.py`.

For Streamlit secrets, create `.streamlit/secrets.toml` locally:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

Make sure `.streamlit/secrets.toml` is excluded from Git and **never commit your real API key**. If you deploy on Streamlit Community Cloud, add the secret through the app's settings. For Render, configure the key as an environment variable or use the secrets mechanism supported by your deployment setup, and update `app.py` to read it appropriately.

### 6. Start the application

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 🧠 How It Works

1. The app loads the movie metadata from `movies.pkl`.
2. If `similarity.pkl` is not present, the app attempts to download it from its configured Google Drive file.
3. You select a movie title from the list.
4. The app finds the selected movie's row in the similarity data and ranks other movies by their similarity scores.
5. The five highest-ranked matching movies are displayed with poster images when available.

The recommendations depend on the movie collection and precomputed similarity artifact. The application does not train a new recommendation model each time it runs.

## 🔑 Configuration and Troubleshooting

- **Similarity file download fails:** Check that the Google Drive file is shared so the app can access it, and confirm that the configured file ID is correct.
- **`movies.pkl` cannot be loaded:** Confirm that `movies.pkl` is present in the project directory and is a trusted artifact.
- **Posters do not appear:** Check the TMDB API key, network access, and whether TMDB has a poster for that movie.
- **App is slow on first visit:** A hosted free service may need to wake up after inactivity, and the similarity artifact may need to download.
- **Dependency or pickle errors:** Install the project's listed dependencies and use compatible Python and library versions for the saved artifacts.

## 🔐 Security Note

Pickle files should only be loaded when they come from a trusted source. Keep API keys out of source code and public repositories; use secrets or environment variables instead.

## 🙌 Acknowledgements

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for movie metadata and poster information.
- Python and the open-source libraries used to build the application.

## 📌 Disclaimer

Movie recommendations are generated from precomputed similarity data and are intended for discovery and entertainment. Recommendations may not reflect every user's preferences.
