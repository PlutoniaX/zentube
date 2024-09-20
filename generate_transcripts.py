import os
import json
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle
from datetime import datetime, timezone

# Load environment variables from .env file
load_dotenv()
# You'll need to set these environment variables
API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST_ID = os.environ.get('YOUTUBE_PLAYLIST_ID')

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

unprocessed_dir = os.path.join(base_dir, "experiments", "youtube", "transcripts", "unprocessed")

SCOPES = ['https://www.googleapis.com/auth/youtube']

def get_authenticated_service():
    ```
    """Authenticates and builds a YouTube API service object.
    
    This function checks for existing credentials, refreshes them if expired,
    or creates new ones if necessary. It then builds and returns an authenticated
    YouTube API service object.
    
    Args:
        None
    
    Returns:
        googleapiclient.discovery.Resource: An authenticated YouTube API service object.
    """
    ```
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

youtube = get_authenticated_service()

def get_playlist_items(playlist_id):
    """Retrieves all items from a YouTube playlist.
    
    Args:
        playlist_id (str): The ID of the YouTube playlist to fetch items from.
    
    Returns:
        list: A list of dictionaries, where each dictionary contains information about a playlist item, including snippet and content details.
    """
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items.extend(response["items"])
        request = youtube.playlistItems().list_next(request, response)
    return playlist_items

def get_video_details(video_id):
    """Retrieves detailed information about a specific YouTube video.
    
    Args:
        video_id (str): The unique identifier of the YouTube video.
    
    Returns:
        dict: A dictionary containing detailed information about the video, including snippet, content details, and statistics.
    """
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    return response['items'][0]

