import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from reference_lists.Reference_Lists import multiword_signifiers as multiwords
from reference_lists.Reference_Lists import ordinal_times as ordinal

measures = pd.read_csv("data/measures.csv", header = 0, index_col = 0,
                        squeeze=True).to_dict()

measurement_roots = pd.read_csv('data/measurement_roots.csv', header=0,
                                index_col=1, squeeze=True).to_dict()

class Concat_Multiword(object):

    """Method finding and concatenating tokenized multi-word measure words.

    attributes:
        __init__
        __run__

    """

    def __init__(self, object):
        """Method initializing Concat_Multiword

        args:
            object (obj)

        attributes:
            arr (arr): array of word-tokenized words and symbols
            has_multiword (bool): checks for presence of potential
                multiword-measure words through list of multiword_signifiers
            signifiers (arr): list of multiword_signifiers present in arr
            ordinal (arr): list of ordinal_times signifiers to check
        """
        self.arr = object.string
        self.has_multiword = any(np.intersect1d(arr, multiwords))
        self.signifiers = set(arr).intersection(multiwords)
        self.ordinal = ordinal

    def __run__(self):
        """Method to concatenate multi-word measure words into one Array
        item

        returns:
            arr (arr): array of words with multiword tokens joined
        """
        if self.has_multiword == True:
            for i, j in enumerate(self.arr):
                if j in self.signifiers:
                    if self.arr[i-1] in self.ordinal:
                        self.arr[i-2:i+1] = [" ".join(self.arr[i-2:i+1])]
                    elif j in ("journey", "walk") and \
                    self.arr[i-2] in ("day", "days"):
                        if self.arr[i-3] in ("Sabbath", "sabbath"):
                            self.arr[i-2:i+1] = ["sabbath day's journey"]
                        else:
                            self.arr[i-1:i+1] = ["day's journey"]
                    elif j in ("cubit", "cubits"):
                        if self.arr[i-1] == 'long':
                            self.arr[i-1:i+1] = [" ".join(arr[i-1:i+1])]
        return self.arr

class Has_Measure_Words(object):

    """Method checking whether a valid measurement can be found in the input.

    attributes:
        __init__
        __run__

    """

    def __init__(self, object):
        """Method initializing Has_Measure_Words

        args:
            arr (arr)

        attributes:
            arr (arr): array to be checked for relevant measure words
            measurement_found (bool): signifier if measure word found,
                initialized to False
            mwords (dict): dictionary of measure words in various forms
        """
        self.arr = object.string
        self.measurement_found = False
        self.mwords = set(measurement_roots.keys(), measurement_roots.values())

    def run(self):
        """Method checking for presence of measurments in Ancient Hebrew units

        returns:
            arr (arr): returns array if Ancient Hebrew measure words found
                in arr
        """
        if any(self.mwords.intersection(self.arr)):
            self.measurement_found = True
            return self.arr
        else:
            print("Measurement to be converted not found in input text:\n{}".format(self.arr))
            break

class Lemmatize_Measure_Words(object):
        """Method lemmatizing measure words in input.

        attributes:
            __init__
            __run__
        """
    def __init__(self, object):
        self.arr = object.string
        self.mroots = measurement_roots.values()

    def run(self):
        for word in set(arr).intersection(self.mroots):
            self.arr[:] = [self.mroots[word] if x == word else x for x in arr]
        return self.arr

