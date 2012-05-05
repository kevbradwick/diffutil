import os
import re

class DiffUtil(object):
    """
    DiffUtil
    """

    TYPE_UNIFIED = 1
    TYPE_NORMAL  = 2
    TYPE_CONTEXT = 4
    TYPE_UNKNOWN = 8

    def __init__(self, diff_text=None, diff_file=None):
        """
        When creating a new instance of DiffUtil, you can pass either the raw diff text or a string to the path
        of a diff file.
        """
        if diff_file is None and diff_text is None:
            raise ValueError('You must supply diff as text of a file name to use DiffUtil')

        if diff_file:
            if os.path.isfile(diff_file) is False:
                raise ValueError('The file "%s" does not exist' % diff_file)
            else:
                try:
                    self._diff = open(diff_file).read()
                except IOError:
                    raise ValueError('Unable to open the file "%s", please check the permissions' % diff_file)
        elif diff_text:
            self._diff = diff_text


    @property
    def format(self):
        """
        Check the type of diff
        """
        _u = re.compile('@@\s[\-0-9,]+\s[\+0-9,]+\s@@')
        if _u.search(self._diff):
            return self.TYPE_UNIFIED
        return self.TYPE_UNKNOWN