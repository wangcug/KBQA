from entityextraction import crf
import jieba


# 问句实体抽取
def word_split(sentence: str, model: crf.CRFmodel):
    """
    Split sentence into words and extract entity labels using CRF model

    Args:
        sentence (str): Input question sentence
        model: Loaded CRF model for entity recognition

    Returns:
        tuple: (word_list, label_list) where each is a list of extracted entities and their labels
    """
    # Split sentence into character list
    char_list = [char for char in sentence]

    # Predict entity labels using CRF model
    label_list = model.test([char_list])[0]

    # Filter out characters with 'O' (non-entity) label
    filtered_pairs = [(char, label) for char, label in zip(char_list, label_list) if label != 'O']

    # Group consecutive characters into entities based on IOB tags
    entities, labels = [], []
    current_entity = ""

    relation_type_list = ['AT', 'CB', 'LI', 'FI', 'HM', 'HE', 'IF', 'IA', 'IR']

    for i, (char, label) in enumerate(filtered_pairs):
        tag_prefix, tag_type = label.split('-') if '-' in label else (label, '')

        # Handle current character based on its IOB tag
        if i < len(filtered_pairs) - 1:
            next_prefix = filtered_pairs[i + 1][1].split('-')[0] if '-' in filtered_pairs[i + 1][1] else \
                filtered_pairs[i + 1][1]

            if tag_prefix == 'B' and next_prefix == 'I':
                # Start of multi-character entity
                current_entity += char
            elif tag_prefix == 'I' and next_prefix == 'I':
                # Continue multi-character entity
                current_entity += char
            elif tag_prefix == 'I' and next_prefix == 'B':
                # End of multi-character entity
                current_entity += char
                entities.append(current_entity)
                labels.append(tag_type)
                current_entity = ""
            elif tag_prefix == 'B' and next_prefix == 'B':
                # Single-character entity
                entities.append(char)
                labels.append(tag_type)
        else:
            # Handle last character in the list
            if tag_prefix == 'I':
                current_entity += char
                entities.append(current_entity)
                labels.append(tag_type)
            else:
                entities.append(char)
                labels.append(tag_type)

    for i in range(len(labels)-1):
        if labels[i] in relation_type_list and labels[i+1] not in relation_type_list:
            labels[i], labels[i+1] = labels[i+1], labels[i]
            entities[i], entities[i + 1] = entities[i + 1], entities[i]

    return entities, labels


def fuzzy_matching(entity_list):
    """
    Perform fuzzy matching against a dictionary to find best-matching entity

    Args:
        entity_list (list): List of extracted entity words

    Returns:
        str: Best-matching entity from dictionary
    """
    if not entity_list:
        raise ValueError('No entity words matched!')

    # Load entity dictionary
    with open('./dict/entity_name.txt', 'r', encoding='utf-8') as f:
        entity_dict = [line.strip() for line in f]

    # Calculate matching scores for each dictionary entry
    match_scores = []
    for dict_entry in entity_dict:
        dict_chars = set(dict_entry)
        match_count = sum(1 for char in entity_list[0] if char in dict_chars)

        # Calculate normalized scores to avoid division by zero
        score1 = (len(dict_entry) + 1) / (match_count + 1)
        score2 = (len(entity_list[0]) + 1) / (match_count + 1)

        # Combine scores inversely
        match_scores.append(1 / (score1 + score2))

    # Return dictionary entry with the highest match score
    max_index = match_scores.index(max(match_scores)) if match_scores else -1
    return entity_dict[max_index] if max_index >= 0 else ""


def classify_question_type(question):
    """
    Classify question as factual or judgmental based on keyword dictionary

    Args:
        question (str): Input question

    Returns:
        bool: True for factual questions, False for judgmental questions
    """
    # Load question keyword dictionary
    with open('./dict/question_dic.txt', 'r', encoding='utf-8') as f:
        question_keywords = [line.strip() for line in f]

    # Load keywords into jieba for better segmentation
    jieba.load_userdict('./dict/question_dic.txt')

    # Segment question using jieba
    words = jieba.cut(question)

    # Check for presence of judgmental keywords
    for word in words:
        if word in question_keywords:
            return False

    return True
