from youtube_transcript_api import YouTubeTranscriptApi
from youtube_search import YoutubeSearch
import json

ytt_api = YouTubeTranscriptApi()

def get_youtube_transcript(video_id: str):
    """
    Get the transcript of a YouTube video.

    Args:
        video_id: The ID of the video to get the transcript for.

    Returns:
        The transcript of the video, or None if no transcript is found.
    """
    try :
        script = ytt_api.fetch(video_id)
    except Exception as e:
        try: 
            script = ytt_api.fetch(video_id, languages=['fr'])
        except Exception as e:
            print("No transcript found, error: ", e)
            return None

    if script:
        script = " ".join([line.text for line in script])

    return script

def search_youtube(query: str):
    """
    Search YouTube for a query.

    Args:
        query: The query to search for.

    Returns:
        A list of search results.
    """
    results = YoutubeSearch(query, max_results=10).to_json()
    results_dict = json.loads(results)

    for video in results_dict['videos']:
        if "thumbnails" in video:
            del video["thumbnails"]
    
    return results_dict

