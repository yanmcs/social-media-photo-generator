# MY scripts
import scraper
import imagebuilder
# Everything else
from flask import Flask
from flask_restful import reqparse
import os

print('Starting Flask...')

app = Flask(__name__)

browser = scraper.Browser()
driver = browser.new_driver()
scrape_session = browser.scrape_session()

@app.route("/")
def index():
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('url', required=True)  # add arguments
    args = parser.parse_args()  # parse arguments to dictionary
    if args['url']:
        url = args['url']  # set variable for url
    else:
        return 'we need a url', 406

    html_scrapped_page = browser.get_html_using_request(url, scrape_session)  #  trying to scrape using requests
    if html_scrapped_page[1] != 200:  #  if not possible we try to use chromedriver to scrape page
        print('Bloqueado')
        html_scrapped_page = browser.get_html_using_chrome(url,driver)

    info = browser.html_to_json(html_scrapped_page[0])
    print(info)

    image = info['image']
    category = info['category']
    title = info['title']
    logo = info['logo']
    branding_text = info['branding-text'].upper()

    image = imagebuilder.social_image_builder(image, category, title, logo, branding_text, border=40)

    # Display edited image on screen using flask restful
    return image.tobytes(),200,{'Content-Type': 'image/jpeg'}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
