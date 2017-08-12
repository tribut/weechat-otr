# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=too-many-public-methods

from __future__ import unicode_literals

from weechat_otr_test.weechat_otr_test_case import WeechatOtrTestCase
import weechat_otr_test.mock_account
import weechat_otr_test.mock_context

import weechat_otr

class CommandFinishTestCase(WeechatOtrTestCase):

    def after_setup(self):
        self.context = weechat_otr_test.mock_context.MockContext()
        account = weechat_otr_test.mock_account.MockAccount()

        account.add_context('nick2@server', self.context)
        weechat_otr.ACCOUNTS['nick@server'] = account

    def test_finish_buffer(self):
        self.call_command_cb(None, 'server_nick2_buffer', 'finish')

        self.assertEqual(self.context.disconnects, 1)

    def test_finish_args(self):
        self.call_command_cb(None, None, 'finish nick2 server')

        self.assertEqual(self.context.disconnects, 1)

    # /otr end is an alias for /otr finish

    def test_end_buffer(self):
        self.call_command_cb(None, 'server_nick2_buffer', 'end')

        self.assertEqual(self.context.disconnects, 1)

    def test_end_args(self):
        self.call_command_cb(None, None, 'end nick2 server')

        self.assertEqual(self.context.disconnects, 1)
