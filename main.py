from reference_lists import Reference_Lists
from algs import *
from verse import *

class Discombibleator(Verse):

    """Class taking an object and converting it into an output string with
    measurements converted into imperial or metric units.

    """

    def __init__(self, Verse):
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
        self.string = Verse.string
        self.units = Verse.units


    def __run__(self):
        "Method running algorithms on "
        tokenized = Tokenize(self.input)
        Concat_Multiword.run()
        Has_Multiword.run()
        Lemmatize_Measure_Words.run()
        Find_Convert_Numbers.run()
        Join_Elements.run()
