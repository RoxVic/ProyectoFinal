from flask import Flask, redirect, url_for, session, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura

# Configuración de OAuth
CLIENT_SECRETS_FILE = "client_secret.json"  # Descarga este archivo desde Google Cloud Console
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

@app.route('/')
def index():
    return '<a href="/authorize">Autorizar con YouTube</a>'

@app.route('/authorize')
def authorize():
    # Crear flow para manejar el OAuth 2.0
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True))
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True))
    
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    return redirect(url_for('get_channel_info'))

@app.route('/channel')
def get_channel_info():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    credentials = Credentials(
        **session['credentials'])
    
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    
    # Ejemplo: obtener información del canal del usuario autenticado
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()
    
    return jsonify(response)

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Solo para desarrollo local
    app.run(debug=True)