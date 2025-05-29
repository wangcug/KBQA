def load_data(filename):
    """Load data from file and split into sentences.

    Args:
        filename: Path to input file

    Returns:
        List of sentences where each sentence is a list of word/label pairs
    """
    f = open(filename, 'r', encoding='utf-8')
    datalist = list()
    datalists = list()

    for line in f:
        line_str = line.strip().split()

        if len(line_str) == 2:
            datalist.append([line_str[0], line_str[1]])
        elif len(line_str) == 1:
            datalist.append([line_str[0]])
        else:
            datalists.append(datalist)
            datalist = []

    if len(datalist) > 0:
        datalists.append(datalist)

    return datalists


def word2feature(sent, i):
    """Generate feature dictionary for a single word.

    Args:
        sent: List of word/label pairs
        i: Index of current word

    Returns:
        Feature dictionary with context information
    """
    word = sent[i][0]
    feature = {
        'bias:': 1.0,
        'word:': word,
        'word.isdigit():': word.isdigit(),
    }

    # Previous words features
    if i > 0:
        word1 = sent[i - 1][0]
        words = word1 + word
        feature.update({
            '-1word:': word1,
            '-1words:': words,
            '-1word.isdigit():': word1.isdigit(),
        })
    else:
        feature['BOS'] = True

    if i > 1:
        word2 = sent[i - 2][0]
        word1 = sent[i - 1][0]
        words = word2 + word1 + word
        feature.update({
            '-2:word': word2,
            '-2:words': words,
            '-2:word.isdigit()': word2.isdigit(),
        })

    if i > 2:
        word3 = sent[i - 3][0]
        word2 = sent[i - 2][0]
        word1 = sent[i - 1][0]
        words = word3 + word2 + word1 + word
        feature.update({
            '-3:word': word3,
            '-3:words': words,
            '-3:word.isdigit()': word3.isdigit(),
        })

    # Next words features
    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        words = word + word1
        feature.update({
            '+1:word': word1,
            '+1:words': words,
            '+1:word.isdigit()': word1.isdigit(),
        })
    else:
        feature['EOS'] = True

    if i < len(sent) - 2:
        word2 = sent[i + 2][0]
        word1 = sent[i + 1][0]
        words = word + word1 + word2
        feature.update({
            '+2:word': word2,
            '+2:words': words,
            '+2:word.isdigit()': word2.isdigit(),
        })

    if i < len(sent) - 3:
        word3 = sent[i + 3][0]
        word2 = sent[i + 2][0]
        word1 = sent[i + 1][0]
        words = word + word1 + word2 + word3
        feature.update({
            '+3:word': word3,
            '+3:words': words,
            '+3:word.isdigit()': word3.isdigit(),
        })

    return feature


def sent2feature(sent):
    """Convert sentence to feature list.

    Args:
        sent: List of word/label pairs

    Returns:
        List of feature dictionaries for each word
    """
    return [word2feature(sent, i) for i in range(len(sent))]


def sent2label(sent):
    """Extract labels from sentence.

    Args:
        sent: List of word/label pairs

    Returns:
        List of labels
    """
    return [ele[-1] for ele in sent]


def word_split(sentence, model):
    """Split sentence into words based on model predictions.

    Args:
        sentence: Input sentence string
        model: Trained model for word segmentation

    Returns:
        List of segmented words
    """
    sent_list = []
    for word in sentence:
        sent_list.append(word)

    labellist = model.test([sent_list])

    # Remove elements labeled as 'O'
    word_label = list(zip(sent_list, labellist[0]))
    word_label_wash = []

    for each in word_label:
        if each[1] != 'O':
            word_label_wash.append(each)

    # Segment words based on B-I labels
    word = ""
    wordlist = []

    for i in range(len(word_label_wash)):
        # print(each[1])
        if i < len(word_label_wash) - 1:
            t0 = word_label_wash[i][1].split('-')[0]
            t1 = word_label_wash[i + 1][1].split('-')[0]

            if (t0 == 'B' and t1 == 'I') or (t0 == 'I' and t1 == 'I'):
                word += word_label_wash[i][0]
            elif (t0 == 'I' and t1 == 'B'):
                word += word_label_wash[i][0]
                wordlist.append(word)
                word = ""
            elif (t0 == 'B' and t1 == 'B'):
                wordlist.append(word_label_wash[i][0])

        if i == len(word_label_wash) - 1:
            # t_1 = word_label_wash[i - 1][1].split('-')[0]
            t0 = word_label_wash[i][1].split('-')[0]

            if t0 == 'I':
                word += word_label_wash[i][0].split('-')[0]
                wordlist.append(word)
            else:
                wordlist.append(word_label_wash[i][0])

    return wordlist
