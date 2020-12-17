import numpy as np
import networkx as nx
import pyttsx3
import docx2txt
from difflib import SequenceMatcher


def text_to_speech(command):
    """
    General function to convert text to speech
    :param command: text (type:string)
    :return: speech
    """
    engine = pyttsx3.init()
    # engine.setProperty('voice', 'com.apple.speech.synthesis.voice.moira')
    engine.say(command)
    engine.runAndWait()


def read_article(file_name):
    """
    General function to read a text or a docs file.
    :param file_name: filename with path to be read.
    :return: sentences from the aricle
    """
    if file_name.endswith('.docs') or file_name.endswith('.doc') or file_name.endswith('.docx'):
        filedata = docx2txt.process(file_name).replace('\n', '. ')

    else:
        file = open(file_name, "r")
        filedata = file.read().replace('\n', '. ')
        file.close()
    article = filedata.split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


def build_similarity_matrix(sentences):
    """
    Compare each sentence to one another and form a similarity matrix
    :param sentences: Array of sentences present in the article
    :return: Similarity Matrix
    """
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:  # ignore if both are same sentences
                continue
            similarity_matrix[i][j] = similar(sentences[i], sentences[j])
    return similarity_matrix


def similar(string1, string2):
    """
    General function to compare similarity score using sequence matcher between 2 strings.

    :param string1: first string (type: string)
    :param string2: second string (type: string)

    :return: ratio of similarity (type: float)
    """
    return SequenceMatcher(None, string1, string2).ratio()


def generate_summary(file_name):
    """
    The main function to generate summary by finding similarity among sentences and ranking them
    :param file_name: filename and path
    :return: Summarized text
    """
    summarize_text = []
    sentences = read_article(file_name)
    if len(sentences) > 4:
        num_sentences = int(len(sentences) / 3)
    else:
        num_sentences = len(sentences)
    sentence_similarity_martix = build_similarity_matrix(sentences)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    for i in range(num_sentences):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    final_text = '. '.join(summarize_text)
    return final_text


def speak_out(file):
    """
    Uses text to speech to speak out the contents of a given file
    :param file: File path with filename(Type:String)
    :return: NA (calls text to speech)
    """
    f = open(file, 'r')
    text = f.read()
    f.close()
    text_to_speech(text)


def write_output(outfile):
    """
    General function to write the output to a file
    :param outfile: File path with filename(Type:String)
    :return: NA (just writes the file at the location)
    """
    f = open(outfile, 'w')
    f.write(op)
    f.close()


if __name__ == '__main__':
    input_file = 'news.txt'
    write_file = 'output.txt'

    op = generate_summary(input_file)
    write_output(write_file)
    speak_out(write_file)
