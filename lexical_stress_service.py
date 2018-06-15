import prosodic as p
from flask import Flask, request
showAlternatives = False 

app = Flask(__name__)


# def mark_word_variants(word_variants):
#     if len(word_variants) == 1 or isMonoSyllab(word_variants):
#         return mark_word(word_variants[0])
#     return str([mark_word(word) for word in word_variants])
#
# def isMonoSyllab(word_variants):
#     return all([word.isMonoSyllab() for word in word_variants])
#
# def mark_word(word):
#     if word.isMonoSyllab():
#         return word.getToken().upper()
#     return ''.join([mark_syllable(syllable) for syllable in word.syllables()])
#
#
# def mark_syllable(syllable):
#     return syllable.str_orth().upper() if syllable.stressed else syllable.str_orth()
#
#
# def mark_line(line):
#     t = p.Text(line)
#     words = t.words(flattenList=(not showAlternatives))
#     if showAlternatives:
#         return " ".join([mark_word_variants(word_variants) for word_variants in words])
#     else:
#         return " ".join([mark_word(word) for word in words])
#

vowels = 'aeiouAEIOU'
vowelsy = 'aeiouyAEIOUY'


class VowelClusterCounter:
    def __init__(self, word):
        letter_no = 0
        token = word.token
        vowel_clusters = 0
        while letter_no < len(token):
            if token[letter_no] in vowels:
                vowel_clusters += 1
                while token[letter_no] in vowels:
                    letter_no += 1
            else:
                letter_no += 1


def find_vowel_clusters(word):
    letter_no = 0
    token = word.token
    vowel_cluster_positions = []
    while letter_no < len(token):
        if token[letter_no] in vowels:
            vowel_cluster_positions.append(letter_no)
            while letter_no < len(token) and token[letter_no] in vowels:
                letter_no += 1
        else:
            letter_no += 1
    return vowel_cluster_positions

def revise_cluster_positions(vowel_cluster_positions, syl_count, token):
    vowel_clusters_ct = len(vowel_cluster_positions)
    if vowel_clusters_ct == (syl_count + 1) and token[-1] == 'e':
        del vowel_cluster_positions[-1]
    elif vowel_clusters_ct == (syl_count + 1) and (
            token[-2:] =='ed'
            or token[-2:] == 'es'
    ):
        del vowel_cluster_positions[-1]
    elif vowel_clusters_ct == (syl_count - 1) and token[-1] == 'y':
        vowel_cluster_positions.append(len(token) - 1)

def mark_lexical_stress(token, position):
    return token[:position] + '`' + token[position:]

def mark_lexical_stress_from_vowel_clusters(word, vowel_cluster_positions):
    syls = word.syllables()
    for i, syl in enumerate(syls):
        if syl.str_stress() == 'P':
            return mark_lexical_stress(word.token, vowel_cluster_positions[i])

def mark_syllable(syllable, str_stress):
    if str_stress == 'P':
        for i, c in enumerate(syllable):
            if c in vowelsy:
                return mark_lexical_stress(syllable, i)
        return syllable
    else:
        return syllable

def syl_text(syllable):
    return syllable.str_orth()

def mark_lexical_stress_by_prosodic(word, vowel_cluster_positions):
    return ''.join([mark_syllable(syl_text(syllable), syllable.str_stress()) for syllable in word.syllables()])


def mark_line(content):
    t = p.Text(content)
    words = t.words()
    results = []
    for i, word in enumerate(words):
        if word.isMonoSyllab():
            result = mark_syllable(syl_text(word.syllables()[0]), 'P')
            # print (i, word.token, word.syllables()[0], result)
        else:
            vowel_cluster_positions = find_vowel_clusters(word)
            syl_count = len(word.syllables())
            token = word.token

            ok = len(vowel_cluster_positions) == syl_count
            if not ok:
                revise_cluster_positions(vowel_cluster_positions, syl_count, token)
                ok = len(vowel_cluster_positions) == syl_count

            if ok:
                result = mark_lexical_stress_from_vowel_clusters(word, vowel_cluster_positions)
            else:
                result = mark_lexical_stress_by_prosodic(word, vowel_cluster_positions)

            if result == token:
                # As a last resort, just mark the first vowel in the word.
                ok = False
                result = mark_syllable(token, 'P')

            if ok:
                pass
                # print (i, vowel_clusters_ct, syl_count, vowel_cluster_positions, token, result)
            else:
                print ('##############', i, syl_count, vowel_cluster_positions, token, result)
        results.append(result)
    return ' '.join(results)


def mark_content(content):
    lines = [mark_line(line) for line in content.split('\n')]
    return '\n'.join(lines)


@app.route("/", methods=['POST'])
def handle_request():
    content = request.data
#    print "============================="
#    print "content: "
#    print content
    return mark_content(content)

lincoln = """Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.
Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.
But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth."""

if __name__ == "__main__":
    #print(mark_content(lincoln))
    app.run(host="198.211.105.27", port="5121")

