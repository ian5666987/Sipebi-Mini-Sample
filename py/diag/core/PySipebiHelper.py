# This file contains helper methods for PySipebi
import os

class PySipebiHelper:
    @staticmethod
    def find_proper_path(filepath):
        if filepath is not None and not os.path.isfile(filepath) and filepath.startswith('py\\'):
            return filepath[len('py\\'):]
        return filepath
