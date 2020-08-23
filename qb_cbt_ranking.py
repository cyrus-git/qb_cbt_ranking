from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

DRIVER_PATH = ''    # ブラウザのドライバーのpath:str
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')


def main():
    html = get_html()

    soup = BeautifulSoup(html, 'html.parser')
    total_html = str(
        soup.select('#app > div.wrapper > div:nth-child(2) > div > div.leftContents > section:nth-child(2) > '
                    'div > div.graph-ranking-result.style-graphRankingResult > div > div > svg > g.graphData'))\
                    .replace('[', '').replace(']', '')
    day_html = str(
        soup.select('#app > div.wrapper > div:nth-child(2) > div > div.leftContents > section:nth-child(5) > div >'
                    ' div.graph-common-plot-count.style-graphWrapper > svg > g.graphData'))\
                    .replace('[', '').replace(']', '')

    get_total_rank(total_html)
    get_daily_rank(day_html)


def get_html():
    def access_url(url):
        driver.get(url)

    def click(selector):
        element = driver.find_element_by_css_selector(selector)
        element.click()

    def type_text(selector, text):
        element = driver.find_element_by_css_selector(selector)
        element.send_keys(text)

    # CSS selectors
    login_form_button = '#header > div > div.r-cont > div.guest-items.only-pc > a:nth-child(2)'
    email_form = '#mauth-title > div > input'
    pass_form = '#mauth-popup-content > div > div > form > div:nth-child(2) > div > input'
    login_button = '#mauth-popup-content > div > div > form > div.cmn-button-1-wrap-1 > input'

    print('Getting information...')

    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    driver.implicitly_wait(5)

    access_url("https://medilink-study.com/")
    click(login_form_button)
    type_text(email_form, '')   # アカウントのemailアドレス:str
    type_text(pass_form, '')    # アカウントのパスワード:str
    click(login_button)
    time.sleep(7)
    access_url('https://cbt.medilink-study.com/#/Record')
    time.sleep(3)
    html = driver.page_source
    return html


def get_total_rank(html):
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find_all("circle")

    # get my x and y
    my_x = 0
    my_y = 0
    for i in p:
        s = str(i)
        if 'class="myData"' in s:
            t = s.split()
            for u in t:
                if u.startswith('cx="'):
                    u = u.replace('cx=', '').replace('"', '')
                    my_x = float(u)
                if u.startswith('cy="'):
                    u = u.replace('cy=', '').replace('"', '')
                    my_y = float(u)

    # get classmates' x and y
    x = []
    y = []
    for i in p:
        s = str(i)
        if 'class="myData"' in s:
            break
        t = s.split()
        for u in t:
            if u.startswith('cx="'):
                u = u.replace('cx=', '').replace('"', '')
                x.append(float(u))
            if u.startswith('cy="'):
                u = u.replace('cy=', '').replace('"', '')
                y.append(float(u))
    x = sorted(x, reverse=True)
    y = sorted(y, reverse=True)

    # get my rank
    my_x_rank = 1
    for i in range(len(x)):
        if my_x > x[i]:
            my_x_rank = i + 1
            break
    my_y_rank = 1
    for i in range(len(y)):
        if my_y > y[i]:
            my_y_rank = i + 1
            break

    print('あなたの演習数ランキングは ' + str(my_x_rank) + '位 です！')
    print('あなたの正解率ランキングは ' + str(my_y_rank) + '位 です！')


def get_daily_rank(html):
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find_all('circle')

    # get yesterday's x
    cx = []
    for i in p:
        s = str(i)
        t = s.split()
        for j in t:
            if j.startswith('cx="'):
                j = int(j.replace('cx="', '').replace('"', ''))
                if j not in cx:
                    cx.append(j)
    x_yesterday = max(cx)

    # get my y
    my_y = 0
    for i in p:
        s = str(i)
        if 'class="myData"' in s and 'cx="' + str(x_yesterday) + '"' in s:
            t = s.split()
            for u in t:
                if u.startswith('cy="'):
                    u = u.replace('cy=', '').replace('"', '')
                    my_y = float(u)

    # get classmates' y
    y = []
    for i in p:
        s = str(i)
        if 'cx="' + str(x_yesterday) + '"' in s:
            if 'class="myData"' in s:
                break
            t = s.split()
            for u in t:
                if u.startswith('cy="'):
                    u = u.replace('cy=', '').replace('"', '')
                    y.append(float(u))
    y = sorted(y, reverse=True)

    # get my rank
    my_y_rank = 1
    for i in range(len(y)):
        if my_y > y[i]:
            my_y_rank = i + 1
            break

    print('あなたの昨日の演習数ランキングは ' + str(my_y_rank) + '位 です！')


if __name__ == '__main__':
    main()
