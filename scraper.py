from selenium import webdriver
import os
from bs4 import BeautifulSoup as Bs
import html as ht
import cfscrape


class Browser:

    # Function to check if element is a link or not
    def check_if_element_is_link(self, element):
        element_size = len(element.get_text())
        if element.find('a'):
            link_size = len(element.find('a').get_text())
            if link_size > 0 and element_size / link_size < 1.5:
                return True
            else:
                return False
        else:
            return False

    # Creating chromedriver to scrape HTML if we are being blocked on requests
    # Set local=True for local testing
    def new_driver(self,local=False):
        chrome_options = webdriver.ChromeOptions()
        if not local:
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")  # disable for local run, enable to commit
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")

        # For ChromeDriver version 79.0.3945.16 or over
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # Set user agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

        if local:
            driver = webdriver.Chrome(chrome_options=chrome_options) # enable for local run, disable to commit
        else:
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), \
                                  chrome_options=chrome_options)  # disable for local run, enable to commit
        
        return driver

    # Function to scrape URL and return HTML to be souped
    def get_html_using_chrome(self, url, driver):
        driver.get(url)
        html = driver.page_source
        # for debug
        # print(html)
        return html, 'chromedriver'

    # Funciton to close browser to save memory
    def close(self):
        self.driver.close()
        self.driver.quit()

    # Function to create the JSON we will use to create the image
    # {"article-url": "https://www.com.br/article",
    # "title": "Lorem Ipsum",
    # "image": "https://www.com.br/image.jpg",
    # "category": "Saúde",
    # "branding-text": "Pacote Barato",
    # "favicon": "https://.jpg"
    # }
    def html_to_json(self, html):

        # Starting json
        info = {
                "article-url": "",
                "title": "",
                "image": "",
                "category": "",
                "branding-text": "",
                "logo": ""
                }

        soup = Bs(html, 'html.parser')  # get soup

        # Finding the div with the content
        the_content = self.find_div_with_most_paragraphs(soup)

        # Let's grab all infos we need from the html souped and start building the json content
        # Get url from canonical tag
        if soup.find('link', attrs={"rel": "canonical"}):
            info["article-url"] = soup.find('link', attrs={"rel": "canonical"})['href']
        else:
            info["article-url"] = ''
            # return "Erro: sem canonical tag no site"

        # Get favicon
        if soup.find('link', attrs={"rel": "icon"}):
            info["logo"] = soup.find('link', attrs={"rel": "icon"})['href']
        else:
            info["logo"] = ''
            #return 'Erro: site sem favicon'

        # Get logo
        if info['logo'] == '':
            try:
                logo = soup.find('meta', attrs={"name": "msapplication-TileImage"})['content']
            except:
                try:
                    logo = soup.find('link', attrs={"rel": "apple-touch-icon-precomposed"})['href']
                except:
                    try:
                        logo = soup.find('link', attrs={"rel": "icon"})['href']
                    except:
                        logo = ''
                        #return 'Erro: não encontrei o logotipo'
            info["logo"] = logo  

        # Get website name
        try:
            website_name = soup.find('meta', attrs={"property": "og:site_name"})['content']
        except:
            #return 'Erro: não existe a meta tag que define o nome do site'
            website_name = ''
            pass
        info["branding-text"] = website_name

        # Get post category
        if soup.find('meta', attrs={"property": "article:section"}):
            info["category"] = soup.find('meta', attrs={"property": "article:section"})['content']     

        # Get H1
        h1 = soup.find_all('h1')
        info["title"] = h1[-1].get_text()

        # Get cover image or whatever is possible
        if the_content.select('img'):
            try:
                if 'http' in the_content.select('img')[0]['src'] and 'data:image' not in the_content.select('img')[0]['src']:
                    info["image"] = the_content.select('img')[0]['src']
            except:
                if 'http' in the_content.select('img')[0]['data-src'] and 'data:image' not in the_content.select('img')[0]['data-src']:
                    info["image"] = the_content.select('img')[0]['data-src']
        if len(str(info["image"])) < 10:
            if soup.find('meta', attrs={"property": "og:image"}):      
                info["image"] = soup.find('meta', attrs={"property": "og:image"})['content']
            elif soup.find('meta', attrs={"name": "twitter:image"}):
                info["image"] = soup.find('meta', attrs={"name": "twitter:image"})['content']
            else:
                return 'Erro: não existe a tag de imagem destacada, tente inserir uma ou envie outra url de outro artigo'

        return info

    def find_div_with_most_paragraphs(self,soup):
        div_with_most_paragraphs = ''
        divs = soup.find_all('div')
        for div in divs:
            if div.find_all('p'):
                number_of_paragraphs = len(div.find_all('p'))
                if number_of_paragraphs > len(div_with_most_paragraphs):
                    div_with_most_paragraphs = div
        return div_with_most_paragraphs

    # If you are not being blocked, you can just use requests
    def get_html_using_request(self, url, cfscrape_session):
        
        r = cfscrape_session.get(url)
        r.encoding = 'UTF-8'
        html = ht.unescape(r.text)
        # FOR DEBUG
        # print(html)

        return html, r.status_code

    def scrape_session(self):
        session = cfscrape.create_scraper()
        return session