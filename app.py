# MY scripts
from io import BytesIO
import scraper
import image_builder
# Everything else
from flask import Flask, request, send_file, render_template
import traceback

print('Starting Flask...')

app = Flask(__name__, static_url_path='/static')

browser = scraper.Browser()
scrape_session = browser.scrape_session()

@app.route("/")
def index():
    global scrape_session
    if 'url' in request.args:
        try:
            url = request.args.get('url')
            # enconde special caracters in url
            url = url.replace('%3A', ':')
            url = url.replace('%2F', '/')
            url = url.replace('%3F', '?')
            url = url.replace('%3D', '=')
            url = url.replace('%26', '&')
            border = request.args.get('border')
            height = request.args.get('height')
            color = request.args.get('color')
            if border is None:
                border = 40
            else:
                border = int(border)
            if height is None:
                height = 1080
            else:
                height = int(height)
            if color is None:
                color = '000000'

            html_scrapped_page = browser.get_html_using_request(url, scrape_session)  #  trying to scrape using requests
            info = browser.html_to_json(html_scrapped_page[0])
            print(info)
            image = info['image']
            category = info['category']
            title = info['title']
            logo = info['logo']
            branding_text = info['branding-text'].upper()
            image = image_builder.social_image_builder(image, category, title, logo, branding_text, border=border, height=height, color=color)
            # Return image to browser
            img_io = BytesIO()
            # Convert image to JPEG
            image.convert('RGB').save(img_io, 'JPEG', quality=80)
            img_io.seek(0)
            # Return image to browser on heroku
            return send_file(img_io, mimetype='image/jpeg'), 200, {'Content-Type': 'image/jpeg'}
        except Exception as e:
            # Check if debug is set on parameter
            if 'debug' in request.args:
                error = traceback.format_exc()
                return 'error: e\n\n' + str(error), 200, {'Content-Type': 'text/plain'}
            else:
                # Show message to user and link to go back to the website
                return 'Deu ruim :(<br><br><a href="/">Didnt work Back to generator</a>', 500, {'Content-Type': 'text/html'}
    else:
        # flask render form.html
        return render_template('form.html'), 200, {'Content-Type': 'text/html'}

if __name__ == "__main__":
    app.run(port=6001)
