import imagebuilder
import scraper


if __name__ == '__main__':

    url = 'https://pacotebarato.com.br/resorts-all-inclusive-no-brasil'

    browser = scraper.Browser()
    driver = browser.new_driver(local=True)
    scrape_session = browser.scrape_session()
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
    # Display edited image
    image.show()
    # Save the edited image
    image.save("text_on_image.jpg", "JPEG", optimize=True)