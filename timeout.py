import calendar
from collections import OrderedDict
import datetime
import urllib2

from bs4 import BeautifulSoup


FRIDAY = "http://www.timeout.com/london/things-to-do/things-to-do-in-london-on-a-friday"
SATURDAY = "http://www.timeout.com/london/things-to-do/things-to-do-in-london-on-a-saturday"
SUNDAY = "http://www.timeout.com/london/things-to-do/things-to-do-in-london-on-a-sunday"

def month_from_number(i):
    return calendar.month_name[i]

def current_month_number():
    return datetime.datetime.now().month

def get_month_urls():

    MONTH_URL_BASE = "http://www.timeout.com/london/things-to-do/london-events-in-"

    this_month_num = current_month_number()
    next_month_num = this_month_num + 1
    this_month = month_from_number(this_month_num).lower()
    next_month = month_from_number(next_month_num).lower()
    this_month_url = MONTH_URL_BASE + this_month
    next_month_url = MONTH_URL_BASE + next_month
    return (this_month_url, next_month_url)

def print_html(text, tag):
    """Print text inside tags"""
    print "<{}>{}</{}>".format(tag, text, tag)

this_month, next_month = get_month_urls()

times = OrderedDict()
times['This Friday'] = FRIDAY
times['This Saturday'] = SATURDAY
times['This Sunday'] = SUNDAY
times['This month'] = this_month
times['Next month'] = next_month


for time, url in times.iteritems():

    response = urllib2.urlopen(url)
    html = response.read()

    soup = BeautifulSoup(html, "html.parser")

    print "\n\n\n\n\n{}\n\n".format(print_html(time, 'h1'))

    for entry in soup.find_all(class_="feature-item__content"):
        try:
            title = 4 * '&nbsp;'+ entry.find('h3').a.string.strip()
            if title:
                print_html(title, 'h3')
        except:
            pass
        try:
            description = 14 * '&nbsp;' + entry.find(class_='feature_item__annotation--truncated').string.strip()
            if description:
                print_html(description, 'p')
        except:
            pass
        print 1 * "</br>"
