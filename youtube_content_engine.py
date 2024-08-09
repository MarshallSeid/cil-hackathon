from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import datetime
import streamlit as st
import pickle

API_KEY = st.secrets.get('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

# Day Kamala Harris became the Democratic nominee for Vice President
# @st.cache_data
def search_videos(query, language, max_results=6, published_after=datetime.datetime(2024, 7, 21)):
    try:
        print(query)
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=max_results,
            relevanceLanguage=language,
            order='viewCount',  # This sorts by view count
            publishedAfter=published_after.isoformat() + "Z"
        ).execute()

        videos = []
        for search_result in search_response.get('items', []):
            video = {
                'id': search_result['id']['videoId'],
                'title': search_result['snippet']['title'],
                'description': search_result['snippet']['description'],
                'channel_title': search_result['snippet']['channelTitle'],
                'published_at': search_result['snippet']['publishedAt']
            }
            videos.append(video)

        return videos

    except HttpError as e:
        print(f'An error occurred: {e}')
        return []

# @st.cache_data
def get_video_stats(video_id):
    try:
        stats = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        if 'items' in stats and stats['items']:
            return stats['items'][0]['statistics']
        return None

    except HttpError as e:
        print(f'An error occurred: {e}')
        return None

# @st.cache_data
def fetch_high_polarity_video(query_strings = ['कमला हैरिस को राष्ट्रपति नहीं बनना चाहिए' ], language='hi', use_pickle=True):

    # Check if pickled results exist and are less than 24 hours old
    if use_pickle is True:
        pickle_file = 'video_results.pickle'
        if os.path.exists(pickle_file):
            file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(pickle_file))
            if datetime.datetime.now() - file_mod_time < datetime.timedelta(hours=24):
                with open(pickle_file, 'rb') as f:
                    return pickle.load(f)

    results = {}
    for query in query_strings:
        print(f"Searching for top trending videos about '{query}' in Hindi...")
        videos = search_videos(query, language)
        results[query] = []
        for i, video in enumerate(videos, 1):
            print(f"\n{i}. {video['title']}")
            print(f"Channel: {video['channel_title']}")
            print(f"Published: {video['published_at']}")
            print(f"Description: {video['description'][:100]}...")  # Truncate long descriptions
            
            stats = get_video_stats(video['id'])
            if stats:
                print(f"Views: {stats.get('viewCount', 'N/A')}")
                print(f"Likes: {stats.get('likeCount', 'N/A')}")
                print(f"Comments: {stats.get('commentCount', 'N/A')}")
            
            print(f"Video URL: https://www.youtube.com/watch?v={video['id']}")
            results[query].append({"video": video, "stats": stats})

    with open(pickle_file, 'wb') as f:
        pickle.dump(results, f)

    return results