import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Ruta a tu archivo client_secret.json
CLIENT_SECRETS_FILE = "client.json"

# Alcances que pedimos
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Autenticación
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8080)

    # Construcción del cliente de la API
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # ID de la playlist de videos que te gustaron (fijo)
    liked_playlist_id = "LL"

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=25,
        playlistId=liked_playlist_id
    )
    response = request.execute()

    # Mostrar resultados
    for item in response.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["snippet"]["resourceId"]["videoId"]
        print(f"{title}: https://www.youtube.com/watch?v={video_id}")

if __name__ == "__main__":
    main()
