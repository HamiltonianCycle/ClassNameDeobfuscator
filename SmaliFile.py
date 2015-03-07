__author__ = 'HamiltonianPath'


class SmaliFile:
    """A class to represent a Smali file."""

    raw_lines = []  # A list of all lines in the Smali file.

    def __init__(self, filepath=None):
        if filepath:
            self.readsmalifile(filepath)

    def readsmalifile(self, filepath):
        f = open(filepath, 'r')
        self.raw_lines = f.readlines()
