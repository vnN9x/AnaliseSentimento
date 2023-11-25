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
    
    def create_csv(self):
        self.comentarios.to_csv(f'{self.titulo}.csv')

def search_videos(busca):
    video_list = []

    search_response = youtube.search().list(
    q=busca,
    type='video',
    part='id,snippet',
    order='relevance',
    maxResults=20
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
                maxResults=100
            )

            res = req.execute()

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
    video_list = search_videos('aprender programação')
    print(get_video_comments(video_list))

if __name__=='__main__':
    main()