import requests
import random
from instagrapi import Client
import json
import re
import imaplib
import email
from instagrapi.mixins.challenge import ChallengeChoice
from PIL import Image
import os
import time
import pandas as pd
from database_operations import *
from cloutsy import initiate_order
proxies0 = ["3a658c2df1e8d954fbe2__cr.so:0cc4c57886851e53@gw.dataimpulse.com:823"]

CHALLENGE_EMAIL = None
CHALLENGE_EMAIL_PASSWORD = None


def generate_unused_proxy(used_proxies, max_attempts=100):
    if not used_proxies:
        print(f"used proxies list is empty")
        return None
    user_pass = "42f0ee2c5907656693ee:b5f203e0222b9ac9"
    host = "gw.dataimpulse.com"
    
    for _ in range(max_attempts):
        port = random.randint(10000, 20000)
        new_proxy = f"{user_pass}@{host}:{port}"
        if new_proxy not in used_proxies:
            return new_proxy
    
    print(f"Failed to generate a unique proxy after {max_attempts} attempts")
    return None


# def scan_user(user_name):
#     url = "https://scrappygram.p.rapidapi.com/api/insta/andr/userinfov1"
#     headers = {
#         "x-rapidapi-key": "2f5b0dee51msh47a4e9364d8b93fp13c2b6jsn52cfc6d849dc",
#         "x-rapidapi-host": "scrappygram.p.rapidapi.com"
#     }
#     try:
#         response = dict()
#         for _ in range(25):
#             querystring = {"username": f"{user_name}", "proxy": f"{random.choice(proxies0)}"}
#             try:
#                 response = requests.get(url, headers=headers, params=querystring)
#                 if response.status_code == 200 and response.json()['biography']:
#                     break
#             except:
#                 pass
#             time.sleep(1)
#         bio = response.json()['biography']
#         name = response.json()['full_name']
#         profile_pic = response.json()['profile_pic_url']
#         if bio or name or profile_pic:
#             return {'bio': bio, 'name': name, 'profile_pic': profile_pic}
#         else:
#             return None
#     except:
#         return None


# def fetch_posts(user_name):
#     url = "https://scrappygram.p.rapidapi.com/api/insta/andr/allpostscrapper"
#     headers = {
#         "X-RapidAPI-Key": "2f5b0dee51msh47a4e9364d8b93fp13c2b6jsn52cfc6d849dc",
#         "X-RapidAPI-Host": "scrappygram.p.rapidapi.com"
#     }
#     try:
#         response = dict()
#         for _ in range(25):
#             querystring = {"username": f"{user_name}", "proxy": f"{random.choice(proxies0)}"}
#             try:
#                 response = requests.get(url, headers=headers, params=querystring)
#                 if response.status_code == 200 and response.json()['data']['user']['edge_owner_to_timeline_media']:
#                     break
#             except:
#                 pass
#         posts_raw_data = dict()
#         num_of_posts = random.randint(2, 20)
#         available_posts = len(response.json()['data']['user']['edge_owner_to_timeline_media']['edges'])
#         if num_of_posts > available_posts:
#             posts_raw_data = response.json()['data']['user']['edge_owner_to_timeline_media']['edges']
#         else:
#             posts_raw_data = response.json()['data']['user']['edge_owner_to_timeline_media']['edges'][:num_of_posts]
#         posts = []
#         for post in posts_raw_data:
#             try:
#                 if post['node']['is_video']:
#                     media = post['node']['video_url']
#                     is_video = True
#                 elif not post['node']['is_video']:
#                     media = post['node']['display_url']
#                     is_video = False
#                 try:
#                     caption = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
#                 except:
#                     caption = ''
#                 posts.append({
#                     'media': media,
#                     'caption': caption,
#                     'is_video': is_video
#                 })
#             except:
#                 pass
#         return posts

#     except:
#         return None