class Find_Convert_Numbers(object):

        """Class locating and converting relevant numbers.

        attributes:
            __init__
            Represents_Int
            Number_Multiplier
            Number_Converter
            Range_Sensitizer
            Measure_Word_Converter
            Match_Num_MW
            __run__
        """

    def __init__(self, object):
        """Method initializing Find_Convert_Numbers

        args:
            arr (arr)

        attributes:
            arr (arr): array to be processed
            units (str): string indication whether measurement are to be given
                in metric or imperial units. Default in imperial
            num_mw_match & mw_num_match (arr): array of Ancient Hebrew measure
                words Number_Converter and Measure_Word_Converter use, for
                comparison
        """
        self.arr = object.string
        self.units = object.units
        self.num_mw_match = []
        self.mw_num_match = []

    def Represents_Int(self, s):
        """Method checking whether an input is a string representation of an integer.

        args:
            s (string): string item to be checked

        returns:
            (bool): whether the input is a string representation of an integer
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    def Number_Multiplier(self, n, measure_word):
        """Method converting number from units in Ancient Hebrew measurements to
        units in modern measurements.

        args:
            n (int): number to be converted
            measure_word (str): Ancient Hebrew units in which n was measured

        returns:
            (str): string of the float of n converted into Imperial or Metric
                units
        """
        if self.units == "metric":
            n = float(n) * float(measures['metric_multiplier'][measure_word])
        else:
            n = float(n) * float(measures['imperial_multiplier'][measure_word])
        self.num_mw_match.append(measure_word)
        return str(n)

    def Number_Converter(unit, arr):
        """Method handling both integers and the words "the" and "an" before
        measure words, converting them to imperial or metric units

        args:
            arr (arr): array to be examined for ints or variations on "a" and
                "the"
        returns:
            arr (arr): array with numbers replaced with converted numbers
        """
        unit_locator = arr.index(unit)
        if self.Represents_Int(unit):
            arr[unit_locator] = self.Number_Multiplier(unit, j)
        elif unit in ("a", "an", "the", "A", "An", "The"):
            if(arr.index(j) - unit_locator) in range(2):
                arr[unit_locator] = self.Number_Multiplier(1, j)
        return arr

    def Range_Sensitizer(self):
        """Method catching numbers separated from measure words by adjectives
        or other filler words

        args:
            arr (arr): array to be processed

        returns:
            arr (arr): array with original numbers converted to modern units
        """
        for i, j in enumerate(self.arr):
            if j in measurement_roots.values():
                if i <= 4:
                    for unit in arr[:i]:
                        self.arr = Number_Converter(unit, self.arr)
                else:
                    for unit in arr[i-4:i]:
                        self.arr = Number_Converter(unit, self.arr)
        return self.arr


    def Measure_Word_Converter(self):
        """Method converting measure words into Imperial or Metric measures.

        Returns:
            (str): string of corresponding metric or imperial measure
        """
        for i, j in enumerate(self.arr):
            if j in measurement_roots.values():
                mw_num_match.append(j)
                self.arr[i] = measures[self.units][j]
        return self.arr

    def Match_Num_MW(self):
        """Method checking that measure words used to convert numbers correspond
        to measure words converted to modern versions
        """
        try:
            self.num_mw_match == self.mw_num_match
        except AssertionError:
            print("Measure words and corresponding numbers", \
                    "don't match:\n{}".format(self.num_mw_match,
                    self.mw_num_match))
            break

    def __run__(self):
        """Method running consecutive methods within Find_Convert_Numbers class

        returns:
            arr (arr): array with measurement elements converted into modern
                units
        """
        nums_converted = self.Range_Sensitizer(self.arr)
        mws_converted = self.Measure_Word_Converter(nums_converted)
        self.Match_Num_MW(mws_converted)
        self.arr = mws_converted
        return self.arr


class Join_Elements(object):

        """Class detokenizing array of words into final sentence.

        attributes:
            __init__

        """

    def __init__(self, object):
        """Method initializing Join_Elements class

        args:
            arr (arr): array to be joined into continuous string
        """
        self.arr = object.string
        self.output = None

    def run(self):
        """Method running Join_Elements class

        returns:
            output (str): string of input verse with Ancient Hebrew measurements
            converted into modern measurements.
        """
        for element in self.arr:
            self.output = "".join([" "+i if not i.startswith("'") and \
            i not in self.punctuation else i for i in arr]).strip()
        return self.output
