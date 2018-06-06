import prosodic as p
from flask import Flask, request

app = Flask(__name__)


def mark_word_variants(word_variants):
    for word in word_variants:
        if word.isMonoSyllab():
            return [word.getToken()]
        else:
            return [mark_word(word) for word in word_variants]


def mark_word(word):
    if word.isMonoSyllab():
        return word.getToken()
    return ''.join([mark_syllable(syllable) for syllable in word.syllables()])


def mark_syllable(syllable):
    return syllable.str_orth().upper() if syllable.stressed else syllable.str_orth()


def mark_line(line):
    t = p.Text(line)
    words = t.words(flattenList=True)
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
