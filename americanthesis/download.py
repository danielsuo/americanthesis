import sys

from absl import flags
from bs4 import BeautifulSoup
import pandas as pd
import requests


flags.DEFINE_boolean('save_pdf', False, 'Save PDF?')


flags.FLAGS(sys.argv)

URL = 'https://suo.seas.harvard.edu/suo-publications'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

sections = soup.find_all('section')

papers = []
for section in sections:
    articles = section.find_all('article')
    year = section.find_all('h2')[0].decode_contents()

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

        id = id.zfill(3)
        if flags.FLAGS.save_pdf:
            pdf = requests.get(url)
            with open(f'{id.zfill(3)}.pdf', 'wb') as f:
                f.write(pdf.content)
        
        papers.append(dict(
            id=id,
            year=year,
            title=title,
            authors=authors,
            url=url,
            journal=journal,
        ))


df = pd.DataFrame.from_records(papers)
df = df.iloc[::-1]

year = None
for _, row in df.iterrows():
    if year != row.year:
        year = row.year
        if '.' in year:
            year = year.strip().split('.')[0]
        with open(f'{year}.tex', 'a') as f:
            f.write(f'\part{{{year}}}\n')
    print(f'{year}: {row.id}')
    with open(f'{year}.tex', 'a') as f:
        f.write(f'\\pdf{{{row.id}}}{{{row.title}}}\n')
