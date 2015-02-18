#!/usr/bin/env python

from unittest import TestCase

from before_after import before, after, before_after
from before_after.tests import test_functions


class TestBeforeAfter(TestCase):
    def setUp(self):
        test_functions.reset_test_list()
        super(TestBeforeAfter, self).setUp()

    def test_before(self):
        def before_fn(*a):
            test_functions.test_list.append(1)

        with before('before_after.tests.test_functions.sample_fn', before_fn):
            test_functions.sample_fn(2)

        self.assertEqual(test_functions.test_list, [1, 2])

    def test_after(self):
        def after_fn(*a):
            test_functions.test_list.append(2)

        with after('before_after.tests.test_functions.sample_fn', after_fn):
            test_functions.sample_fn(1)

        self.assertEqual(test_functions.test_list, [1, 2])

    def test_before_and_after(self):
        def before_fn(*a):
            test_functions.test_list.append(1)

        def after_fn(*a):
            test_functions.test_list.append(3)

        with before_after(
                'before_after.tests.test_functions.sample_fn',
                before_fn=before_fn, after_fn=after_fn):
            test_functions.sample_fn(2)

        self.assertEqual(test_functions.test_list, [1, 2, 3])

    def test_before_once(self):
        def before_fn(*a):
            test_functions.test_list.append(1)

        with before(
                'before_after.tests.test_functions.sample_fn',
                before_fn, once=True):
            test_functions.sample_fn(2)
            test_functions.sample_fn(3)

        self.assertEqual(test_functions.test_list, [1, 2, 3])

    def test_after_once(self):
        def after_fn(*a):
            test_functions.test_list.append(2)

        with after(
                'before_after.tests.test_functions.sample_fn',
                after_fn, once=True):
            test_functions.sample_fn(1)
            test_functions.sample_fn(3)

        self.assertEqual(test_functions.test_list, [1, 2, 3])

    def test_before_and_after_once(self):
        def before_fn(*a):
            test_functions.test_list.append(1)

        def after_fn(*a):
            test_functions.test_list.append(3)

        with before_after(
                'before_after.tests.test_functions.sample_fn',
                before_fn=before_fn, after_fn=after_fn, once=True):
            test_functions.sample_fn(2)
            test_functions.sample_fn(4)

        self.assertEqual(test_functions.test_list, [1, 2, 3, 4])
