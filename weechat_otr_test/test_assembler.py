# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: disable=too-many-public-methods

from __future__ import unicode_literals

from weechat_otr_test.weechat_otr_test_case import WeechatOtrTestCase

import weechat_otr

class AssemblerTestCase(WeechatOtrTestCase):

    def after_setup(self):
        # pylint: disable=attribute-defined-outside-init
        self.assembler = weechat_otr.Assembler()

    def test_is_query_start(self):
        self.assembler.add('?OTRv2? verschlüsselung/encryption?')

        self.assertTrue(self.assembler.is_query())

    def test_is_query_middle(self):
        self.assembler.add('ATT: ?OTRv2?someone requested verschlüsselung/encryption!')

        self.assertTrue(self.assembler.is_query())

    def test_is_query_end(self):
        self.assembler.add('verschlüsselung/encryption? ?OTRv2?')

        self.assertTrue(self.assembler.is_query())

    def test_add_get(self):
        self.assembler.add('stück 1')
        self.assembler.add('stück 2')
        self.assertEqual(self.assembler.get(), 'stück 1stück 2')
        self.assertEqual(self.assembler.get(), '')

    def test_is_done_non_otr(self):
        self.assembler.add('stück 1')
        self.assertTrue(self.assembler.is_done())
