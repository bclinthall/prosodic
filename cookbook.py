import prosodic as p
t = p.Text('corpora/corppoetry_fi/fi.koskenniemi.txt',lang='fi')


def is_ntV(word):
	phonemes = word.phonemes()
	if phonemes[-3:-1] != [p.Phoneme("n"), p.Phoneme("t")]:
		return False
	return phonemes[-1].feature("syll")



nta = [word for word in t.words() if is_ntV(word)]
print nta