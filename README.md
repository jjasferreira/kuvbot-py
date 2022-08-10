# <img alt="Logo" src="./misc/light_logo.png" width=26px> kuvbot-py

<a href="https://twitter.com/kuvbot"><img align="left" alt="Follow @kuvbot" src="https://dabuttonfactory.com/button.png?t=Follow+%40kuvbot&f=Open+Sans-Bold&ts=25&tc=fff&hp=35&vp=15&c=round&bgt=unicolored&bgc=1da1f2&be=1" height=26px></a>

<a href="https://twitter.com/intent/tweet?screen_name=kuvrep&ref_src=twsrc%5Etfw"><img alt="Tweet to @kuvrep" src="https://dabuttonfactory.com/button.png?t=Mention+%40kuvrep&f=Open+Sans-Bold&ts=25&tc=1da1f2&hp=35&vp=15&c=round&bgt=unicolored&bgc=fff&be=1" height=26px></a>

Kuv is a Twitter bot written in Python 3.10.5 that scrapes images from across the web, edits them, credits them to their author, tags them with a word and a corresponding confidence percentage using A.I. techniques, and finally tweets them.

<img src="misc/image.png" alt="Image" width="800"/>

It is currently using the [Unsplash](https://github.com/unsplash) API as an image source, the [Imagga](https://github.com/imagga) API for image recognition and the [Twitter](https://github.com/twitter) API for programmatic access to Twitter in advanced ways.

Image scraping is guaranteed by the [Requests](https://github.com/psf/requests) HTTP library. To edit them, the used module is [Pillow](https://github.com/python-pillow/Pillow), the Python Imaging Library fork. To easily access the Twitter API from Python, [Tweepy](https://github.com/tweepy/tweepy) has been used.

In order to keep consistency in this project, [black](https://github.com/psf/black) has been used as a code formatter for Python files.

If you'd like to contribute, feel free to open a pull request and if proven helpful, I will credit you! 😄
