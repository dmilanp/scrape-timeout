from __future__ import absolute_import, unicode_literals

import calendar
import datetime


def month_from_number(i):
    return calendar.month_name[i]


def current_month_number():
    return datetime.datetime.now().month


def month_name_after_n_months(n):
    return month_from_number(current_month_number() + n)