def scan_user_and_fetch_posts(user_name):
    url = "https://instagram-media-api.p.rapidapi.com/user/profile"
    payload = {
	"username": f"{user_name}",
	"proxy": ""
            }
    headers = {
	"x-rapidapi-key": "2f5b0dee51msh47a4e9364d8b93fp13c2b6jsn52cfc6d849dc",
	"x-rapidapi-host": "instagram-media-api.p.rapidapi.com",
	"Content-Type": "application/json"
    }
    for _ in range(10):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200 and response.json()['biography']:
                bio = response.json()['biography']
                name = response.json()['full_name']
                profile_pic = response.json()['profile_pic_url']
                media_data = random.choice(response.json()['edge_owner_to_timeline_media']['edges'])
                media = media_data['node']['video_url'] if media_data['node']['is_video'] else media_data['node']['display_url']
                is_video = media_data['node']['is_video']
                caption = media_data['node']['edge_media_to_caption']['edges'][0]['node']['text']

                if bio or name or profile_pic:
                    return [{'bio': bio, 'name': name, 'profile_pic': profile_pic}, {'media':media,'caption':caption,'is_video':is_video}]
        except:
            pass
    return None




def get_user_profile_info(user_name):
    user_info,user_media = scan_user_and_fetch_posts(user_name)
    if user_info or  user_media:
        return {'user_info': user_info, 'user_media': user_media}
    return None


def challenge_code_handler(username, choice):
    if choice == ChallengeChoice.SMS:
        pass
    elif choice == ChallengeChoice.EMAIL:
        return get_code_from_email(username)
    return False


def get_imap_server(email_address):
    domain = email_address.split('@')[-1]
    return f"imap.{domain}"


def get_code_from_email(username):
    time.sleep(60)
    global CHALLENGE_EMAIL , CHALLENGE_EMAIL_PASSWORD 
    imap_server = get_imap_server(CHALLENGE_EMAIL)
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(CHALLENGE_EMAIL, CHALLENGE_EMAIL_PASSWORD)
    mail.select("inbox")
    result, data = mail.search(None, "(UNSEEN)")
    assert result == "OK", "Error1 during get_code_from_email: %s" % result
    ids = data.pop().split()
    for num in reversed(ids):
        mail.store(num, "+FLAGS", "\\Seen")  # mark as read
        result, data = mail.fetch(num, "(RFC822)")
        assert result == "OK", "Error2 during get_code_from_email: %s" % result
        msg = email.message_from_string(data[0][1].decode())
        payloads = msg.get_payload()
        if not isinstance(payloads, list):
            payloads = [msg]
        code = None
        for payload in payloads:
            body = payload.get_payload(decode=True).decode()
            if "<div" not in body:
                continue
            match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
            if not match:
                continue
            print("Match from email:", match.group(1))
            match = re.search(r">(\d{6})<", body)
            if not match:
                print('Skip this email, "code" not found')
                continue
            code = match.group(1)
            if code:
                return code
    return False


def convert_webp_to_jpg(webp_path):
    if not os.path.exists(webp_path):
        raise FileNotFoundError(f"No such file: '{webp_path}'")
    with Image.open(webp_path) as img:
        file_name = os.path.splitext(webp_path)[0]
        jpg_path = f"{file_name}.jpg"
        img = img.convert("RGB")
        img.save(jpg_path, "JPEG")
    os.remove(webp_path)
    return jpg_path





