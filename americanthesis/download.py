from bs4 import BeautifulSoup
import requests


URL = 'https://suo.seas.harvard.edu/suo-publications'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

years = soup.find_all('section')

papers = []
for year in years:
    articles = year.find_all('article')
    for article in articles:
        authors = article.find_all('span', class_='biblio-authors')[0].decode_contents()
        id = authors.split(',')[0].split()[0].strip()
        authors = authors.replace(id, '').strip()
        if authors.startswith(', '):
            authors = authors[2:]
        elif authors.startswith('and '):
            authors = authors[4:]
        authors = authors.replace('  ', ' ')

        title_block = article.find_all('a')[0]
        url = title_block['href']
        title = title_block.decode_contents()

        inner = article.find_all('div', class_='node-content')[0].decode_contents()
        journal = inner.split('span')[-3].strip('><."” ')
        print(id, authors)

        pdf = requests.get(url)
        with open(f'{id.zfill(3)}.pdf', 'wb') as f:
            f.write(pdf.content)
        
        papers.append(dict(
            id=id,
            title=title,
            authors=authors,
            url=url,
            journal=journal,
        ))
