#важный комментарий - код писался вместе с Максом Кимом (3 группа)

import re
import os
import urllib.request

#создаем таблицу .csv
def make_csv():
    if not os.path.exists("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/"):
        os.makedirs("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/")
    with open("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/metadata.csv", "w", encoding="utf-8") as f:
        f.write(
            "path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n")


def add_csv(date, name, url, number):
    with open("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/metadata.csv", "a", encoding="utf-8") as f:
        f.write("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/Clean_Papers/2017/" + number + "/\t\t\t\t" + name[
                                                                                         7:-8] + "\t" + date + "\tпублицистика\t\t\t\t\tнейтральный\tн-возраст\tн-уровень\tгородская\t" + url + "\tВперед\t\t" + date[
                                                                                                                                                                                                                 :-4] + "\tгазета\tРоссия\tУльяновская область\tru\n")

#регулярное выражение для поиска даты
def find_date(page):
    return str((re.search("\d\d\d\d-\d\d-\d\d", page)).group(0))


def find_name(page):
    return str((re.search("<title>.+</title>", page)).group(0))


def write_page(page, name, date, url, number):
    path = "/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/Clean_Papers/2018/" + number + "/"
    path_mystem_txt = "/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/Parsed_Papers_txt/2018/" + number + "/"
    path_mystem_xml = "/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/Parsed_Papers_xml/2018/" + number + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path_mystem_txt):
        os.makedirs(path_mystem_txt)
    if not os.path.exists(path_mystem_xml):
        os.makedirs(path_mystem_xml)
    with open(path + number + ".txt", "w", encoding="utf-8") as f:
        f.write("@au\tNoname\n")
        f.write("@ti\t")
        f.write(name[7:-8])
        f.write("\n")
        f.write("@da\t")
        f.write(date)
        f.write("\n")
        f.write("@url\t")
        f.write(url)
        f.write("\n")
        clean_page = clean_tags(page)
        f.write(clean_page)
        os.system(
            "/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/mystem" + " -cgid " + path + number + ".txt " + path_mystem_txt + number + ".txt")
        os.system(
            "/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/mystem" + " -cgid " + path + number + ".txt " + path_mystem_xml + number + ".xml")
    if not f.writable:
        print("Unable to get access to the end file.")


def write_raw_page(page, number):
    if not os.path.exists("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/Raw_Papers/2018/" + number + "/"):
        os.makedirs("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/Raw_Papers/2018/" + number + "/")
    with open("/Users/melnikovaarina/Desktop/CODING/ПРОЕКТ/PapersA/Raw_Papers/2018/" + number + "/" + number + ".html", "w",
              encoding="utf-8") as f:
        f.write(page)
    if not f.writable:
        print("Unable to get access to the end file.")

#отчистка от тегов
def clean_tags(html_content):
    regtag = re.compile('<.*?>', re.DOTALL)
    regscript = re.compile('<script>.*?</script>', re.DOTALL)
    regcomment = re.compile('<!--.*?-->', re.DOTALL)
    regspace = re.compile('  ', re.DOTALL)
    reglet = re.compile("&[a-z]+", re.DOTALL)
    html_content = regscript.sub("", html_content)
    html_content = regcomment.sub("", html_content)
    html_content = regtag.sub("", html_content)
    html_content = regspace.sub("", html_content)
    html_content = reglet.sub("", html_content)
    html_content = html_content.split("\n")
    while '' in html_content:
        html_content.remove('')
    return ''.join(html_content)


#скачиваем страницу
def download_page(pageurl):
    try:
        page = urllib.request.urlopen(pageurl)
        text = page.read().decode('utf-8')
        print('Успешно: ', pageurl)
        return text
    except:
        return 0


def find_pages():
    page_num = 1
    common_url = "http://sprostor.ru/?module=articles&action=view&id="
    for i in range(4000, 4297):
        page = download_page(common_url + str(i))
        if page != 0:
            date = find_date(page)
            title = find_name(page)
            url = common_url + str(i)
            add_csv(date, title, url, str(page_num))
            write_raw_page(page, str(page_num))
            write_page(page, title, date, url, str(page_num))
            page_num += 1


make_csv()
find_pages()
print("final")
