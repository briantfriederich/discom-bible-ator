from .reference_lists import Reference_Lists as ref_list
from .algs import *
from .inputs import *

class Discombibleator(Verse):

    """Class taking an object and converting it into an output string with
    measurements converted into imperial or metric units.

    """

    def __init__(self, object):
        """Method initializing Discombibleator tool.
        Method initializing Biblical_Measurement object.

        Args:
            string (str)
            units (str)

        Attributes:
            string (str): String of text to be converted into modern measurements.
            arr (arr): Class' string attribute word-tokenized through NLTK.
            units (string): String indicating whether output units will be in
                Imperial or Metric units. Default is Imperial units.
            measurement_found (bool): Boolean indicating a valid Ancient Hebrew
                measurement has been found in self.arr and can be processed.
            lemmatized (bool): Boolean indicating the lemitization step has been
                executed.
            nums_converted (bool): Boolean indicating numbers have been converted.
            mw_converted (bool): Boolean indicating measure words have been converted.
            multiword signifiers (arr): Array of words signaling the possible
                presence of multiword measure words tokenized into multiple items.
            ordinal_times (arr): Array of words indicating a specific time.
            punctuation (arr): List if punctuation to ease detokenizing sentences.
        """
        self.string = object.string
        self.units = object.units
        self.arr = None

    def __run__(self):
        """Method running algorithms from algs.py on inputs from inputs.py"""
        self.arr = Tokenize(self.string).__run__()
        self.arr = Concat_Multiword(self.arr).__run__()
        self.arr = Has_Measure_Words(self.arr).__run__()
        self.arr = Lemmatize_Measure_Words(self.arr).__run__()
        self.arr = Find_Convert_Numbers(self.arr, self.units).__run__()
        return Join_Elements(self.arr).__run__()
