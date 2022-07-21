# Python modules
from json import dump, load, loads
from os import makedirs, path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from random import randint
from requests import get
from shutil import copyfileobj

# Twitter module
import tweepy as tp

# Maximum ID of Picsum Photos as of 16/07/2022
MAX_ID = 1084

# Image file directory and format and JSON files directory
IMG_DIR = "imgs"
IMG_FORMAT = ".jpg"
JSON_DIR = "json"


def authenticate():
    """Authenticates to the Twitter API using a developer account's API keys and a
    bot account's Access Token keys, both of which must be stored in a JSON file.
    Returns the API object to be used."""

    # Open local credentials file
    file = open("keys.json", "r")
    keys = load(file)
    file.close()

    # Get the keys from the file
    api_key = keys["twitter"]["api_key"]
    api_key_secret = keys["twitter"]["api_key_secret"]
    access_token = keys["twitter"]["kuvbot"]["access_token"]
    access_token_secret = keys["twitter"]["kuvbot"]["access_token_secret"]

    # Authenticate to Twitter API
    auth = tp.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tp.API(auth, wait_on_rate_limit=True, parser=tp.parsers.JSONParser())
    return api


def load_image_ids_state():
    """Loads the current array stored in a JSON file that signals which images have
    already been selected, if it exists. Otherwise, it creates one to be stored.
    Returns the array."""

    # If there is no serialized array, initialize one
    if not path.exists(JSON_DIR + "/ids.json"):
        ids = [0] * MAX_ID

    # If there is one already, load it
    else:
        file = open(JSON_DIR + "/ids.json", "r")
        ids = load(file)
        file.close()

    return ids


def save_image_ids_state(ids):
    """Saves the array passed as an argument and that signals which images have
    already been selected to a JSON file, for future usage."""

    # (Over)write array to file
    file = open(JSON_DIR + "/ids.json", "w")
    dump(ids, file)
    file.close()


def get_random_image_picsum(ids):
    """Gets a new random image using the Lorem Picsum API. Returns the id and
    the author of the new image."""

    # Choose a random new image that is available
    while 1:
        id = randint(0, MAX_ID)
        metadata_url = "https://picsum.photos/id/" + str(id) + "/info"
        page = get(metadata_url)
        if (ids[id] < 1) and (page.text != "Image does not exist\n"):
            break

    # Get the image author's name
    author = loads(page.text)["author"]
    return [id, author]


def tag_url_image_imagga(url: str):
    """Attempts to give different tags to the image contained in the given url
    with corresponding confidence rates. Returns the most accurate answer amongst all.
    """

    # Open local credentials file
    file = open(JSON_DIR + "/keys.json", "r")
    keys = load(file)
    file.close()

    # Authentication with the API keys
    api_key = keys["imagga"]["api_key"]
    api_key_secret = keys["imagga"]["api_key_secret"]

    # Get the response from Imagga
    response = get(
        "https://api.imagga.com/v2/tags?image_url=%s" % url,
        auth=(api_key, api_key_secret),
    )

    # Dump full response to a file
    file = open(JSON_DIR + "/tags.json", "w")
    dump(response.json(), file)
    file.close()

    # Return the most accurate attempt
    tag = response.json()["result"]["tags"][0]["tag"]["en"]
    confidence = response.json()["result"]["tags"][0]["confidence"]
    con = str(round(confidence, 2)) + "%"
    return [tag, con]


def download_image(url: str, filename: str):
    """Downloads an image from the given url to the directory IMG_DIR with the
    name filename and the format IMG_FORMAT. Returns the path to that image."""

    # If there is no directory for the image file, create one
    if not path.exists(IMG_DIR):
        makedirs(IMG_DIR)

    # Open the URL image and return the stream content
    r = get(url, stream=True)

    # Check if the image was retrieved and ensure its file size is not zero
    if r.status_code == 200:
        r.raw.decode_content = True
        image_path = IMG_DIR + "/" + filename + IMG_FORMAT
        with open(image_path, "wb") as f:
            copyfileobj(r.raw, f)
            return image_path
    else:
        print("Error: Image couldn't be retrieved")
        return None


def edit_image(image_path: str, text: str):
    """Edits the image found at the image_path given with the text passed as
    argument using the pillow module. Returns the edited image path."""

    # Open image, select font and its coordinates with the pillow module
    image = Image.open(image_path)
    font = ImageFont.truetype("misc/Windows_Regular.ttf", 50)
    x = image.width - 82
    y = image.height - 58

    # Create piece of canvas to draw text on and blur
    new = Image.new("RGBA", image.size)
    edit_new = ImageDraw.Draw(new)
    edit_new.text((x, y), text, fill="black", font=font, anchor="mm")
    new = new.filter(ImageFilter.BoxBlur(8))

    # Paste shadow onto background and draw sharp text
    image.paste(new, new)
    edit_image = ImageDraw.Draw(image)
    edit_image.text((x, y), text, fill=255, font=font, anchor="mm")

    # Save the result
    id = image_path.split("/")[1].split(".")[0]
    edit_path = IMG_DIR + "/" + id + "_edit" + IMG_FORMAT
    image.save(edit_path)
    return edit_path


def tweet_media_metadata(api: tp.API, path: str, alt: str):
    """Tweets the file found at the path given with the alt text passed as an
    argument, using the API object given."""

    # Tweet image with its alt text
    file = open(path, "rb")
    r = api.media_upload(filename=path, file=file)
    api.create_media_metadata(r.media_id_string, alt)
    api.update_status("", media_ids=[r.media_id_string])


def like_tweet_contains(api: tp.API, search: str, result: str):
    """Likes a random recent Tweet that contains the word(s) passed as an
    argument, using the type of search specified in the result argument
    and the API object given. Returns the URL of the Tweet."""

    # Get a Tweet that uses the words in the search argument
    tweet = api.search_tweets(search, lang="en", result_type=result, count=1)["statuses"][0]
    tweet_id = str(tweet["id"])

    # Like the Tweet and return its URL
    api.create_favorite(tweet_id)
    tweet_url = "https://twitter.com/i/web/status/" + tweet_id
    return tweet_url