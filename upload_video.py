from multiprocessing import AuthenticationError
import os
from oauth2client.file import Storage
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from time import process_time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import time
import sys
import KeepNotes as keep


from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def authentication():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_1.json"
    CREDENTIALS = 'credentials.json'

    credentials = None
    if os.path.exists('credentials.json'):
        credentials = Credentials.from_authorized_user_file('credentials.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials.json', 'w') as token:
            token.write(credentials.to_json())

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    return youtube

def upload_video(youtube, title):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    print("Uploading video...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title
            },
            "status": {
                "madeForKids": True
            }
        },

        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(title, chunksize=4 * 1024 * 1024, resumable=True, mimetype=None)
    )
    response = request.execute()

    print("Video uploaded successfully.")
    print(response)
    delete_file(title)

def download_video_series(download_url):

    movie_title = download_url.split("/")[-1]

    with open(movie_title, "wb") as f:
        # print("Downloading %s" % file_name)
        start = process_time()
        response = requests.get(download_url, stream=True)
        total_length = response.headers.get('content-length')
        total_size = int(total_length) / (1024 * 1024)

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                f.flush()
                done = int(100 * dl / total_length)
                current_size = dl / (1024 * 1024)

                sys.stdout.write("\r[%s%s] %s%s   %s/%s mb    %s mbps" % (
                '#' * done, ' ' * (100 - done), done, "%", round(current_size, 2), round(total_size, 2),
                (process_time() - start)))
                sys.stdout.flush()

            print("Video downloaded")

def delete_file(title):
    os.remove(title)

def download_torrent(file_name):
    qb = Client("http://127.0.0.1:8080/")

    qb.login("admin", "Ritik@4")
    # open the torrent file of the file you wanna download
    torrent_file = open(file_name, "rb")
    qb.download_from_file(torrent_file)

def get_video_name():
    for x in os.listdir():
        if x.endswith(".mp4"):
            print(x)
            return x


if __name__ == "__main__":
    movie_link_note_id = '1YMbT7XbFgq8Vq_GbMD3Dhfj2fNf-jJC_TRcdUt9bfVJFkuWzNUDIUn9pUoIP9g'
    error_log_id = '1NO5GQfgTDr5k3xd4GKUsQaS1GDXumEiCXRkDH-UZGNVflYEtDEAfsi0iOu7Z-sQ'

    youtube = authentication()
    # download_url_list = input("Enter all link of movie with ',' splited form :- ")

    while True:
        try:
            note = keep.get_note(movie_link_note_id)
            if(len(note.text) > 0 ): 
                error = []
                movie_links = note.text.split(",")
                for link in movie_links:
                    try:
                        title = link.split("/")[-1]
                        download_video_series(link)
                        time.sleep(1)
                        upload_video(youtube, title)
                    except Exception as err:
                        error.append(err)

                error_log = keep.edit_note(error_log_id, error)
                keep.clear_note(movie_link_note_id)
            else:
                print("Add some link in notes")
                time.sleep(10)
        except Exception as e:
            print(e)
            keep.clear_note(movie_link_note_id)
            error_log = keep.edit_note(error_log_id, e)
            time.sleep(10)




    # videoName = get_video_name()
    # download_video_series(download_url)
    # upload_video(movie_title)
    # i = 0
    # while(i<3):
    #     upload_video(youtube, f"Testing {i}")
    #     i += 1
    # download_torrent("black-widow-2021-720p.torrent")



# download_url = 'https://my.kirtijpl5.workers.dev/0:/web/The.Silent.Sea/s1/1080p/The.Silent.Sea.S01E01.Balhae.Lunar.Research.Station.1080p.NF.WEB-DL.DDP5.1.Atmos.x264.mkv'
# movie_title = "Testing"