def post_content_to_user_profile(user_name,password,new_password,new_user_name, new_full_name,target,challenge_email,challenge_email_password):
    global CHALLENGE_EMAIL , CHALLENGE_EMAIL_PASSWORD 
    CHALLENGE_EMAIL = challenge_email
    CHALLENGE_EMAIL_PASSWORD = challenge_email_password
    content = get_user_profile_info(target)
    if not content:
        print(f"Scanning user went unsuccessfull for {user_name}!")
        print("==================================================================================")
        return False
    users_data = dict()
    used_proxies = None
    connection = db_connection()
    if connection is not None:
        users_data = get_users_data(connection)
        used_proxies = get_used_proxies(connection)
    elif connection is None:
        return False
    if user_name in [info['user_name'] for info in users_data] or new_user_name in [info['user_name'] for info in users_data]:
        print(f"Skipping {user_name} , already populated!")
        print("==================================================================================")
        return False
    try:
        cl = Client()
        random_proxy = generate_unused_proxy(used_proxies)
        if random_proxy:
            cl.set_proxy(random_proxy)
        elif not random_proxy:
            print(f"Aborting account population operations for {user_name}, detail : Proxy not generated!")
            print("==================================================================================")
            return False
        cl.challenge_code_handler = challenge_code_handler
        is_logged = cl.login(user_name, password)
        if is_logged:
            print(f"logged in using : {user_name}")
            user_data_dict = dict()
            posted_media = list()
            try:
                cl.photo_download_by_url(content['user_info']['profile_pic'],f'{user_name}_profile_pic')
                cl.account_change_picture(f'{user_name}_profile_pic.jpg')
                if os.path.exists(f'{user_name}_profile_pic.jpg'):
                    os.remove(f'{user_name}_profile_pic.jpg')
            except Exception as e:
                print(f'profile pic operation failed : {e}')
                if os.path.exists(f'{user_name}_profile_pic.jpg'):
                    os.remove(f'{user_name}_profile_pic.jpg')
            try:
                cl.account_edit(biography=content['user_info']['bio'])
            except Exception as e:
                print(f'profile biography operation failed : {e}')
                print("==================================================================================")
                return False
            try:
                cl.account_edit(username=new_user_name)
                user_data_dict["user_name"] = new_user_name
            except Exception as e:
                print(f'username  operation failed: {e}')
                user_data_dict["user_name"] = user_name
                print("==================================================================================")
                return False
            try:
                cl.account_edit(full_name=new_full_name)
            except Exception as e:
                print(f'fullname  operation failed: {e}')
            try:
                media = random.choice(content['user_media'])
                if media['is_video']:
                    cl.video_download_by_url(media['media'], f'{user_name}_media_video')
                    cl.video_upload(f'{user_name}_media_video.mp4',media['caption'])
                    posted_media.append( media['media'])
                    if os.path.exists(f'{user_name}_media_video.mp4'):
                        os.remove(f'{user_name}_media_video.mp4')
                    if os.path.exists(f'{user_name}_media_video.mp4.jpg'):
                        os.remove(f'{user_name}_media_video.mp4.jpg')
                    
                elif not media['is_video']:
                    cl.photo_download_by_url(media['media'],f'{user_name}_media_pic')
                    if os.path.exists(f'{user_name}_media_pic.webp'):
                        img = convert_webp_to_jpg(f'{user_name}_media_pic.webp')
                    else:
                        img = f'{user_name}_media_pic.jpg'
                    cl.photo_upload(img,media['caption'])
                    posted_media.append( media['media'])
                    if os.path.exists(img):
                        os.remove(img)
            except Exception as e:
                print(f'profile media operation failed : {e}')
                if os.path.exists(f'{user_name}_media_video.mp4'):
                    os.remove(f'{user_name}_media_video.mp4')
                if os.path.exists(f'{user_name}_media_video.mp4.jpg'):
                    os.remove(f'{user_name}_media_video.mp4.jpg')
                if os.path.exists(f'{user_name}_media_pic.webp'):
                    os.remove(f'{user_name}_media_pic.webp')
                if os.path.exists(f'{user_name}_media_pic.jpg'):
                    os.remove(f'{user_name}_media_pic.jpg')
            try:
                story = random.choice(content['user_media'])
                if story['is_video']:
                    cl.video_download_by_url(story['media'], f'{user_name}_story_video')
                    cl.video_upload_to_story(f'{user_name}_story_video.mp4',story['caption'])
                    posted_media.append(story['media'])
                    if os.path.exists(f'{user_name}_story_video.mp4'):
                        os.remove(f'{user_name}_story_video.mp4')
                    if os.path.exists(f'{user_name}_story_video.mp4.jpg'):
                        os.remove(f'{user_name}_story_video.mp4.jpg')
                elif not story['is_video']:
                    cl.photo_download_by_url(story['media'],f'{user_name}_story_pic')
                    if os.path.exists(f'{user_name}_story_pic.webp'):
                        img = convert_webp_to_jpg(f'{user_name}_story_pic.webp')
                    else:
                        img = f'{user_name}_story_pic.jpg'
                    cl.photo_upload_to_story(img,story['caption'])
                    posted_media.append(story['media'])
                    if os.path.exists(img):
                        os.remove(img)
            except Exception as e:
                print(f'profile story operation failed : {e}')
                if os.path.exists(f'{user_name}_story_video.mp4'):
                    os.remove(f'{user_name}_story_video.mp4')
                if os.path.exists(f'{user_name}_story_video.mp4.jpg'):
                    os.remove(f'{user_name}_story_video.mp4.jpg')
                if os.path.exists(f'{user_name}_story_pic.webp'):
                    os.remove(f'{user_name}_story_pic.webp')
                if os.path.exists(f'{user_name}_story_pic.webp'):
                    os.remove(f'{user_name}_story_pic.jpg')
            if password != new_password:
                try:
                    cl.change_password(password,new_password)
                    user_data_dict["password"] = new_password
                except Exception as e:
                    print(f'password change operation failed : {e}')
                    user_data_dict["password"] = password
            elif password == new_password:
                user_data_dict["password"] = password
            
            initiate_order(f"https://www.instagram.com/{new_user_name}/")
            time.sleep(2*60)
            try:
                cl.relogin()
                cl.account_set_private()
            except Exception as e:
                print(f'setting account status to private failed : {e}')
            user_data_dict["proxy"] = random_proxy
            user_data_dict["settings"] = cl.get_settings()
            user_data_dict["target"] = target
            user_data_dict["posted_media"] = posted_media
            user_data_dict["challenge_email"] = challenge_email
            user_data_dict["challenge_email_passowrd"] = challenge_email_password
        else:
            print(f"can't login using : {user_name}!")
            print("==================================================================================")
            return False
        insert_record(connection,dict(user_data_dict))
        print("==================================================================================")
    except Exception as e:
        print(f"something went wrong with : {user_name} , detail : {e}")
        print("==================================================================================")
        return False
    return True



