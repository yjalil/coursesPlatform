import requests
import re
import config
from functools import lru_cache
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
oauth2_scheme = HTTPBearer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache
def get_settings():
    return config.Settings()


@app.get('/access_token')
async def get_token(code: str, settings: config.Settings = Depends(get_settings)):
    params = {
        'client_id': settings.github_client_id,
        'client_secret': settings.github_client_secret,
        'code': code
    }

    headers = {
        'Accept': 'application/json'
    }

    response =  requests.post('https://github.com/login/oauth/access_token',params=params, headers=headers).json()
    return response


@app.get('/user')
async def get_user(token: str = Depends(oauth2_scheme)):
    headers = { 'Authorization': f'Bearer {token.credentials}' }
    git_response = requests.get('https://api.github.com/user', headers=headers).json()
    # return response['login']
    url = f"https://kitt.lewagon.com/alumni/{git_response['login']}"
    kitt_response = requests.get(url)

    name_pattern = re.compile(r'content="([^"]+) attended')
    batch_pattern = re.compile(r'Batch #(\d+)')
    dates_pattern = re.compile(r'from ([^"]*) to ([^"]*) in')

    name_match = name_pattern.search(kitt_response.text)
    if name_match:
        name = name_match.group(1)
        batch_match = batch_pattern.search(kitt_response.text)
        dates_match = dates_pattern.search(kitt_response.text)
        image_pattern = re.compile(f'<img[^>]*alt="{re.escape(name)}"[^>]*src="([^"]+)"')
        profile_picture_match = image_pattern.search(kitt_response.text)

        if batch_match and dates_match and profile_picture_match:
            batch = batch_match.group(1)
            from_date, to_date = dates_match.groups()
            profile_picture = profile_picture_match.group(1)
        else:
            return {
                'error': 'Could not find batch or dates'
            }
    else:
        return {
            'error': 'Could not find Alumni'
        }

    return {
        'name': name,
        'batch': batch,
        'from_date': from_date,
        'to_date': to_date,
        'profile_picture': profile_picture
    }