def get_transcript(video_id):
    """Retrieves and concatenates the transcript of a YouTube video.
    
    Args:
        video_id (str): The unique identifier of the YouTube video.
    
    Returns:
        str or None: A string containing the full transcript of the video if successful, or None if an error occurs.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"\nError fetching transcript for video {video_id}: {str(e)}")
        return None

def remove_from_playlist(playlist_item_id):
    """
    Removes a video from a YouTube playlist.
    
    Args:
        playlist_item_id (str): The unique identifier of the playlist item to be removed.
    
    Returns:
        None: This function doesn't return anything, but prints a success or error message.
    """
    try:
        youtube.playlistItems().delete(id=playlist_item_id).execute()
        print(f"\n❌Removed video {playlist_item_id} from playlist\n\n")
    except Exception as e:
        print(f"\nError removing video {playlist_item_id} from playlist: {str(e)}\n")
        
def get_channel_name(channel_id):
    """Retrieves the name of a YouTube channel given its channel ID.
    
    Args:
        channel_id (str): The unique identifier of the YouTube channel.
    
    Returns:
        str: The title (name) of the YouTube channel.
    """
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0]['snippet']['title']


def get_latest_video_from_channel(channel_id):
    """Retrieves the latest video from a YouTube channel.
    
    Args:
        channel_id (str): The unique identifier of the YouTube channel.
    
    Returns:
        dict or None: A dictionary containing information about the latest video if found, None otherwise.
    """    try:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=1
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            print(f"Latest video found: {video['snippet']['title']}")
            return video
        else:
            print(f"No videos found for channel {channel_id}")
            return None
    except Exception as e:
        print(f"Error fetching latest video from channel {channel_id}: {str(e)}")
        return None

def add_video_to_playlist(video_id, playlist_id):
    """Adds a video to a specified YouTube playlist.
    
    Args:
        """Retrieves the transcript from the latest video of a specified YouTube channel.
        
        Args:
            channel_id (str): The unique identifier of the YouTube channel.
        
        Returns:
            None: This function doesn't return a value, but it processes the latest video's transcript.
        """
        video_id (str): The ID of the video to be added to the playlist.
        playlist_id (str): The ID of the playlist to which the video will be added.
    
    Returns:
        None: This function doesn't return anything, but prints a success message if the video is added successfully or an error message if an exception occurs.
    """
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        print(f"✅ Added video {video_id} to playlist {playlist_id}")
    except Exception as e:
        print(f"Error adding video {video_id} to playlist {playlist_id}: {str(e)}")

def get_transcript_from_latest_video(channel_id):
    latest_video = get_latest_video_from_channel(channel_id)
    if latest_video:
        handle_playlist_item(latest_video, remove=False)
    else:
        """
        Handle a playlist item by processing its video details and transcript, saving the data, and optionally removing it from the playlist.
        
        Args:
            playlist_item (dict): A dictionary containing information about the playlist item.
            remove (bool, optional): Whether to remove the processed item from the playlist. Defaults to True.
        
        Returns:
            None: This function doesn't return anything, but it performs several side effects:
                - Retrieves video details and transcript
                - Saves processed data to a JSON file
                - Prints progress information
                - Optionally removes the item from the playlist
        """
        print("Failed to add latest video to playlist")


def generate_transcripts():
    """
    Generate transcripts for videos in a specified playlist.
    
    This function retrieves playlist items, processes each item to generate transcripts,
    and handles any exceptions that may occur during the process.
    
    Args:
        None
    
    Returns:
        None: This function doesn't return any value but prints status messages to the console.
    """
    try:
        playlist_items = get_playlist_items(PLAYLIST_ID)
        print(f"\nFound {len(playlist_items)} videos in playlist: {PLAYLIST_ID}\n")
        for item in playlist_items:
            handle_playlist_item(item)
            
        print(f"\n\n🏁 All done making transcript json files!\n")
    except Exception as e:
        print(f"Error in generate_transcripts: {str(e)}")


def handle_playlist_item(playlist_item, remove=True):
    try:
        video_id = playlist_item['contentDetails']['videoId']
    except Exception as e:
        print(f"playlist_item is missing contentDetails, using playlist_item['id'] instead: {str(e)}")
        video_id = playlist_item['id']['videoId']
        
    try:
        video_details = get_video_details(video_id)
        transcript = get_transcript(video_id)
        if transcript:
            channel_id = video_details.get('snippet', {}).get('channelId', '')
            channel_name = get_channel_name(channel_id) if channel_id else ''
            title = video_details.get('snippet', {}).get('title', '')
            print(f"\n\n🎥 Processing:\n {title}\n\nChannel: {channel_name}")   
            data = {
                'title': title,
                "channel_name": channel_name,
                'publish_date': video_details['snippet'].get('publishedAt', ''),
                'processed_date': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                'view_count': video_details['statistics'].get('viewCount', '0'),
                'like_count': video_details['statistics'].get('likeCount', '0'),
                'comment_count': video_details['statistics'].get('commentCount', '0'),
                'duration': video_details['contentDetails'].get('duration', ''),
                'video_id': video_id,
                'description': video_details['snippet'].get('description', ''),
                "channel_id": channel_id,
                'thumbnail': video_details['snippet'].get('thumbnails', {}).get('high', {}).get('url', ''),
                'transcript': transcript,
                'video_url': f"https://www.youtube.com/watch?v={video_id}"
            }
            with open(f"{unprocessed_dir}/{video_id}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"\n✅Saved transcript and details for video {video_id}")
            
            if remove:
                remove_from_playlist(playlist_item['id'])
        else:
            print(f"\nSkipping video {video_id} due to missing transcript\n")
    except Exception as e:
        print(f"Error processing video {video_id}: {str(e)}")
        

def add_videos_to_playlist(video_ids):
    """Adds multiple videos to a YouTube playlist.
    
    Args:
        video_ids (list): A list of YouTube video IDs to be added to the playlist.
    
    Returns:
        None: This function doesn't return any value, but prints status messages.
    """
    for video_id in video_ids:
        try:
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": PLAYLIST_ID,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = request.execute()
            print(f"✅ Added video {video_id} to playlist {PLAYLIST_ID}")
        except Exception as e:
            print(f"❌ Error adding video {video_id} to playlist: {str(e)}")