'''Initialize a process that wait a new video in order to procees it'''

import os
import socket
import sys
import glob
from api_aws import usage_demo
import pymysql.cursors

LISTENER_PORT = 50008
LISTENER_TIMEOUT = 2
connection = pymysql.connect(
        host='mysql-db',
        user='root',
        password='root',
        database='teia',
        )

def process_video(video_name, user_id, video_class):
    '''asdf'''
    print('processing video')
    os.system('rm -f videos/frames/*')
    os.system(f'cd videos; sh extract_frames {video_name} 0.01')

    # insert new video
    print("---------------------")
    print(f"video clas : {video_class}")
    print("---------------------")
    with connection.cursor() as cur:
        cur.execute("insert into video (name, user_id, class) values (%s, %s, %s)", (video_name, user_id, video_class))
        connection.commit()
        video_id = cur.lastrowid

        print('executing aws')
        frame_paths = glob.glob("videos/frames/*")
        for frame_path in frame_paths:
            # TODO: im only using the first face 
            data = usage_demo(frame_path)
            if len(data) == 0:
                continue

            for face in data:
                if('emotions' not in face):
                    continue
                emotions = face['emotions']
                for emotion in emotions:
                    confiablity = 100   
                    cur.execute("insert into emotions (names, confiability, video_id, video_class, usuario_id) values(%s, %s, %s, %s, %s)", (emotion, confiablity,  video_id, video_class, user_id))
                    connection.commit()

def main():
    '''Initialize a socket listener in order to wait a video to process it'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            try:
                listener.bind(('localhost', LISTENER_PORT))
            except socket.error as except_return:
                # TODO: Handle when the port is occupied
                print('Can\'t connect to localhost')
                print(except_return)
                sys.exit(1)
            listener.listen(1)

            while True:
                try:
                    (client, (ip_, port)) = listener.accept()
                    with client:
                        print(f'Connected to: {ip_}:{port}')
                        client.settimeout(2)
                        while True:
                            try:
                                print('waiting for data')
                                ret = client.recv(1024).decode('utf-8')
                            except socket.timeout:
                                continue
                            else:
                                if not ret:
                                    break
                                values = ret.split(';')
                                if len(values) < 3:
                                    print('invalid message from app')
                                    continue
                                process_video(values[0], values[1], values[2])
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print('exiting')



if __name__ == '__main__':
    main()
