from json import dump, load
from requests import get


def tag_url_image(url: str):
    """Attempts to give different tags to the image contained in the given url
    with corresponding confidence rates. Returns the most accurate answer amongst all.
    """

    # Open local credentials file
    file = open("keys.json", "r")
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


if __name__ == "__main__":

    # Default test
    [tag, con] = tag_url_image("https://picsum.photos/id/0/1500")
    print("Tag: " + tag + "\nConfidence: " + con)
