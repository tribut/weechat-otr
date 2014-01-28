# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=too-many-public-methods

from __future__ import unicode_literals

import sys

from weechat_otr_test.weechat_otr_test_case import WeechatOtrTestCase

import weechat_otr

class WeechatOtrGeneralTestCase(WeechatOtrTestCase):

    def test_message_out_cb(self):
        result = weechat_otr.message_out_cb(None, None, 'server',
            ':nick!user@host PRIVMSG friend :Grüße')
        self.assertEqual(result, 'PRIVMSG friend :Grüße')

    def test_message_out_cb_send_tag_non_ascii(self):
        sys.modules['weechat'].config_options[
            'otr.policy.server.nick.friend.send_tag'] = 'on'

        result = weechat_otr.message_out_cb(None, None, 'server',
            ":nick!user@host PRIVMSG friend :\xc3")
        self.assertEqual(weechat_otr.PYVER.to_unicode(result),
            "PRIVMSG friend :\xc3" +
            " \t  \t\t\t\t \t \t \t    \t\t  \t \t")

    def test_parse_irc_privmsg_channel_ampersand(self):
        result = weechat_otr.parse_irc_privmsg(
            ':nick!user@host PRIVMSG &channel :Grüße')
        self.assertEqual(result['to_channel'], '&channel')

    def test_build_privmsg_in_without_newline(self):
        result = weechat_otr.build_privmsg_in('f', 't', 'Mötley Crüe')
        self.assertEqual(result, ':f PRIVMSG t :Mötley Crüe')

    def test_build_privmsg_in_with_newline(self):
        result = weechat_otr.build_privmsg_in('f', 't', ' Mötley Crüe\nSpın̈al Tap')
        self.assertEqual(result, ':f PRIVMSG t : Mötley CrüeSpın̈al Tap')

    def test_build_privmsgs_in_without_newline(self):
        fromm = 'f'
        to = 't'
        line = 'Blue Öyster Cult'
        result = weechat_otr.build_privmsgs_in(fromm, to, line)
        self.assertEqual(result,
                weechat_otr.build_privmsg_in(fromm, to, line))

    def test_build_privmsgs_in_without_newline_prefix(self):
        fromm = 'f'
        to = 't'
        line = 'Blue Öyster Cult'
        prefix = 'Präfix: '
        result = weechat_otr.build_privmsgs_in(fromm, to, line, prefix)
        self.assertEqual(result,
                weechat_otr.build_privmsg_in(fromm, to, prefix+line))

    def test_build_privmsgs_in_with_newline(self):
        fromm = 'f'
        to = 't'
        result = weechat_otr.build_privmsgs_in(fromm, to, 'Mötley Crüe\nSpın̈al Tap')
        self.assertEqual(result, '{msg1}\r\n{msg2}'.format(
            msg1=weechat_otr.build_privmsg_in(fromm, to, 'Mötley Crüe'),
            msg2=weechat_otr.build_privmsg_in(fromm, to, 'Spın̈al Tap')))

    def test_build_privmsgs_in_with_newline_prefix(self):
        fromm = 'f'
        to = 't'
        prefix = 'Präfix: '
        result = weechat_otr.build_privmsgs_in(fromm, to, 'Mötley Crüe\nSpın̈al Tap',
                prefix)
        self.assertEqual(result, '{msg1}\r\n{msg2}'.format(
            msg1=weechat_otr.build_privmsg_in(fromm, to,
                '{}Mötley Crüe'.format(prefix)),
            msg2=weechat_otr.build_privmsg_in(fromm, to,
                '{}Spın̈al Tap'.format(prefix))))

    def test_build_privmsg_out_without_newline(self):
        result = weechat_otr.build_privmsg_out('t', 'Mötley Crüe')
        self.assertEqual(result, 'PRIVMSG t :Mötley Crüe')

    def test_build_privmsg_out_with_newline(self):
        result = weechat_otr.build_privmsg_out('t', 'Mötley Crüe\nSpın̈al Tap')
        self.assertEqual(result, 'PRIVMSG t :Mötley Crüe\r\nPRIVMSG t :Spın̈al Tap')

    def test_msg_irc_from_plain_action(self):
        result = weechat_otr.msg_irc_from_plain('/me führt etwas aus')
        self.assertEqual(result,
                '\x01ACTION führt etwas aus\x01')

    def test_msg_irc_from_plain_no_action(self):
        msg_no_action = 'Nur eine Übertragung'
        self.assertEqual(weechat_otr.msg_irc_from_plain(msg_no_action),
                msg_no_action)

    def test_msg_irc_from_plain_action_invariant(self):
        msg_action = '\x01ACTION führt etwas aus\x01'
        self.assertEqual(msg_action,
                weechat_otr.msg_irc_from_plain(
                    weechat_otr.msg_plain_from_irc(msg_action)
                    )
                )

    def test_msg_plain_from_irc_action(self):
        result = weechat_otr.msg_plain_from_irc('\x01ACTION führt etwas aus\x01')
        self.assertEqual(result,
                '/me führt etwas aus')

    def test_msg_plain_from_irc_no_action(self):
        msg_no_action = 'Nur eine Übertragung'
        self.assertEqual(weechat_otr.msg_plain_from_irc(msg_no_action),
                msg_no_action)

    def test_msg_plain_from_irc_action_invariant(self):
        msg_action = '/me führt etwas aus'
        self.assertEqual(msg_action,
                weechat_otr.msg_plain_from_irc(
                    weechat_otr.msg_irc_from_plain(msg_action)
                    )
                )

    def test_command_cb_start_send_tag_off(self):
        weechat_otr.command_cb(None, None, 'start')

        self.assertPrinted('server_nick_buffer',
          'otr\tSending OTR query... Please await confirmation of the OTR ' +
          'session being started before sending a message.')

        self.assertPrinted('server_nick_buffer',
          'otr\tTo try OTR on all conversations with nick@server: /otr ' +
          'policy send_tag on')

    def test_command_cb_start_send_tag_off_no_hints(self):
        sys.modules['weechat'].config_options[
            'otr.general.hints'] = 'off'
        weechat_otr.command_cb(None, None, 'start')

        self.assertNotPrinted('server_nick_buffer',
            'otr\tTo try OTR on all conversations with nick@server: /otr ' +
            'policy send_tag on')

    def test_command_cb_start_send_tag_off_with_hints(self):
        sys.modules['weechat'].config_options['otr.general.hints'] = 'on'
        weechat_otr.command_cb(None, None, 'start')

        self.assertPrinted('server_nick_buffer',
            'otr\tTo try OTR on all conversations with nick@server: /otr ' +
            'policy send_tag on')

    def test_command_cb_start_send_tag_on(self):
        sys.modules['weechat'].config_options[
            'otr.policy.server.nick.nick.send_tag'] = 'on'
        weechat_otr.command_cb(None, None, 'start')

        self.assertPrinted('server_nick_buffer',
          'otr\tSending OTR query... Please await confirmation of the OTR ' +
          'session being started before sending a message.')

    def test_irc_sanitize(self):
        result = weechat_otr.irc_sanitize(
            'this\r\x00 is \r\n\rnot an i\n\x00rc command')
        self.assertEqual(result, 'this is not an irc command')

    def test_print_buffer_not_private(self):
        weechat_otr.command_cb(None, None, 'start no_window_nick server')
        self.assertPrinted('non_private_buffer',
            'otr\t[no_window_nick] Sending OTR query... Please await ' +
            'confirmation of the OTR session being started before sending a ' +
            'message.')

    def assertPrinted(self, buf, text):
        self.assertIn(text, sys.modules['weechat'].printed[buf])

    def assertNotPrinted(self, buf, text):
        self.assertNotIn(text, sys.modules['weechat'].printed.get(buf, []))
