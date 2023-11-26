import pandas as pd

import googleapiclient.discovery
import googleapiclient.errors

from keys import *

youtube = googleapiclient.discovery.build(
    API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY
)

class Video:
    def __init__(self, titulo, id, comentarios: pd.DataFrame):
        self.titulo = titulo
        self.id = id
        self.comentarios = comentarios

    def __str__(self) -> str:
        return f'Titulo: {self.titulo}\nid: {self.id}\n comentarios:\n{self.comentarios}'
    
    def create_csv(self, locale='relevance'):
        self.comentarios.to_csv(f'./data/youtube/{locale}/{self.id}.csv')

def search_videos(query, maxResults, sort='relevance'):
    video_list = []

    search_response = youtube.search().list(
    q=query,
    type='video',
    part='id,snippet',
    order=sort,
    maxResults=maxResults
    ).execute()

    for search_result in search_response.get('items', []):
        video_title = search_result['snippet']['title']
        video_id = search_result['id']['videoId']
        video_list.append({video_title:video_id})

    return video_list

def get_video_comments(video_list):
    video_objects = []

    for video in video_list:
        for key in video:
            req = youtube.commentThreads().list(
                part="snippet",
                videoId= video[key],
                maxResults=10
            )

            try:
                res = req.execute()
            except Exception as e:
                print(e)

            comments = []

            for item in res['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append([
                    comment['authorDisplayName'],
                    comment['publishedAt'],
                    comment['updatedAt'],
                    comment['likeCount'],
                    comment['textDisplay'],
                ])

            df = pd.DataFrame(comments, columns=['author', 'published', 'uploaded', 'likes', 'text'])
            df.head(10)
            video = Video(key, video[key], df)
            video_objects.append(video)

    return video_objects

def main():
    video_list = search_videos('unip', 40, 'date')
    results = get_video_comments(video_list)
    for result in results:
        result.create_csv('recent')

    """ video_list = search_videos('unip', 40)
    results = get_video_comments(video_list)
    for result in results:
        result.create_csv() """

if __name__=='__main__':
    main()