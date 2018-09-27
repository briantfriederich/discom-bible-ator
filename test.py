import unittest

from discombibleator.inputs import *
from discombibleator.reference_lists import  Reference_Lists as ref_list
from discombibleator.algs import *
from discombibleator.main import *


class Test_Inputs(unittest.TestCase):
    def setUp(self):
        self.verse1 = Verse("2 drachmae")
        self.verse2 = Verse("2 drachmae", "metric")

    def test_initialization(self):
        self.assertEqual(self.verse1.string, "2 drachmae", "incorrect string")
        self.assertEqual(self.verse1.units, "imperial", "incorrect units")
        self.assertEqual(self.verse2.units, "metric", "incorrect units")

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

class Test_Has_Measure_Words(unittest.TestCase):
    def setUp(self):
        self.test_arr1 = ["Now", "is", "the eleventh hour", "."]
        self.test_arr2 = ["No", "measurements", "here"]

    def test_initialization(self):
        self.assertEqual(Has_Measure_Words(self.test_arr1).arr, self.test_arr1,
            "array not initialized properly")
        self.assertEqual(len(Has_Measure_Words(self.test_arr2).mwords),
            88, "measure words not loaded properly into class")

    def test_run_method(self):
        output1 = Has_Measure_Words(self.test_arr1).__run__()
        self.assertEqual(output1, self.test_arr1, "array not returned")
        with self.assertRaises(ValueError):
            Has_Measure_Words(self.test_arr2).__run__()

class Test_Lemmatize_Measure_Words(unittest.TestCase):
    def setUp(self):
        self.test_arr1 = ["5", "spans", "and", "10", "long cubits", "at", "5",
            "day's journey", "away", "."]
        self.test_arr2 = ["10", "shekels", "and", "1", "shekel"]

    def test_initialization(self):
        self.assertEqual(Lemmatize_Measure_Words(self.test_arr1).arr,
            self.test_arr1, "array not initialized properly")

    def test_run_method(self):
        output1 = Lemmatize_Measure_Words(self.test_arr1).__run__()
        output2 = Lemmatize_Measure_Words(self.test_arr2).__run__()
        self.assertEqual(output1, ["5", "span", "and", "10", "long cubit", "at",
         "5", "day's journey", "away", "."], "did not lemmatize correctly")
        self.assertEqual(output2,["10", "shekel", "and", "1", "shekel"],
            "did not lemmatize correctly")

class Test_Find_Convert_Numbers(unittest.TestCase):
    def setUp(self):
        self.test_arr1 = ["12", "golden", "shekel"]
        self.test_arr2 = ["twelve", "golden", "shekel"]
        self.test_arr3 = ["I", "drank", "a", "bath", "of", "wine", "and",
            "5", "homer", "of", "water", "."]
        self.test_arr4 = ["12", "years", "ago", "I", "took", "a", "nice",
        "long", "walk", "along", "a", "river", "."]

    def test_initialization(self):
        self.assertEqual(Find_Convert_Numbers(self.test_arr1).arr,
            self.test_arr1, "array not initialized properly")
        self.assertEqual(Find_Convert_Numbers(self.test_arr1).units,
         "imperial", "did not initialize units correctly")
        self.assertEqual(Find_Convert_Numbers(self.test_arr1, "metric").units,
            "metric", "did not initialize units correctly")

    def test_represents_num(self):
        self.assertEqual(Find_Convert_Numbers.represents_num(self.test_arr1,
        "12"), True, "Didn't recognize int")
        self.assertEqual(Find_Convert_Numbers.represents_num(self.test_arr2,
        "twelve"), False, "Didn't execute correctly")

    def test_number_multiplier(self):
        self.assertEqual(Find_Convert_Numbers(self.test_arr1).number_multiplier(
            "70", "cubit"), "105.0", "did not multiply correctly")
        self.assertEqual(Find_Convert_Numbers(self.test_arr1,
            "metric").number_multiplier("70", "cubit"), "32.0",
            "did not multiply correctly")
        self.assertEqual(Find_Convert_Numbers(self.test_arr1).number_multiplier(
            "0", "talent"), "0.0", "did not multiply correctly")

    def test_nums_to_modern(self):
        array_1 = Find_Convert_Numbers(self.test_arr1)
        array_3 = Find_Convert_Numbers(self.test_arr3)
        array_4 = Find_Convert_Numbers(self.test_arr4)
        self.assertEqual(Find_Convert_Numbers.nums_to_modern(array_1),
            ["4.8", "golden", "shekel"], "did not convert correctly")
        self.assertEqual(Find_Convert_Numbers.nums_to_modern(array_3),
            ["I", "drank", "5.9", "bath", "of", "wine", "and", "295.0",
            "homer", "of", "water", "."],
            "did not convert correctly")
        self.assertEqual(Find_Convert_Numbers.nums_to_modern(array_4),
            ["12", "years", "ago", "I", "took", "a", "nice", "long", "walk",
            "along", "a", "river", "."], "did not convert correctly")

    def test_run_method(self):
        output1 = Find_Convert_Numbers(self.test_arr1).__run__()
        output2 = Find_Convert_Numbers(self.test_arr2).__run__()
        output3 = Find_Convert_Numbers(self.test_arr3).__run__()
        output4 = Find_Convert_Numbers(self.test_arr4).__run__()

        self.assertEqual(output1, ['4.8', 'golden', 'shekel'],
            "did not match numbers correctly")
        self.assertEqual(output3, ["I", "drank", "5.9", "bath", "of", "wine",
         "and", "295.0", "homer", "of", "water", "."],
            "did not match numbers correctly")
        self.assertEqual(output4, self.test_arr4,
            "did not match numbers correctly")
        self.assertEqual(output2, ['twelve', 'golden', 'shekel'],
            "did not match numbers correctly")

