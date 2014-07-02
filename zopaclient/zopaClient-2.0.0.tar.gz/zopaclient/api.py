# -*- coding: utf-8 -*-

#  Copyright 2014 Jean-Francois Paris
#
# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, absolute_import, division

import requests
from lxml import html
from decimal import Decimal
from re import sub
import time
import random
from collections import namedtuple
from .log import logger

zopa_url = "https://secure2.zopa.com/login"
provision_fund_url = "https://www.zopa.com/lending/peer-to-peer-experts"

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0"

SafeGuardFund = namedtuple('SafeGuardFund', 'amount, estimated_default, coverage')



def convert_to_decimal(num):
    """ convert strings to decimal.Decimal() objects, taking into account zopa formatting
    conventions

    :param num: a number as per formatted by rate setter website
    :return: decimal.Decimal() representation of num
    """
    return Decimal(sub(r'[^\d\-.]', '', num.strip('£ \n\r')))


class ZopaException(Exception):
    pass

class ZopaExceptionSiteChanged(ZopaException):
    pass


class ZopaClient(object):

    def __init__(self, email, password, security_questions, natural=True):
        """Initialise the Zopa client

        The init method takes a dict that contains the answers to the security questions used by Zopa
        during the authentication process. The key of the dictionary are as follow

        _security_questions  = {
            "FIRST_SCHOOL": "xxx",
            "LAST_SCHOOL": "xxx",
            "PLACE_OF_BIRTH": "xxx"
        }

        :param str email: email address for the account
        :param str password: password for the account
        :param dict security_questions: dict mapping the three expected security questions to their answers
        :param boolean natural: when true, the object behave naturally and pauses between requests
        """
        self._email = email
        self._password = password
        self._security_questions = security_questions
        self._natural = natural
        self._connected = False
        self._dashboard_url = None

        # create an http session
        self._init_session()

        # if in natural mode, we initiate the random number generator
        if self._natural:
            random.seed()

        logger.debug("Created client for Zopa")

    def _get_http_helper(self):
        """Returns a helper function that allows lxml form processor to post using requests"""

        def helper(method, url, value):
            if not url:
                logger.error("Cannot submit request. No URL provided")
                raise ValueError("cannot submit, no URL provided")
            if method == 'GET':
                logger.debug("GET request URL: %s, Value: %s", url, value)
                return self._session.get(url, value)
            else:
                logger.debug("POST request URL: %s, Value: %s", url, value)
                return self._session.post(url, value)

        return helper

    def _sleep_if_needed(self):
        """Sleep for a random amount of time between 2 and 10 seconds

        This method is used to make our behaviour look more human and avoid overloading Zopa's server
        """
        if self._natural:
            #if in natural mode we sleep for some time
            time.sleep(random.randint(2, 10))

    def _extract_url(self, tree):
        """Extract and save the main urls

        This method shall be called once after connection in order to
        avoid having to seek for the URL at a later stage
        """
        # noinspection PyAttributeOutsideInit
        self._exit_url = tree.cssselect(".signout a")[0].get("href")
        self._loanbook_url = tree.cssselect("#lending_my_loan_book a")[0].get("href")
        self._account_url = tree.cssselect("#lending_account a")[0].get("href")
        self._statement_url = "https://secure2.zopa.com/lending/statements"

    def _init_session(self):
        """Create a new http client
        """
        # initiate the browser
        self._session = requests.Session()
        self._session.headers = {'User-agent': user_agent}
        self._session.verify = True

    def connect(self):
        """Connect the client from Zopa"""
        # create a new http session each time we attempt a new connection
        self._init_session()

        # pull zopaclient signup page
        logger.debug("GET request URL: %s", zopa_url)
        page = self._session.get(zopa_url)
        self._sleep_if_needed()

        # fill the signup form
        tree = html.fromstring(page.text, base_url=page.url)
        form = tree.forms[0]
        form.fields["email"] = self._email
        form.fields["password"] = self._password
        logger.debug("Submit form")
        page = html.submit_form(form, open_http=self._get_http_helper())
        self._sleep_if_needed()

        # check if we have landed on the secret verification page
        url = page.url
        if not "login/confirm" in url:
            raise ZopaExceptionSiteChanged("Unexpected page")

        # fill the idea verification form
        tree = html.fromstring(page.text, base_url=page.url)
        form = tree.forms[0]
        form.fields["answer"] = self._security_questions[form.fields["question"]]
        logger.debug("Submit form")
        page = html.submit_form(form, open_http=self._get_http_helper())

        self._sleep_if_needed()

        # check if we have landed on the dashboard page
        url = page.url
        if not "/dashboard" in url:
            raise ZopaExceptionSiteChanged("Unexpected page")()

        self._connected = True
        self._dashboard_url = url
        tree = html.fromstring(page.text, base_url=page.url)
        tree.make_links_absolute(page.url)
        self._extract_url(tree)

    def disconnect(self):
        """Disconnect the client from Zopa"""
        # call the logout url
        logger.debug("GET request URL: %s", self._exit_url)
        page = self._session.get(self._exit_url)
        url = page.url
        if not "/signed_out" in url:
            raise Exception("Failed to sign out")

        self._connected = False

    def get_loan_book(self):
        """Download and return the full loan book

        :return: loan book in csv format
        :rtype: str
        """
        logger.debug("GET request URL: %s", self._loanbook_url)
        page = self._session.get(self._loanbook_url)
        self._sleep_if_needed()

        tree = html.fromstring(page.text, base_url=page.url)
        form = tree.forms[0]

        # submit the two following values through the extra_values parameters
        # as they are not part of the initial form
        values = {"_template$MainControl$Content$MyLoanBookControl$btnDownloadCSV.x": "132",
                  "_template$MainControl$Content$MyLoanBookControl$btnDownloadCSV.y": "7"}

        logger.debug("Submit form")
        page = html.submit_form(form, extra_values=values, open_http=self._get_http_helper())
        self._sleep_if_needed()
        return page.text

    def get_statement(self, year, month):
        """Download and return the monthly statement for a given period

        :param int year: year for which the statement is required
        :param int month: month within the year for which the statement is required
        :return: statement in csv format
        :rtype: str
        """
        logger.debug("GET request URL: %s", self._statement_url)
        page = self._session.get(self._statement_url)
        self._sleep_if_needed()

        tree = html.fromstring(page.text, base_url=page.url)
        form = tree.forms[0]

        form.fields["date[month]"] = str(month) if type(month) == int else month
        form.fields["date[year]"] = str(year) if type(year) == int else year

        logger.debug("Submit form")
        page = html.submit_form(form, open_http=self._get_http_helper())
        self._sleep_if_needed()
        return page.text


    def get_account_summary(self):
        """Get the account summary

        :return: summary of current account
        :rtype: dict
        """
        logger.debug("GET request URL: %s", self._account_url)
        page = self._session.get(self._account_url)
        self._sleep_if_needed()

        results = {}

        tree = html.fromstring(page.text, base_url=page.url)

        summary_items = tree.cssselect(".result .important strong")

        ZopaAccount = namedtuple('ZopaAccount', """total_earnings, zopa_total, total_paid_in, total_paid_out, not_offered, fees_not_deducted
        offered, processing, processing_nb_loans, lent_out, lent_out_nb_loans, late_payment, late_payment_nb_loans, bad_debt, bad_debt_nb_loans,
        all_time_borrower_interest, all_time_holding_account_interest, all_time_bonuses, all_time_tell_a_friend, all_time_rapid_return_interest,
        all_time_rate_promise, all_time_total_lender_fees, all_time_bad_debt, all_time_lent_out, all_time_capital_returned""")

        total_earnings = convert_to_decimal(summary_items[0].text)
        zopa_total = convert_to_decimal(summary_items[1].text)
        total_paid_in = convert_to_decimal(summary_items[2].text)
        total_paid_out = convert_to_decimal(summary_items[3].text)

        summary_items = tree.cssselect(".lending-offers-summary td.number")
        not_offered = convert_to_decimal(summary_items[0].text)
        fees_not_deducted = convert_to_decimal(summary_items[2].text)
        offered = convert_to_decimal(summary_items[4].text)
        processing = convert_to_decimal(summary_items[6].text)
        processing_nb_loans = convert_to_decimal(summary_items[7].text)
        lent_out = convert_to_decimal(summary_items[8].text)
        lent_out_nb_loans = convert_to_decimal(summary_items[9].text)
        late_payment = convert_to_decimal(summary_items[10].text)
        late_payment_nb_loans= convert_to_decimal(summary_items[11].text)
        bad_debt = convert_to_decimal(summary_items[14].text)
        bad_debt_nb_loans = convert_to_decimal(summary_items[15].text)

        summary_items = tree.cssselect(".lending-offers-all-time-summary td.number")
        all_time_borrower_interest = convert_to_decimal(summary_items[0].text)
        all_time_holding_account_interest = convert_to_decimal(summary_items[1].text)
        all_time_bonuses = convert_to_decimal(summary_items[2].text)
        all_time_tell_a_friend = convert_to_decimal(summary_items[3].text)
        all_time_rapid_return_interest = convert_to_decimal(summary_items[4].text)
        all_time_rate_promise = convert_to_decimal(summary_items[5].text)
        all_time_total_lender_fees = convert_to_decimal(summary_items[6].text)
        all_time_bad_debt = convert_to_decimal(summary_items[7].text)
        all_time_lent_out = convert_to_decimal(summary_items[8].text)
        all_time_capital_returned = convert_to_decimal(summary_items[9].text)

        return ZopaAccount(total_earnings=total_earnings, zopa_total=zopa_total, total_paid_in=total_paid_in,
                           total_paid_out=total_paid_out, not_offered=not_offered, fees_not_deducted=fees_not_deducted,
                           offered=offered, processing=processing, processing_nb_loans=processing_nb_loans,
                           lent_out=lent_out, lent_out_nb_loans=lent_out_nb_loans,
                           late_payment=late_payment, late_payment_nb_loans=late_payment_nb_loans,
                           bad_debt=bad_debt, bad_debt_nb_loans=bad_debt_nb_loans,
                           all_time_borrower_interest=all_time_borrower_interest,
                           all_time_holding_account_interest=all_time_holding_account_interest,
                           all_time_bonuses=all_time_bonuses,
                           all_time_tell_a_friend = all_time_tell_a_friend, all_time_rapid_return_interest=all_time_rapid_return_interest,
                           all_time_rate_promise=all_time_rate_promise, all_time_total_lender_fees=all_time_total_lender_fees,
                           all_time_bad_debt=all_time_bad_debt, all_time_lent_out=all_time_lent_out,
                           all_time_capital_returned=all_time_capital_returned)

    def get_safeguard_fund(self):
        """ Get a summary of the amount in the safeguard fund

        This method does not require that the client is connected before you invoke it

        :return: namedtuple with the following keys:
           * amount: total amount in the safeguard fund
           * estimated_default: estimated default from outstanding loans
           * coverage: coverage ratio

        """
        logger.debug("GET request URL: %s", provision_fund_url)
        page = self._session.get(provision_fund_url)
        self._sleep_if_needed()
        tree = html.fromstring(page.text, base_url=page.url)

        td = tree.xpath('.//div[@id = "reducing-risk"]/descendant::td[@class = "number"]')

        amount = convert_to_decimal(td[0].text)
        estimated_default = convert_to_decimal(td[1].text)
        coverage = amount / estimated_default

        return SafeGuardFund(amount = amount, estimated_default = estimated_default, coverage = coverage)