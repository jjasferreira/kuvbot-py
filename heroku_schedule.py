from actions import *

# Runs every 10 minutes
def main():

    # If there is a file with a counter, load it; otherwise, initialize the counter
    if not path.exists(JSON_DIR + "/heroku_schedule.json"):
        times = -1
    else:
        file = open(JSON_DIR + "/heroku_schedule.json", "r")
        times = load(file)
        file.close()

    # Account for the new 10 minutes that have passed
    times += 1

    # 01. Every 10 minutes, likes a tweet containing certain word(s)
    if times % 1 == 0:
        action_like_tweet_contains("#photography")
    
    # 02. Every 3 hours, tweets an image
    if times % 18 == 0:
        action_tweet_image_picsum(1000)

    # (Over)write counter variable to file
    file = open(JSON_DIR + "/heroku_schedule.json", "w")
    dump(times, file)
    file.close()


if __name__ == "__main__":
    main()