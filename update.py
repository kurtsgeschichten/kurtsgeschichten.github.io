from urllib.request import urlopen
import requests
from readability import Document
from bs4 import BeautifulSoup
from googletrans import Translator

# ----- To produce output -------
from datetime import datetime
# -------------------------------

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main():
    url = "https://www.history.com/this-day-in-history"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # Extract title from full html file    
    title_en = None
    for header in soup.find_all('h1'):
        if '<h1 class="m-detail-header--title">' in repr(header):
            title_en = header.string

    # Extract year if stored in dd tag        
    year = ''
    for dd in soup.find_all('dd'):
        if RepresentsInt(dd.string):
            year = f'{int(dd.string)} | '

    # ----- Create document summary ------
    response = requests.get(url)
    doc = Document(response.text)   # readability removes all but the main story
    # Pass document summary to 
    soup_sum = BeautifulSoup(doc.summary(), features="html.parser")
    # Remove all elements except text stored in paragraphs
    for script in soup_sum(["script", "style"]):
        script.extract()    # rip it out
    for m in soup_sum.find_all('a'):
        m.replaceWithChildren()
    for m in soup_sum.find_all('em'):
        m.replaceWithChildren()
    for strong in soup_sum.find_all('strong'):
        strong.extract()

    # Get story
    sentences = []
    for parag in soup_sum.body.find_all('p'):
        chunks = (phrase.strip() for line in parag for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        if text!='':
            sentences.append(text)

    # ----- Translate story -------
    translator = Translator()
    sentences_de = [translator.translate(sent_i, src='en', dest='de').text 
                    for sent_i in sentences]
    # Put sentence into paragraph mode
    text_de = ''
    for satz in sentences_de:
        text_de += '<p>' + satz + '</p>'

    # ----- Save in html file ------
    title_de = translator.translate(title_en, src='en', dest='de').text
    html_text = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Kurts Geschichten</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="style.css">

    </head>
    <body>
    <script src="datetime.js"></script>
    <div class="header">
      <h1>W&#229s w&#229r denn d&#229 los?</h1>
      <p>Kurts Geschichte zum <span id="datetime"></span></p>
    </div>

    <script src="datetime.js"></script>

    <div class="row">
      <div class="column side">
      </div>

      <div class="column middle">
        <h2>{year}{title_de}</h2>
        {text_de}
      </div>

      <div class="column side">
      </div>
    </div>

    </body>
    </html>
    """

    # save in file
    Html_file= open("index.html","w")
    Html_file.write(html_text)
    Html_file.close()

    with open("/home/sebastian/Desktop/updated_htmlfile.txt", "w") as text_file:
        text_file.write(f"Updated on {datetime.today().strftime('%A')}")


if __name__=='__main__':
    main()

