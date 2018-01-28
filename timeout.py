import logging
import sys
import time

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader, select_autoescape

import constants
import mailer
from config import (LOG_LEVEL, OUTPUT_FILE, RECIPIENT, SEND_EMAIL,
                    SENDER_EMAIL, SENDER_PASSWORD)
from utils.dates import month_name_after_n_months

logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL)
logging.getLogger('urllib3').setLevel(LOG_LEVEL)

template_env = Environment(loader=PackageLoader('timeout', 'templates'), autoescape=select_autoescape(['html', 'xml']))


def monthly_url(index):
    return constants.MONTH_URL_BASE + month_name_after_n_months(index)


def get_entry_title(entry):
    try:
        return entry.find('h3').a.string.strip()
    except:
        return ''


def get_entry_description(entry):
    try:
        return ''.join(entry.find(class_='feature_item__annotation--truncated').strings).strip()
    except:
        import pdb; pdb.set_trace()
        return ''


def parse_entry(entry):
    title = get_entry_title(entry)
    description = get_entry_description(entry)

    return title, description


def format_entry_items(title, description):
    """
    Returns formatted HTML for title and description
    """
    if not title:
        logging.debug(u'Unable to format title \'{}\' and description \'{}\''.format(title, description))
        return ''

    entry_content = ''
    query = u'{} London'.format(title)
    query = query.replace(' ', '+')
    search_link = constants.SEARCH_URL + query

    title_template = template_env.get_template(constants.TITLE_TEMPLATE)
    entry_content += title_template.render(title=title, search_link=search_link)

    if description:
        description_template = template_env.get_template(constants.DESCRIPTION_TEMPLATE)
        entry_content += description_template.render(description=description)

    return entry_content


def parse_timeout_page(content):
    soup = BeautifulSoup(content, "html.parser")
    entries = soup.find_all(class_="feature-item__content")

    return (
        format_entry_items(*parse_entry(entry))
        for entry in entries
    )


def extract_content_from_timeout_url(section, url):
    logging.info('Processing {}'.format(section))

    response = requests.get(url)
    response.encoding = 'utf-8'
    content = response.text

    parsed_content = ''.join(parse_timeout_page(content))
    section_template = template_env.get_template(constants.SECTION_TEMPLATE)

    return section_template.render(section=section, content=parsed_content)


if __name__ == '__main__':
    content = ''

    for section, url in [
        ('This Friday', constants.FRIDAY),
        ('This Saturday', constants.SATURDAY),
        ('This Sunday', constants.SUNDAY),
        ('This month', monthly_url(0)),
        ('Next month', monthly_url(1)),
    ]:
        logging.debug('Processing ' + section)
        content += extract_content_from_timeout_url(section, url)

    template = template_env.get_template(constants.EMAIL_TEMPLATE)
    email_content = template.render(content=content)

    try:
        if SEND_EMAIL:
            logging.info('Sending email to {}'.format(RECIPIENT))

            mailer.send_email(
                user=SENDER_EMAIL,
                pwd=SENDER_PASSWORD,
                recipient=RECIPIENT,
                subject='Timout Events - {}'.format(time.strftime('%d/%m/%Y')),
                body=email_content,
            )

            logging.debug('Email sent')

    finally:
        with open(OUTPUT_FILE, 'w') as f:
            f.write(email_content.encode('utf-8'))
            logging.debug('Wrote output to {}'.format(OUTPUT_FILE))
