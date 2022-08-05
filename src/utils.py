from bs4 import BeautifulSoup

def convert_article(v):
    bs = BeautifulSoup(v, 'html.parser')
    if bs.iframe:
        urls = [iframe.get('src') for iframe in bs.find_all('iframe')]
        return bs.text + '\n' + '\n'.join(urls)
    text = bs.get_text(' ', strip=True).replace('\n', '')
    if bs.span is not None:
        title = bs.span.text
        text = text.replace(title, '').strip()
        text = f"{title}\n{text}"
    return text
