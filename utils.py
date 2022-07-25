# Python modules
from ast import literal_eval
from json import dump
from os import environ, makedirs, path
from PIL import Image, ImageColor, ImageDraw
from requests import get
from shutil import copyfileobj, rmtree

# Twitter module
import tweepy as tp

# Maximum ID of Picsum Photos as of 16/07/2022
MAX_ID = 1084

# Image file directory and format and JSON files directory
IMG_DIR = "imgs/"
IMG_FORMAT = ".jpg"


def authenticate():
    """Authenticates to the Twitter API using a developer account's API keys and a
    bot account's Access Token keys, both of which must be stored as environment
    variables. Returns the API object to be used."""

    # Get the dictionary containing the keys
    keys = literal_eval(environ["KEYS"])

    # Extract the keys
    api_key = keys["TWITTER_API_KEY"]
    api_key_secret = keys["TWITTER_API_KEY_SECRET"]
    access_token = keys["TWITTER_KUVBOT_ACCESS_TOKEN"]
    access_token_secret = keys["TWITTER_KUVBOT_ACCESS_TOKEN_SECRET"]

    # Authenticate to the Twitter API
    auth = tp.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tp.API(auth, wait_on_rate_limit=True)
    return api


def get_random_image_unsplash():
    """Authenticates to the Unsplash API using an API key stored in an environment
    variable and gets a new random image using. Returns the average color, the
    download url, the Unsplash url, the user's name and its Twitter handle."""

    # Get the dictionary containing the keys
    keys = literal_eval(environ["KEYS"])

    # Authenticate with the API key and get a random image
    api_key = keys["UNSPLASH_API_KEY"]
    r = get("https://api.unsplash.com/photos/random?client_id=" + api_key)

    # Get image info
    if r.status_code == 200:
        id = r.json()["id"]
        color = r.json()["color"]
        download_url = r.json()["urls"]["raw"]
        url = r.json()["links"]["html"]
        user = r.json()["user"]["name"]
        twitter_handle = r.json()["user"]["twitter_username"]
        return [id, color, download_url, url, user, twitter_handle]
    else:
        raise Exception("Image couldn't be retrieved")


def tag_url_image_imagga(url: str):
    """Authenticates to the Imagga API using access keys stored in an environment
    variable and attempts to give different tags to the image contained in the
    given url with corresponding confidence rates. Returns the most accurate
    answer amongst all."""

    # Get the dictionary containing the keys
    keys = literal_eval(environ["KEYS"])

    # Authenticate and get a response fo
    api_key = keys["IMAGGA_API_KEY"]
    api_key_secret = keys["IMAGGA_API_KEY_SECRET"]

    # Get the response from Imagga
    response = get(
        "https://api.imagga.com/v2/tags?image_url=%s" % url,
        auth=(api_key, api_key_secret),
    )

    # Dump full response to a file
    """
    file = open("tags.json", "w")
    dump(response.json(), file)
    file.close()
    """

    # Return the most accurate attempt
    tag = response.json()["result"]["tags"][0]["tag"]["en"]
    confidence = response.json()["result"]["tags"][0]["confidence"]
    con = str(round(confidence, 2)) + "%"
    return [tag, con]


def download_image(url: str, filename: str):
    """Downloads an image from the given url to the directory IMG_DIR with the
    name filename and the format IMG_FORMAT. Returns the path to that image."""

    # Eliminates the directory containing the images and re-creates it
    if path.exists(IMG_DIR):
        rmtree(IMG_DIR)
    makedirs(IMG_DIR)

    # Open the URL image and return the stream content
    r = get(url, stream=True)

    # Check if the image was retrieved and ensure its file size is not zero
    if r.status_code == 200:
        r.raw.decode_content = True
        image_path = IMG_DIR + filename + IMG_FORMAT
        with open(image_path, "wb") as f:
            copyfileobj(r.raw, f)
            return image_path
    else:
        raise Exception("Image couldn't be downloaded")


def edit_image(image_path: str, resize_params: tuple, color: str):
    """Edits the image found at the image_path given with the text passed as
    argument using the pillow module. Returns the edited image path."""

    # Open, crop and resize the original image
    image = Image.open(image_path)
    size = min(image.size)
    crop = image.crop(
        (
            (image.width - size) // 2,
            (image.height - size) // 2,
            (image.width + size) // 2,
            (image.height + size) // 2,
        )
    )
    resize = crop.resize((resize_params[0], resize_params[1]), Image.ANTIALIAS)

    # Open the resized image and draw hexagon with a certain radius
    draw = ImageDraw.Draw(resize)
    x = resize.width - 85
    y = resize.height - 80
    r = 60
    color = ImageColor.getcolor(color, "RGB")
    draw.regular_polygon((x, y, r), 6, fill=color, outline=None)

    # Draw logo
    logo_path = "misc/light_logo.png"
    red = 0.299 * color[0]
    green = 0.587 * color[1]
    blue = 0.144 * color[2]
    if (red + green + blue) > 186:
        logo_path = "misc/dark_logo.png"
    logo = Image.open(logo_path)
    resize_logo = logo.resize((2 * r, 2 * r), Image.ANTIALIAS)
    resize.paste(resize_logo, (x - r, y - r, x + r, y + r), resize_logo)

    # Save the result
    edit_path = IMG_DIR + "edit" + IMG_FORMAT
    resize.save(edit_path)
    return edit_path


def tweet_media_metadata(api: tp.API, path: str, alt: str):
    """Tweets the file found at the path given with the alt text passed as an
    argument, using the API object given. Returns the media"""

    # Tweet image with its alt text
    file = open(path, "rb")
    r = api.media_upload(filename=path, file=file)
    media_id = r.media_id_string
    api.create_media_metadata(media_id, alt)
    status = api.update_status("", media_ids=[media_id])
    return status.id


def reply_to_tweet(api: tp.API, tweet_id: int, text: str):
    """Replies to the given Tweet ID with the text passed as an argument,
    using the connection to the Twitter API specified in the parameter."""
    api.update_status(
        status=text, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True
    )


def like_tweet_contains(api: tp.API, search: str, result: str):
    """Likes a random recent Tweet that contains the word(s) passed as an
    argument, using the type of search specified in the result argument
    and the API object given. Returns the URL of the Tweet."""

    # Get a Tweet that uses the words in the search argument
    tweet = api.search_tweets(search, lang="en", result_type=result, count=1).statuses[
        0
    ]
    tweet_id = tweet.id_str

    # Like the Tweet and return its URL
    api.create_favorite(tweet_id)
    tweet_url = "https://twitter.com/i/web/status/" + tweet_id
    return tweet_url
