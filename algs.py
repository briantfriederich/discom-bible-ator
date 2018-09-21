import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from reference_lists import Reference_Lists

measures = pd.read_csv("data/measures.csv", header = 0, index_col = 0,
                        squeeze=True).to_dict()

measurement_roots = pd.read_csv('data/measurement_roots.csv', header=0,
                                index_col=1, squeeze=True).to_dict()

class Concat_Multiword(object):

    """Method finding and concatenating tokenized multi-word measure words.

    Attributes:
        __init__
        run(arr)

    """

    def __init__(self, arr):
        """Method initializing Concat_Multiword

        Args:
            arr (arr)

        Attributes:
            arr (arr): array of word-tokenized words and symbols
            has_multiword (bool): checks for presence of potential
                multiword-measure words through list of multiword_signifiers
            signifiers (arr): list of multiword_signifiers present in arr
            ordinal (arr): list of ordinal_times signifiers to check
        """
        self.arr = arr
        self.has_multiword = any(np.intersect1d(arr, Reference_Lists.multiword_signifiers))
        self.signifiers = set(arr).intersection(Reference_Lists.multiword_signifiers)
        self.ordinal = Reference_Lists.ordinal_times

    def run(self):
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
        run

    """

    def __init__(self, arr):
        """Method initializing Has_Measure_Words

        args:
            arr (arr)

        attributes:
            arr (arr): array to be checked for relevant measure words
            measurement_found (bool): signifier if measure word found,
                initialized to False
            mwords (dict): dictionary of measure words in various forms
        """
        self.arr = arr
        self.measurement_found = False
        self.mwords = set(Reference_Lists.measurement_roots.keys(),
                          Reference_Lists.measurement_roots.values())

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

    def Lemmatize_Measure_Words(self):
        """Method lemmatizing measure words in input.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        if self.measurement_found: #change to assertion
            for word in set(arr).intersection(measurement_roots.keys()):
                arr[:] = [measurement_roots[word] if x == word else x for x in arr]
            self.lemmatized = True
        self.tokenized_string = arr

    def Represents_Int(self, s):
        """Method checking whether an input is a string representation of an integer.

        Args:
            s (string): string item to be checked

        Returns:
            (bool): whether the input is a string representation of an integer
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    def Number_Converter(self, n, measure_word):
        """Method converting number from units in Ancient Hebrew measurements to
        units in modern measurements.

        Args:
            n (int): number to be converted
            measure_word (str): Ancient Hebrew units in which n was measured

        Returns:
            (str): string of the float of n converted into Imperial or Metric units
        """
        if self.units == "metric":
            n = float(n) * float(measures['metric_multiplier'][measure_word])
        else:
            n = float(n) * float(measures['imperial_multiplier'][measure_word])
        return str(n)

    def Measure_Word_Converter(self, word):
        """Method converting measure words into Imperial or Metric measures.

        Args:
            word(str): Ancient Hebrew measure word to be converted

        Returns:
            (str): string of corresponding metric or imperial measure
        """
        return (measures[self.units][word])

    def Find_Convert_Numbers(self):
        """Method locating and converting relevant numbers.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        if self.lemmatized: # turn into assertion
            for i, j in enumerate(arr):
                if j in measurement_roots.values():
                    for unit in arr[:i]: # I don't like that this might look so extensively back.
                        if (i - arr.index(unit)) <= 4:
                            unit_locator = arr.index(unit)
                            if self.Represents_Int(unit):
                                arr[unit_locator] = self.Number_Converter(unit, j)
                            elif unit in ("a", "an", "the", "A", "An", "The"):
                                if(arr.index(j) - unit_locator) in range(2):
                                    arr[unit_locator] = self.Number_Converter(1, j)
            self.nums_converted = True
        self.tokenized_string = arr

    def Convert_Measure_Words(self):
        """Method locating and converting relevant numbers.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        if self.nums_converted: # turn into assertion
            for i, j in enumerate(arr):
                if j in measurement_roots.values():
                    arr[i] = self.Measure_Word_Converter(j)
        self.mw_converted = True
        self.tokenized_string = arr

    def Join_Elements(self):
        """Method detokenizing array of words into final sentence.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        for element in arr:
            output = "".join([" "+i if not i.startswith("'") and i not in self.punctuation else i for i in arr]).strip()
        self.tokenized_string = arr
        return output
