import requests
import re
from PIL import Image

def pp_download(username):
    url = f"https://www.instagram.com/{username}/"
    final_url = None

    try:
        if re.match(r"^https://www.instagram.com/[a-zA-Z0-9_]+/$", url):
            final_url = f"{url}?__a=1"
        elif re.match(r"^https://www.instagram.com/[a-zA-Z0-9_]+$", url):
            final_url = f"{url}/?__a=1"
        else:
            raise ValueError("Invalid URL")
    except ValueError as e:
        print(f"Error: {str(e)}")
        return

    try:
        response = requests.get(final_url)
        response.raise_for_status()
        match = re.search(r'"profile_pic_url_hd":"([^"]+)"', response.text)
        if match:
            profile_picture_url = match.group(1)
            response = requests.get(profile_picture_url, stream=True)
            response.raise_for_status()

            with open(f"{username}.jpg", "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            with Image.open(f"{username}.jpg") as im:
                im.show()
            print(f"Profile picture for {username} downloaded successfully")
        else:
            raise Exception("Profile picture URL not found in the response")
    except Exception as e:
        print(f"Error: {str(e)}")
