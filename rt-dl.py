import json
import requests
import youtube_dl

from pathlib import Path

auth_url = "https://auth.roosterteeth.com/oauth/token"
ep_list_url = "https://svod-be.roosterteeth.com/api/v1/shows/{}/episodes"
svod_url = "https://svod-be.roosterteeth.com/api/v1/episodes/{}/videos"

auth_payload = {"client_id":"4338d2b4bdc8db1239360f28e72f0d9ddb1fd01e7a38fbb07b4b1f4ba4564cc5",
        "grant_type":"password",
        "username":"MY_USERNAME",
        "password":"MY_PASSWORD",
        "scope":"user public"}

#
#   Generate Auth Token
#
auth_req = requests.post(auth_url, data=auth_payload)
if auth_req.status_code == 200:
    auth_resp = json.loads(auth_req.text)
    headers = {"Authorization": "Bearer {}".format(auth_resp['access_token'])}
else:
    print("Unable to get access_token! HTTP Error {}".format(auth_req.status_code))
    exit()

#
#   Get Episode lists
#
show_list = ["last-call", "rooster-teeth-podcast-post-show", "still-open"]
for show in show_list:
    ep_req = requests.get(ep_list_url.format(show))
    if ep_req.status_code != 200:
        print("Error getting episode list for {}!\n".formaT(show))
    else:
        # Loop through episodes
        ep_resp = json.loads(ep_req.text)
        for e in ep_resp["data"]:
            title = e["attributes"]["title"]
            slug = e["attributes"]["slug"]
            print("Title: {}".format(title))
            print("Slug: {}".format(slug))

            # If we don't have this video, download it
            vid_dest = "./{}/video/{}.mp4".format(show, slug)
            if not Path(vid_dest).is_file():
                m3u8_req = requests.get(svod_url.format(slug), headers=headers)
                if m3u8_req.status_code != 200:
                    print("Unable to get URL for this episode!")
                else:
                    url = json.loads(m3u8_req.text)["data"][0]["attributes"]["url"]
                    print("URL: {}\n".format(url))
                    ydl_opts = {
                        "format": "worst",
                        "logtostderr": True,
                        "outtmpl": vid_dest
                        }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

            # Check if we already have this as mp3
            mp3_dest = "./{}/audio/().mp3"
            if Path(mp3_dest).is_file():
                continue
            else:
                print("Downloading to {}...".format(mp3_dest))

            exit()
