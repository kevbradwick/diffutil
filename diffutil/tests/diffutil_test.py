"""
Info on reading diffs;
http://www.markusbe.com/2009/12/how-to-read-a-patch-or-diff-and-understand-its-structure-to-apply-it-manually/

"""
from diffutil import DiffUtil
import unittest
import os

diff_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'diffs')

class DiffUtilTest(unittest.TestCase):

    def test_helper_exists(self):
        self.assertIsInstance(DiffUtil, object)

    def test_exception_raise_when_arguments_not_specified(self):
        self.assertRaises(ValueError, DiffUtil)

    def test_exception_raised_when_file_does_not_exist(self):
        self.assertRaises(ValueError, DiffUtil, diff_file='foo')

    def test_detect_unified_format(self):
        diff = DiffUtil(diff_file=os.path.join(diff_path, 'unified', 'jquery_754bda21.diff'))
        self.assertEqual(DiffUtil.TYPE_UNIFIED, diff.format)

    def test_detect_unknown_format(self):
        diff = DiffUtil(diff_text='foo')
        self.assertEqual(DiffUtil.TYPE_UNKNOWN, diff.format)

    def test_detect_normal_format(self):
        diff = DiffUtil(diff_file=os.path.join(diff_path, 'normal', 'jquery-1.3-1.7.diff'))
        self.assertEqual(DiffUtil.TYPE_NORMAL, diff.format)

    def test_detect_context_format(self):
        diff = DiffUtil(diff_file=os.path.join(diff_path, 'context', 'jquery-1.3-1.7.diff'))
        self.assertEqual(DiffUtil.TYPE_CONTEXT, diff.format)