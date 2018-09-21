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
