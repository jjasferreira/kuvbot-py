from utils import *

def main():

    api = authenticate()
    ids = load_state()

    [id, author] = get_random_image_picsum(ids)
    url = "https://picsum.photos/id/" + str(id) + "/1500"
    [tag, confidence] = tag_url_image_imagga(url)

    url += "?grayscale"
    image_path = download_image(url, str(id))
    edit_path = edit_image(image_path, "Kuv")

    alt = "Author: " + author + "\nTag: " + tag + "\nConfidence: " + confidence
    tweet_media_metadata(api, edit_path, alt)
    print("[TWEET]:\n" + "Image ID: " + str(id) + "\n" + alt + "\n==========")
    save_state(ids)


if __name__ == "__main__":

    main()
