from bs4 import BeautifulSoup
import requests, re

urls = (("https://www.radio1.cz/hitparada-radia-1", "hr1", "Hitparáda Rádia 1"), ("https://www.radio1.cz/hitparada-velka-sedma", "vs", "Velká Sedma"))

def parse_data(soup, file):
    names= soup.find(class_="h4")
    position = names.get_text()
    names = names.next_sibling
    band = names.a.get_text()
    song = re.search("(?<=\n\n).*", names.get_text()).group()
    #print(f"{position}. {interpret}: {song}")
    names = names.next_sibling
    #print(type(names.get_text()))
    #print(bytes(str(names.get_text()), "utf-8"))
    album = re.search("\n(.*?)(\n|$)", names.get_text()).group(1)
    #print(album)
    names = names.next_sibling
    weeks = re.search("(sto|nka)\n(\d\d?) ", names.get_text())
    week_word = re.search("(t.d..)", names.get_text())
    if weeks:
        weeks = f" - {weeks.group(2)} {week_word.group(1)}"
        position += "."
    else:
        weeks = ""
        position += " -"
    #print("Weeks:", weeks)
    #print()
    printable = f"{position:3} {band}: {song} ({album}){weeks}\n"
    file.write(printable)
    print(printable, end="")

for url, filename_prefix, chart_name in urls:
    print(f"Sending request for {chart_name}")
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    date = soup.select(".container .md-col-8.lg-col-8")[0]
    #print(bytes(date.get_text(), "utf-8"))
    parsed_date = re.search("\n(\d\d)/(\d\d)", date.get_text())
    month = parsed_date.group(2)
    day = parsed_date.group(1)
    
    hit_list = soup.find(id="hitparada-list")

    filename = f"{filename_prefix}-{month}-{day}.txt"

    with open(filename, "w", encoding="utf-8") as infile:
        for pos in hit_list.find_all(class_="chart-song"):
            parse_data(pos, infile)