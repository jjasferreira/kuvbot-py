# Import auxiliary functions
from utils import *


def action_like_tweet_contains(search: str):
    """Likes a random recent Tweet that contains the word(s) passed as
    argument. Prints the confirmation of action."""

    api = authenticate()

    tweet_url = like_tweet_contains(api, search, "recent")
    print(
        "[LIKE]:\n"
        + "Containing: "
        + search
        + "\nTweet URL: "
        + tweet_url
        + "\n=========="
    )


def action_tweet_image_unsplash():
    """Tweets an edited image from Unsplash with an alt text containing the
    author, tag guess, confidence percentage and url. It also replies to the
    Tweet with the image author's Twitter handle, if known. Prints the
    confirmation of action."""

    api = authenticate()

    [id, color, download, url, author, handle] = get_random_image_unsplash()

    [tag, confidence] = tag_url_image_imagga(download)

    image_path = download_image(download, id)

    edit_path = edit_image(image_path, (2000, 2000), color)

    alt = (
        "Author: "
        + author
        + "\nTag: "
        + tag
        + "\nConfidence: "
        + confidence
        + "\n\n"
        + url[8:]
    )

    tweet_id = tweet_media_metadata(api, edit_path, alt)

    if isinstance(handle, str):
        text = "@" + str(handle)
        reply_to_tweet(api, tweet_id, text)

    print("[TWEET]:\n" + alt + "\n==========")
