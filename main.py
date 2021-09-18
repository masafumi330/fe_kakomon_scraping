from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import os
import time
from urllib.parse import urljoin

start = 22
stop = 31
url_lists = []
for year in (range(start, stop+1)):
    url_lists.append(f"https://www.jitec.ipa.go.jp/1_04hanni_sukiru/mondai_kaitou_{1988+year}h{year}.html")


for url in url_lists:
    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")
    result = soup.select("a[href]")

    link_list = []
    for link in result:
        href = link.get("href")
        link_list.append(href)

    pdf_list = [temp for temp in link_list if temp.endswith('pdf')]

    fepdf_list = [temp for temp in pdf_list if '_fe_' in temp]

    abs_fepdf_list = []
    for relative in fepdf_list:
        temp_url = urljoin(url, relative)
        abs_fepdf_list.append(temp_url)

    filename_list = []
    for target in abs_fepdf_list:
        temp_list = target.split("/")
        filename_list.append(temp_list[len(temp_list)-1])

    target_dir = os.path.join(os.getcwd(), "pdf")
    if not "pdf" in os.listdir():
        os.mkdir("pdf")

    savepath_list = []
    for filename in filename_list:
        savepath_list.append(os.path.join(target_dir, filename))

    # do download!( time interval 2 seconds)
    for (pdflink, savepath) in zip(abs_fepdf_list, savepath_list):
        urllib.request.urlretrieve(pdflink, savepath)
        time.sleep(2)
