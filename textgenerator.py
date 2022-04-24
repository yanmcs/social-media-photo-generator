import openai

# OpenAI API Key
openai.api_key = "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"

# Generate caption for social media image
def create_caption(topic):
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="Escreva sobre o assunto. Depois, cite o preço da promoção com uma chamada para ação. Não faça referências a marcas, sites, empresas ou cupons de descontos. Não insira títulos. Não insira regras no texto. Assunto: " + topic + ".\n\n",
    temperature=0.5,
    max_tokens=600,
    top_p=0.5,
    frequency_penalty=1,
    presence_penalty=1,
    best_of=3
    )
    text = response["choices"][0]["text"]
    return text

