import image_builder
import scraper
import textgenerator


if __name__ == '__main__':

    info = {'article-url': 'https://pacotebarato.com.br/noticias/aproveite-as-promocoes-de-viagem-com-carro-voo-e-hotel-inclusos/', 'title': 'Aproveite as promoções de viagem com carro, voo e hotel inclusos', 'image': 'https://s3.amazonaws.com/legado-prod/prod/ofertas/imagens/2021/12/10/12/00/1_shutterstock_1363425368.jpg', 'category': 'Notícias', 'branding-text': 'Pacote Barato', 'logo': 'https://pacotebarato.com.br/wp-content/uploads/2022/02/cropped-PB-1-1-32x32.png'}

    image = info['image']
    category = info['category']
    title = info['title']
    logo = info['logo']
    branding_text = info['branding-text'].upper()

    image = image_builder.social_image_builder(image, category, title, logo, branding_text, border=40, height=1920)
    # Display edited image
    image.show()
    # Save the edited image
    image.save("social_media_image.png")
    # Generate caption for social post
    #text = textgenerator.create_caption(title)
    #print(text)
    