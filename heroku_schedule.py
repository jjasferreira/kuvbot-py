# Python modules
from time import sleep

# Import actions to conduct
from actions import *


def main():
    """Runs every 10 minutes."""

    # If there is a file with a counter, load it; otherwise, initialize the counter
    if not path.exists(JSON_DIR + "/heroku_schedule.json"):
        times = -1
    else:
        file = open(JSON_DIR + "/heroku_schedule.json", "r")
        times = load(file)
        file.close()

    # Account for the new 10 minutes that have passed
    times += 1

    # 01. Every 3 hours, tweets an image
    if times % 18 == 0:
        action_tweet_image_picsum(1000)

    # 02. Every minute, likes a tweet containing certain word(s)
    if times % 1 == 0:
        for i in range(0, 10):
            action_like_tweet_contains("#photography")
            sleep(60)

    # (Over)write counter variable to file
    file = open(JSON_DIR + "/heroku_schedule.json", "w")
    dump(times, file)
    file.close()


if __name__ == "__main__":
    main()