class Test_Join_Elements(unittest.TestCase):
    def setUp(self):
        self.test_arr1 = ['4.8', 'golden', 'ounces']
        self.test_arr2 = ["twelve", "golden", "shekel"]
        self.test_arr3 = ["I", "drank", "5.9", "gallons", "of", "wine",
         "and", "295.0", "gallons", "of", "water", "."]
        self.test_arr4 = ["12", "years", "ago", "I", "took", "a", "nice",
            "long", "bath", "in", "a", "river", "."]

    def test_initialization(self):
        self.assertEqual(Join_Elements(self.test_arr1).arr,
            self.test_arr1, "array not initialized properly")
        self.assertEqual(Join_Elements(self.test_arr2).output,
            None, "output attribute not initialized properly")

    def test_run_method(self):
        self.assertEqual(Join_Elements(self.test_arr1).__run__(),
            "4.8 golden ounces", "run method did not execute properly")
        with self.assertRaises(ValueError):
            Join_Elements(self.test_arr2).__run__()
        self.assertEqual(Join_Elements(self.test_arr3).__run__(),
            "I drank 5.9 gallons of wine and 295.0 gallons of water.",
            "run method did not execute properly")
        self.assertEqual(Join_Elements(self.test_arr4).__run__(),
            "12 years ago I took a nice long bath in a river.",
            "run method did not execute properly")

class Test_Main_Setup(unittest.TestCase):
    def setUp(self):
        self.verse1 = Verse("2 drachmae")
        self.verse2 = Verse("2 drachmae", "metric")
        self.d_verse1 = Discombibleator(self.verse1)
        self.d_verse2 = Discombibleator(self.verse2)
        self.full_pipeline_test1 = Discombibleator(Verse("The marble columns"
            " were a long cubit wide and 52 cubits tall.")).run()
        self.full_pipeline_test2 = Discombibleator(Verse("And on the second day,"
            " she woke at the ninth hour.")).run()
        self.full_pipeline_test3 = Discombibleator(Verse("At the eleventh hour"
            " he paid a golden talent to the emperor.",
            "metric")).run()

    def test_initialization(self):
        self.assertEqual(self.d_verse1.string,
            "2 drachmae", "incorrect string")
        self.assertEqual(self.d_verse1.units,
            "imperial", "incorrect string")
        self.assertEqual(self.d_verse2.units,
            "metric", "incorrect string")

    def test_run_method(self):
        self.assertEqual(self.d_verse1.run(), "1.3 USD",
            "values not converted correctly")

    def test_full_pipeline(self):
        self.assertEqual(self.full_pipeline_test1,
            "The marble columns were 20.4 inches wide and 78.0 feet tall.",
            "Discombibleator did not run correctly")
        self.assertEqual(self.full_pipeline_test2,
            "And on the second day, she woke at 3:00 PM.",
            "Discombibleator did not run correctly")
        self.assertEqual(self.full_pipeline_test3,
            "At 5:00 PM he paid 34.02 golden kg to the emperor.",
            "Discombibleator did not run correctly")

if __name__ == '__main__':
    unittest.main()
