from typing import Optional
from typing import Any
from pathlib import Path
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
import pandas as pd

from app.schemas import RecipeSearchResults, Recipe, RecipeCreate
from app.recipe_data import RECIPES


BASE_PATH = Path(__file__).resolve().parent

# 1
app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

# 2
api_router = APIRouter()

files = {
    'amazon': 'Data_mdif/amazon_prime_modificado.csv',
    'disney': 'Data_mdif/disney_Plus_modificado.csv',
    'hulu': 'Data_mdif/hulu_modificado.csv',
    'netflix': 'Data_mdif/netflix_modificado.csv',
}
df = pd.concat([pd.read_csv(files[file]) for file in files])

# Updated to serve a Jinja2 template
# https://www.starlette.io/templates/
# https://jinja.palletsprojects.com/en/3.0.x/templates/#synopsis
@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """
    return {"message": "Hello World"}

#Pregunta 1

def count_titles_by_platform_function(keyword, df):
    
    count = df[df["title"].str.contains(keyword)].groupby("platform").size().reset_index(name="count")
    return count.to_dict(orient="records").pop().get("count")


@app.get("/count_titles_by_platform", status_code=200)
def count_titles_by_platform(
    keyword: str,
    df: str,
) -> dict:
    """
    Fetch a single recipe by ID
    """
    path_file = files.get(df)
    if not path_file:
        raise HTTPException(status_code=404, detail="File not found")

    file = pd.read_csv(path_file)
    count = count_titles_by_platform_function(keyword, file)

    return {
        'platform': df,
        'count': count,
    }



#Pregunta 2
def get_score_count_function(platform, score, release_year):
    count = df[(df['score'] > score) & (df['release_year'] == release_year) & (df['platform'] == platform)].shape[0]
    return f'platform: {platform},  cantidad: {count}'

@app.get('/get_score_count')
def get_score_count(
    platform: str,
    score: int,
    release_year: int,
) -> dict:
    count = get_score_count_function(platform, score, release_year)
    return {
        'count': count,
    }


#Pregunta 3
def get_second_highest_score_function(platform):
    df_platform = df[df['platform'] == platform]
    df_platform = df_platform.sort_values(by=['score', 'title'], ascending=[False, True])
    title = df_platform.iloc[1]['title']
    score = int(df_platform.iloc[1]['score'])
    return {'title': title, 'score': score}

@app.get('/get_second_score')
def get_score_count(
    platform: str,
) -> dict:
    title_score = get_second_highest_score_function(platform)
    return {
        'title_score': title_score,
    }

#Pregunta 4
def get_longest_function(platform, duration_type, release_year):
    # filtrar los datos segun la plataforma
    df_platform = df[df['platform'] == platform]
    # filtrar los datos segun el tipo de duracion
    df_platform = df_platform[df_platform['duration_type'] == duration_type]
    # filtrar los datos segun el año de lanzamiento
    df_platform = df_platform[df_platform['release_year'] == release_year]
    # Obtener la pelicula con la duracion maxima
    movie_duration = df_platform.loc[df_platform.duration_int.idxmax()]
    return movie_duration["title"], int((movie_duration['duration_int'])), (movie_duration['duration_type'])

@app.get('/get_longest')
def get_longest(
    platform: str,
    duration_type: str,
    release_year: int
) -> dict:
    title, duration, duration_type = get_longest_function(platform, duration_type, release_year)
    return {
        'title': title,
        'duration': duration,
        'duration_type': duration_type
    }

#Pregunta 5

def get_rating_count_function(rating, df):
    # Contar filas con rating especificado en el dataframe
    count = len(df[df['rating'] == rating])
    return rating, count

@app.get('/get_rating_count')
def get_rating_count(rating: str) -> dict:
    rating, count = get_rating_count_function(rating, df)
    return {
        'rating': rating,
        'count': count
    }


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
