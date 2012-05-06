import os
import re

class Diff(object):

    def __init__(self, diff):
        """
        Pass the raw diff text in to the constructor
        """
        self._raw_diff = diff

class UnifiedDiff(Diff):

    def sections(self):
        pattern = re.compile(r'^(diff.*?)(?=^diff|\Z)', re.M | re.S)
        sections = []
        for section in pattern.findall(self._raw_diff):
            _section = dict()
            _section['raw_diff'] = section
            for line in section:
                if line.startswith('---'):
                    _section['left_file'] = line.split('--- ')[1]
                elif line.startswith('+++'):
                    _section['right_file'] = line.split('+++ ')[1]
            sections.append(_section)
        return sections

class ContextDiff(Diff):
    pass

class NormalDiff(Diff):
    pass

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
        self._diff_object = None
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
        _n = re.compile('\d+(c|a|d)\d+(\n|\r)<')
        _c = re.compile('\*{3}\s\d+,?\d+?\s\*{4}')
        if _u.search(self._diff):
            return self.TYPE_UNIFIED
        elif _n.search(self._diff):
            return self.TYPE_NORMAL
        elif _c.search(self._diff):
            return self.TYPE_CONTEXT
        return self.TYPE_UNKNOWN


    @property
    def diff_object(self):
        """
        Get the Diff object
        """
        if isinstance(self._diff_object, Diff):
            return self._diff_object

        if self.format == self.TYPE_UNIFIED:
            self._diff_object = UnifiedDiff(self._diff)
        elif self.format == self.TYPE_CONTEXT:
            self._diff_object = ContextDiff(self._diff)
        elif self.format == self.TYPE_NORMAL:
            self._diff_object = NormalDiff(self._diff)
        else:
            raise RuntimeError('Invalid diff format supplied')

        return self._diff_object


    @property
    def sections(self):
        """
        Get the sections of the diff file
        """
        return self.diff_object.sections()