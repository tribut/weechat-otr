# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=too-many-public-methods

from __future__ import unicode_literals

from weechat_otr_test.weechat_otr_test_case import WeechatOtrTestCase

import weechat_otr

class SmpTestCase(WeechatOtrTestCase):

    def test_smp_ask_nick_server_question_secret(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, None, 'smp ask nick2 server question secret')

        self.assertEqual(('secret', 'question'), context.smp_init)

    def test_smp_ask_nick_server_secret(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, None, 'smp ask nick2 server secret')

        self.assertEqual(('secret', None), context.smp_init)

    def test_smp_ask_nick_server_secret_non_ascii(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, None, 'smp ask nick2 server motörhead')

        self.assertEqual(
            (weechat_otr.PYVER.to_str('motörhead'), None), context.smp_init)

    def test_smp_ask_question_secret(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, 'server_nick2_buffer', 'smp ask question secret')

        self.assertEqual(('secret', 'question'), context.smp_init)

    def test_smp_ask_secret(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(None, 'server_nick2_buffer', 'smp ask secret')

        self.assertEqual(('secret', None), context.smp_init)

    def test_smp_ask_nick_server_question_secret_multiple_words(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, None, "smp ask nick2 server 'what is the secret?' "
            "'eastmost penninsula is the secret'")

        self.assertEqual(
            ('eastmost penninsula is the secret', 'what is the secret?'),
            context.smp_init)

    def test_smp_respond_secret(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, 'server_nick2_buffer', 'smp respond secret')

        self.assertEqual(('secret', ), context.smp_got_secret)

    def test_smp_respond_nick_server_secret(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, 'server_nick2_buffer', 'smp respond nick2 server secret')

        self.assertEqual(('secret', ), context.smp_got_secret)

    def test_smp_respond_secret_non_ascii(self):
        context = self.setup_context('nick@server', 'nick2@server')

        self.call_command_cb(
            None, 'server_nick2_buffer', 'smp respond deathtöngue')

        self.assertEqual(
            (weechat_otr.PYVER.to_str('deathtöngue'), ),
            context.smp_got_secret)

    def test_smp_abort(self):
        context = self.setup_context('nick@server', 'nick2@server')
        context.in_smp = True

        self.call_command_cb(None, 'server_nick2_buffer', 'smp abort')

        self.assertEqual([('SMP aborted.',)], context.smp_finishes)
