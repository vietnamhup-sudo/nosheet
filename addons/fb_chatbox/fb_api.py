import requests
import base64


def convert_to_avatar_1920(avatar_url):
    avatar_b64 = False
    try:
        if avatar_url:
            img_res = requests.get(avatar_url, timeout=10)
            if img_res.ok:
                avatar_b64 = base64.b64encode(img_res.content).decode("utf-8")
    except Exception:
        pass
    return avatar_b64

def get_fb_page_info(access_token):
    url = "https://graph.facebook.com/v19.0/me"
    params = {
        "fields": "id,name,picture",
        "access_token": access_token
    }

    res = requests.get(url, params=params, timeout=10)

    if not res.ok:
        return {}

    data = res.json()
    avatar_url = (
        data.get("picture", {})
            .get("data", {})
            .get("url")
    )
    avatar_b64 = convert_to_avatar_1920(avatar_url)

    return {
        "page_id": data.get("id"),
        "page_name": data.get("name"),
        "avatar_1920": avatar_b64,
    }

def get_fb_user_info(sender_id, access_token):
    url = f"https://graph.facebook.com/v19.0/{sender_id}"
    params = {
        "fields": "first_name,last_name,profile_pic",
        "access_token": access_token
    }

    res = requests.get(url, params=params, timeout=10)

    if not res.ok:
        return {}

    data = res.json()
    avatar_b64 = convert_to_avatar_1920(data.get("profile_pic"))
    return {
        "full_name": data.get("last_name", "") + " " + data.get("first_name", ""),
        "avatar_1920": avatar_b64,
        "sender_id": sender_id,
    }