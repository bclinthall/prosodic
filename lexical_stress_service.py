import prosodic as p
from flask import Flask, request
showAlternatives = True

app = Flask(__name__)


def mark_word_variants(word_variants):
    if len(word_variants) == 1 or isMonoSyllab(word_variants):
        return mark_word(word_variants[0])
    return str([mark_word(word) for word in word_variants])

def isMonoSyllab(word_variants):
    return all([word.isMonoSyllab() for word in word_variants])

def mark_word(word):
    if word.isMonoSyllab():
        return word.getToken().upper()
    return ''.join([mark_syllable(syllable) for syllable in word.syllables()])


def mark_syllable(syllable):
    return syllable.str_orth().upper() if syllable.stressed else syllable.str_orth()


def mark_line(line):
    t = p.Text(line)
    words = t.words(flattenList=(not showAlternatives))
    if showAlternatives:
        return " ".join([mark_word_variants(word_variants) for word_variants in words])
    else:
        return " ".join([mark_word(word) for word in words])
    

@app.route("/", methods=['POST'])
def hello():
    content = request.data
    print "============================="
    print "content: "
    print content
    lines = [mark_line(line) for line in content.split('\n')]
    return '\n'.join(lines)

if __name__ == "__main__":
    app.run(host="localhost", port="5121")
