import unittest

from discombibleator.inputs import *
from discombibleator.reference_lists import  Reference_Lists as ref_list
from discombibleator.algs import *
#from discombibleator.main import *

class Test_Inputs(unittest.TestCase):
    def setUp(self):
        self.verse = Verse("2 drachmae")
        self.units = Units()

    def test_initialization(self):
        self.assertEqual(self.verse.string, "2 drachmae", "incorrect string")
        self.assertEqual(self.units.units, "imperial", "incorrect units")

class Test_Reference_Lists(unittest.TestCase):
    def setUp(self):
        self.multiword_signifiers = ref_list().multiword_signifiers
        self.ordinal_times = ref_list().ordinal_times
        self.punctuation = ref_list().punctuation

    def test_initialization(self):
        self.assertEqual(self.multiword_signifiers, ["hour", "watch", "journey",
            "walk", "cubit", "cubits"], "incorrect multiword signifiers list")
        self.assertEqual(self.ordinal_times, ["second", "third", "fourth",
            "sixth", "seventh", "ninth", "tenth", "eleventh"],
            "incorrect ordinal times list")
        self.assertEqual(self.punctuation, [".", ";", ",", "!", "?", "(", ")",
            ":"], "incorrect punctuation list")

class Test_Tokenizer(unittest.TestCase):
    def setUp(self):
        self.test_string = "Doesn't this need to be tokenized?"
        self.tokenized = ['Does', "n't", 'this', 'need', 'to', 'be',
            'tokenized', '?']

    def test_initialization(self):
        self.assertEqual(Tokenize(self.test_string).string, self.test_string,
            "Not correctly initialized")
        self.assertEqual(Tokenize(self.test_string).arr, None,
            "Not equal to none")

    def test_run_method(self):
        output = Tokenize(self.test_string).__run__()
        self.assertEqual(output, self.tokenized, "Not correctly tokenized")

class Test_Concat_Multiword(unittest.TestCase):
    def setUp(self):
        self.test_arr1 = ["We", "ate", "at", "the", "ninth", "hour", "and",
            "stayed", "till", "the", "second", "watch", "."]

        self.test_arr2 = ["5", "cubits", "and", "2", "long", "cubits"]

        self.test_arr3 = ["No", "multiword", "signifiers", "here", "!"]

    def test_initialization(self):
        self.assertEqual(Concat_Multiword(self.test_arr1).arr, self.test_arr1,
            "Concat_Multiword did not take array")
        self.assertEqual(Concat_Multiword(self.test_arr1).has_multiword, True,
            "Concat_Multiword did not recognize multiword")
        self.assertEqual(Concat_Multiword(self.test_arr3).has_multiword, False,
            "Concat_Multiword corectly found no multiwords")
        self.assertEqual(Concat_Multiword(self.test_arr1).signifiers,
            set(["hour", "watch"]), "Did not pull out both hour and watch")
        self.assertEqual(Concat_Multiword(self.test_arr2).signifiers,
            set(["cubits"]), "did not pull out cubits correctly")
        self.assertEqual(Concat_Multiword(self.test_arr3).signifiers,
            set(), "failed on empty set")
        self.assertEqual(Concat_Multiword(self.test_arr2).ordinal,
            ref_list().ordinal_times, "ordinal list not imported to class")
        self.assertEqual(Concat_Multiword(self.test_arr3).ordinal,
            ref_list().ordinal_times, "ordinal list not imported to class")

    def test_run_method(self):
        output1 = Concat_Multiword(self.test_arr1).__run__()
        output2 = Concat_Multiword(self.test_arr2).__run__()
        output3 = Concat_Multiword(self.test_arr3).__run__()
        self.assertEqual(output1, ["We", "ate", "at", "the ninth hour", "and",
            "stayed", "till", "the second watch", "."],
            "did not concatenate correctly")
        self.assertEqual(output2, ["5", "cubits", "and", "2", "long cubits"],
            "did not concatenate correctly")
        self.assertEqual(output3, ["No", "multiword", "signifiers", "here",
            "!"], "did not concatenate correctly")

if __name__ == '__main__':
    unittest.main()

"""
y = Verse("2 drachmae")
y.Return_String()

x = Biblical_Measurement(y.Return_String())
x.Concat_Multiword()
x.Has_Measure_Words()
x.Lemmatize_Measure_Words()
x.Find_Convert_Numbers()
x.Convert_Measure_Words()
x.Join_Elements()


x = Biblical_Measurement("It was 12 cubits tall and we saw it during the ninth hour.")
x.concat_multiword()
x.has_measure_words()
x.lemmatize_measure_words()
x.find_convert_numbers()
x.convert_measure_words()
x.join_elements()



x = Biblical_Measurement("It was 12 or 13 cubits tall and we saw it during the ninth hour")
x.concat_multiword()
x.has_measure_words()
x.lemmatize_measure_words()
x.find_convert_numbers()
x.convert_measure_words()
x.join_elements()



x = Biblical_Measurement("The bath of wine cost 12 or 13 talents of gold and a denarius; and we saw it during the ninth hour.")
x.concat_multiword()
x.has_measure_words()
x.lemmatize_measure_words()
x.find_convert_numbers()
x.convert_measure_words()
x.join_elements()
"""
