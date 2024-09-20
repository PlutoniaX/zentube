import os
from exa_py import Exa
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from generate_transcripts import add_videos_to_playlist

load_dotenv()

# Configure Exa
exa_api_key = os.getenv("EXA_API_KEY")
exa = Exa(api_key=exa_api_key)


def add_videos(prompt="", num_results=10, include = None, exclude = None):
    """
    Searches for videos based on a given prompt and adds them to a playlist.
    
    Args:
        prompt (str): The search query for finding videos. Defaults to an empty string.
        num_results (int): The number of video results to retrieve. Defaults to 10.
        include (list or None): List of keywords to include in the search. Defaults to None.
        exclude (list or None): List of keywords to exclude from the search. Defaults to None.
    
    Returns:
        None: This function doesn't return any value, it performs actions and prints results.
    """
    try:
        print(f"\n🔎 Finding videos with prompt: {prompt}\n")
        results = find_videos(prompt=prompt, num_results=num_results, include=include, exclude=exclude)
        all_video_ids = []
        for i, result in enumerate(results, 1):
            video_id = get_youtube_video_id(result.url)
            print(f"\n🔎 Exa result {i}/{len(results)}: \n{result.title}\nVideo ID: {video_id}\n")
            if video_id:
                all_video_ids.append(video_id)
        
        add_videos_to_playlist(all_video_ids)
    except Exception as e:
        print(f"\n\n❌ Error adding videos: {str(e)}")


def find_videos(prompt="", num_results=10, include= None, exclude= None):
    
    # Modify the prompt if it doesn't contain "videos" or "youtube"
    """
    Searches for YouTube videos based on a given prompt.
    
    Args:
        prompt (str): The search query for finding videos. If it doesn't contain "videos" or "youtube", it will be modified.
        num_results (int): The number of video results to return. Defaults to 10.
        include (str): Optional text to include in the search results.
        exclude (str): Optional text to exclude from the search results.
    
    Returns:
        list: A list of search results containing video information.
    """
    if "videos" not in prompt.lower() and "youtube" not in prompt.lower():
        prompt = f"Find youtube videos for: {prompt}"
    
    print(f"Modified prompt: {prompt}")
    result = exa.search_and_contents(
    prompt,
    type="neural",
    use_autoprompt=True,
    num_results=num_results,
    include_text=[include] if include else None,
    exclude_text=[exclude] if exclude else None,
    )
    
    return result.results


def get_youtube_video_id(url):
    """Extracts the YouTube video ID from a given URL.
    
    Args:
        url (str): The YouTube video URL to parse.
    
    Returns:
        str or None: The extracted video ID if found, or None if not found.
    """
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    return video_id[0] if video_id else None