# def post_media_to_user_profile(user_name):
#     users_data = dict()
#     if os.path.exists("new_instagram_accounts.json"):
#         with open("new_instagram_accounts.json", 'r') as json_file:
#             users_data = json.load(json_file)
#     elif not os.path.exists("new_instagram_accounts.json"):
#         print("users data file not found!")
#         return False
#     user = users_data[user_name]
#     user_name = user['user_name']
#     password = user['password']
#     proxy = user['proxy']
#     settings = user['settings']
#     target = user['target']
#     posted_media = user['posted_media']
#     content = fetch_posts(target)
#     if not content:
#         print(f"Scanning user went unsuccessfull for {user_name}!")
#         print("==================================================================================")
#         return False
#     try:
#         cl = Client(settings)
#         cl.set_proxy(proxy)
#         cl.challenge_code_handler = challenge_code_handler
#         cl.login(user_name,password)
#         if cl.relogin():
#             print(f"logged in using : {user_name}")
#             try:
#                 for _ in range(15):
#                     media = random.choice(content)
#                     if media['media'] not in posted_media:
#                         break
#                 if media['is_video']:
#                     cl.video_download_by_url(media['media'], f'{user_name}_media_video')
#                     cl.video_upload(f'{user_name}_media_video.mp4',media['caption'])
#                     posted_media.append(media['media'])
#                     if os.path.exists(f'{user_name}_media_video.mp4'):
#                         os.remove(f'{user_name}_media_video.mp4')
#                     if os.path.exists(f'{user_name}_media_video.mp4.jpg'):
#                         os.remove(f'{user_name}_media_video.mp4.jpg')
#                 elif not media['is_video']:
#                     cl.photo_download_by_url(media['media'],f'{user_name}_media_pic')
#                     if os.path.exists(f'{user_name}_media_pic.webp'):
#                         img = convert_webp_to_jpg(f'{user_name}_media_pic.webp')
#                     else:
#                         img = f'{user_name}_media_pic.jpg'
#                     cl.photo_upload(img,media['caption'])
#                     posted_media.append(media['media'])
#                     if os.path.exists(img):
#                         os.remove(img)
#             except Exception as e:
#                 print(f'profile media operation failed : {e}')
#                 if os.path.exists(f'{user_name}_media_video.mp4'):
#                     os.remove(f'{user_name}_media_video.mp4')
#                 if os.path.exists(f'{user_name}_media_video.mp4.jpg'):
#                     os.remove(f'{user_name}_media_video.mp4.jpg')
#                 if os.path.exists(f'{user_name}_media_pic.webp'):
#                     os.remove(f'{user_name}_media_pic.webp')
#                 if os.path.exists(f'{user_name}_media_pic.jpg'):
#                     os.remove(f'{user_name}_media_pic.jpg')
#             try:
#                 for _ in range(15):
#                     story = random.choice(content)
#                     if story['media'] not in posted_media:
#                         break
#                 if story['is_video']:
#                     cl.video_download_by_url(story['media'], f'{user_name}_story_video')
#                     cl.video_upload_to_story(f'{user_name}_story_video.mp4',story['caption'])
#                     posted_media.append(story['media'])
#                     if os.path.exists(f'{user_name}_story_video.mp4'):
#                         os.remove(f'{user_name}_story_video.mp4')
#                     if os.path.exists(f'{user_name}_story_video.mp4.jpg'):
#                         os.remove(f'{user_name}_story_video.mp4.jpg')
#                 elif not story['is_video']:
#                     cl.photo_download_by_url(story['media'],f'{user_name}_story_pic')
#                     if os.path.exists(f'{user_name}_story_pic.webp'):
#                         img = convert_webp_to_jpg(f'{user_name}_story_pic.webp')
#                     else:
#                         img = f'{user_name}_story_pic.jpg'
#                     cl.photo_upload_to_story(img,story['caption'])
#                     posted_media.append(story['media'])
#                     if os.path.exists(img):
#                         os.remove(img)
#             except Exception as e:
#                 print(f'profile story operation failed : {e}')
#                 if os.path.exists(f'{user_name}_story_video.mp4'):
#                     os.remove(f'{user_name}_story_video.mp4')
#                 if os.path.exists(f'{user_name}_story_video.mp4.jpg'):
#                     os.remove(f'{user_name}_story_video.mp4.jpg')
#                 if os.path.exists(f'{user_name}_story_pic.webp'):
#                     os.remove(f'{user_name}_story_pic.webp')
#                 if os.path.exists(f'{user_name}_story_pic.webp'):
#                     os.remove(f'{user_name}_story_pic.jpg')
#             users_data[user_name]["settings"] = cl.get_settings()
#             users_data[user_name]["posted_media"] = posted_media
#         else:
#             print("can't login using : {user_name}!")
#             print("==================================================================================")
#             return False
#     except Exception as e:
#         print(f"something went wrong with : {user_name} , detail : {e}")
#         print("==================================================================================")
#         return False
#     with open("new_instagram_accounts.json", 'w') as f:
#         json.dump(users_data, f, indent=4)
#     print("==================================================================================")
#     return True
