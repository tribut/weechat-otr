# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=too-many-public-methods

from __future__ import unicode_literals

import sys

from weechat_otr_test.weechat_otr_test_case import WeechatOtrTestCase

import weechat_otr

class WeechatOtrGeneralTestCase(WeechatOtrTestCase):

    def test_build_privmsg_in_without_newline(self):
        result = weechat_otr.build_privmsg_in('f', 't', 'line1')
        self.assertEqual(result, ':f PRIVMSG t :line1')

    def test_build_privmsg_in_with_newline(self):
        result = weechat_otr.build_privmsg_in('f', 't', 'line1\nline2')
        self.assertEqual(result, ':f PRIVMSG t :line1line2')

    def test_build_privmsgs_in_without_newline(self):
        fromm = 'f'
        to = 't'
        line = 'line1'
        result = weechat_otr.build_privmsgs_in(fromm, to, line)
        self.assertEqual(
            result, weechat_otr.build_privmsg_in(fromm, to, line))

    def test_build_privmsgs_in_without_newline_prefix(self):
        fromm = 'f'
        to = 't'
        line = 'line1'
        prefix = 'Some prefix: '
        result = weechat_otr.build_privmsgs_in(fromm, to, line, prefix)
        self.assertEqual(
            result,
            weechat_otr.build_privmsg_in(
                fromm, to, '{prefix}{line}'.format(prefix=prefix, line=line)))

    def test_build_privmsgs_in_with_newline(self):
        fromm = 'f'
        to = 't'
        result = weechat_otr.build_privmsgs_in(fromm, to, 'line1\nline2')
        self.assertEqual(result, '{msg1}\r\n{msg2}'.format(
            msg1=weechat_otr.build_privmsg_in(fromm, to, 'line1'),
            msg2=weechat_otr.build_privmsg_in(fromm, to, 'line2')))

    def test_build_privmsgs_in_with_newline_prefix(self):
        fromm = 'f'
        to = 't'
        prefix = 'Some prefix: '
        result = weechat_otr.build_privmsgs_in(
            fromm, to, 'line1\nline2', prefix)
        self.assertEqual(result, '{msg1}\r\n{msg2}'.format(
            msg1=weechat_otr.build_privmsg_in(
                fromm, to, '{0}line1'.format(prefix)),
            msg2=weechat_otr.build_privmsg_in(
                fromm, to, '{0}line2'.format(prefix))))

    def test_build_privmsg_out_without_newline(self):
        result = weechat_otr.build_privmsg_out('t', 'line1')
        self.assertEqual(result, 'PRIVMSG t :line1')

    def test_build_privmsg_out_with_newline(self):
        result = weechat_otr.build_privmsg_out('t', 'line1\nline2')
        self.assertEqual(result, 'PRIVMSG t :line1\r\nPRIVMSG t :line2')

    def test_msg_irc_from_plain_action(self):
        result = weechat_otr.msg_irc_from_plain('/me does something')
        self.assertEqual(result, '\x01ACTION does something\x01')

    def test_msg_irc_from_plain_no_action(self):
        msg_no_action = 'just a message'
        self.assertEqual(
            weechat_otr.msg_irc_from_plain(msg_no_action),
            msg_no_action)

    def test_msg_irc_from_plain_action_invariant(self):
        msg_action = '\x01ACTION does something\x01'
        self.assertEqual(
            msg_action,
            weechat_otr.msg_irc_from_plain(
                weechat_otr.msg_plain_from_irc(msg_action)))

    def test_msg_plain_from_irc_action(self):
        result = weechat_otr.msg_plain_from_irc('\x01ACTION does something\x01')
        self.assertEqual(result, '/me does something')

    def test_msg_plain_from_irc_no_action(self):
        msg_no_action = 'just a message'
        self.assertEqual(
            weechat_otr.msg_plain_from_irc(msg_no_action),
            msg_no_action)

    def test_msg_plain_from_irc_action_invariant(self):
        msg_action = '/me does something'
        self.assertEqual(
            msg_action,
            weechat_otr.msg_plain_from_irc(
                weechat_otr.msg_irc_from_plain(msg_action)))

    def test_command_cb_start_send_tag_off(self):
        self.call_command_cb(None, None, 'start')

        self.assertPrinted('server_nick_buffer', (
            'eval(${color:default}:! ${color:brown}otr${color:default} !:)\t'
            '(color lightblue)'
            'Sending OTR query... Please await confirmation of the OTR '
            'session being started before sending a message.'))

        self.assertPrinted('server_nick_buffer', (
            'eval(${color:default}:! ${color:brown}otr${color:default} !:)\t'
            '(color lightblue)'
            'To try OTR on all conversations with nick@server: /otr '
            'policy send_tag on'))

    def test_command_cb_start_send_tag_off_no_hints(self):
        sys.modules['weechat'].config_options[
            'otr.general.hints'] = 'off'
        self.call_command_cb(None, None, 'start')

        self.assertNotPrinted('server_nick_buffer', (
            'eval(${color:default}:! ${color:brown}otr${color:default} !:)\t'
            '(color lightblue)'
            'To try OTR on all conversations with nick@server: /otr '
            'policy send_tag on'))

    def test_command_cb_start_send_tag_off_with_hints(self):
        sys.modules['weechat'].config_options['otr.general.hints'] = 'on'
        self.call_command_cb(None, None, 'start')

        self.assertPrinted('server_nick_buffer', (
            'eval(${color:default}:! ${color:brown}otr${color:default} !:)\t'
            '(color lightblue)'
            'To try OTR on all conversations with nick@server: /otr '
            'policy send_tag on'))

    def test_command_cb_start_send_tag_on(self):
        sys.modules['weechat'].config_options[
            'otr.policy.server.nick.nick.send_tag'] = 'on'
        self.call_command_cb(None, None, 'start')

        self.assertPrinted('server_nick_buffer', (
            'eval(${color:default}:! ${color:brown}otr${color:default} !:)\t'
            '(color lightblue)'
            'Sending OTR query... Please await confirmation of the OTR '
            'session being started before sending a message.'))

    def test_irc_sanitize(self):
        result = weechat_otr.irc_sanitize(
            'this\r\x00 is \r\n\rnot an i\n\x00rc command')
        self.assertEqual(result, 'this is not an irc command')

    def test_print_buffer_not_private(self):
        self.call_command_cb(None, None, 'start no_window_nick server')
        self.assertPrinted('non_private_buffer', (
            'eval(${color:default}:! ${color:brown}otr${color:default} !:)\t'
            '(color lightblue)'
            '[no_window_nick] Sending OTR query... Please await confirmation '
            'of the OTR session being started before sending a message.'))
