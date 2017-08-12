# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: disable=too-many-public-methods
# pylint: disable=invalid-name

from __future__ import unicode_literals

import sys
import tempfile
import unittest

import weechat_otr_test.mock_weechat
sys.modules['weechat'] = weechat_otr_test.mock_weechat.MockWeechat(
    tempfile.mkdtemp())

# pylint: disable=wrong-import-position
import weechat_otr

# Python 2.6 compatibility
if not hasattr(unittest.TestCase, 'assertIs'):
    import unittest2 as unittest

class WeechatOtrTestCase(unittest.TestCase):

    def setUp(self):
        sys.modules['weechat'].save()
        weechat_otr.ACCOUNTS.clear()
        weechat_otr.otr_debug_buffer = None
        self.after_setup()

    def tearDown(self):
        sys.modules['weechat'].restore()
        self.after_teardown()

    def after_setup(self):
        pass

    def after_teardown(self):
        pass

    def assertPrinted(self, buf, text):
        self.assertIn(text, sys.modules['weechat'].printed[buf])

    def assertPrintedContains(self, buf, regex):
        self.assertRegex(
            ''.join(sys.modules['weechat'].printed.get(buf, [])),
            regex)

    def assertNotPrinted(self, buf, text):
        self.assertNotIn(text, sys.modules['weechat'].printed.get(buf, []))

    def assertNoPrintedContains(self, buf, text):
        for line in sys.modules['weechat'].printed.get(buf, []):
            self.assertNotIn(text, line)

    def assertRegex(self, s, r):
        # To get rid of deprecation warning in python 3.
        try:
            # Python 3.
            super(WeechatOtrTestCase, self).assertRegex(s, r)
        except AttributeError:
            # Python 2.
            self.assertRegexpMatches(s, r)

    def setup_context(self, account_name, context_name):
        # pylint: disable=no-self-use
        context = weechat_otr_test.mock_context.MockContext()
        account = weechat_otr_test.mock_account.MockAccount()
        account.add_context(context_name, context)
        weechat_otr.ACCOUNTS[account_name] = account

        return context
