
import requests
from bs4 import BeautifulSoup as bs
import pdfx
import os
import glob
from colorama import Fore as F

home_folder = os.path.expanduser('~')
list_of_files = glob.glob(f'{home_folder}/Downloads/*')
latest_file = max(list_of_files, key=os.path.getctime)

pdf = pdfx.PDFx(latest_file)

print()

for url in pdf.get_references_as_dict()['url']:
    with requests.Session() as s:
        r = s.get(url)
        soup = bs(r.content, 'html.parser')

        print(F.YELLOW + "Answers for", soup.find('h2').text.strip())
        print(F.RESET + url)

        lesson = url.split("/")[-1].split("?")[0]
        for div in soup.find_all('div', class_='lesson__video-title'):
            if div.next_element['href'].split("/")[-1] == lesson:
                question = div.findNext('div').next_element['href']

        question_url = f"https://mru.org{question}"

        r = s.get(question_url)

        soup = bs(r.content, 'html.parser')

        form = soup.find('form', class_='webform-client-form').next_element

        for question in form.find_all('input', class_="form-radio"):
            if question['value'] == "r":
                print(F.LIGHTGREEN_EX + question.parent.text.strip())

    print(F.RESET)
    
