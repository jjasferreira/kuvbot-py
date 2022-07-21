# Import auxiliary functions
from utils import *


def action_like_tweet_contains(search: str):

    api = authenticate()

    tweet_url = like_tweet_contains(api, search, "recent")
    print("[LIKE]:\n" + "Containing: " + search + "\nTweet URL: " + tweet_url + "\n==========")


def action_tweet_image_picsum(image_size: int):

    api = authenticate()
    ids = load_image_ids_state()

    [id, author] = get_random_image_picsum(ids)
    url = "https://picsum.photos/id/" + str(id) + "/" + str(image_size)
    [tag, confidence] = tag_url_image_imagga(url)

    url += "?grayscale"
    image_path = download_image(url, str(id))
    edit_path = edit_image(image_path, "Kuv")

    alt = "Author: " + author + "\nTag: " + tag + "\nConfidence: " + confidence
    tweet_media_metadata(api, edit_path, alt)
    print("[TWEET]:\n" + "Image ID: " + str(id) + "\n" + alt + "\n==========")
    save_image_ids_state(ids)