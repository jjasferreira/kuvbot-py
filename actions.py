# Import auxiliary functions
from utils import *

BOT = "kuvbot"
REPLY = "kuvrep"


def action_like_tweet():
    """Likes a random recent Tweet that contains the word(s) specified inside
    the function. Prints the confirmation of action."""

    api = authenticate(BOT)

    search = "#photography"
    tweet_url = like_tweet_contains(api, search, "recent")
    print(
        "[LIKE]:\n"
        + "Containing: "
        + search
        + "\nTweet URL: "
        + tweet_url
        + "\n=========="
    )


def action_tweet_image():
    """Tweets an edited image from Unsplash with an alt text containing the
    author, tag guess, confidence percentage and url. It also replies to the
    Tweet with the image author's Twitter handle, if known. Prints the
    confirmation of action."""

    api = authenticate(BOT)

    [id, color, download, url, author, handle] = get_random_image_unsplash()
    [tag, confidence] = tag_url_image_imagga(download)
    image_path = download_image(download, id)
    edit_path = edit_image(image_path, (2000, 2000), color)

    alt = "Author: " + author + "\nTag: " + tag + "\nConfidence: " \
    + confidence + "\n\n" + url[8:]
    tweet_id = tweet_media_metadata(api, edit_path, alt)
    tweet_url = "https:/twitter.com/" + BOT + "/status/" + str(tweet_id)

    if isinstance(handle, str):
        user_id = get_twitter_user_id(api, handle)
        if isinstance(user_id, int):
            text = "@" + handle
            api = authenticate(REPLY)
            reply_to_tweet(api, tweet_id, text)

            message = (
                "Hi there!\n Congratulations! A photo of yours was featured \
                on our page and credited to you. Thank you for being part \
                of the photography world! ❤️\n If you want us to remove \
                your work, please let us know. "
                + tweet_url
            )
            dm_user(api, user_id, message)

    print("[TWEET]:\n" + alt + "\n==========")