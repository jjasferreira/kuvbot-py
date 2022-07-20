from utils import *

def main():

    api = authenticate()

    hashtag = "#photography"
    tweet_url = like_tweet_hashtag(api, hashtag, "recent")
    print("[LIKE]:\n" + "Hashtag: " + hashtag + "\nTweet URL: " + tweet_url + "\n==========")


if __name__ == "__main__":

    main()
