import runme
import networkx as nx
from flask import Flask, request

app = Flask(__name__)


def generate_summary(text):
    """
    The main function to generate summary by finding similarity among sentences and ranking them
    :param file_name: filename and path
    :return: Summarized text
    """
    summarize_text = []
    sentences = clean(text)
    num_sentences = int(len(sentences) / 2)
    sentence_similarity_martix = runme.build_similarity_matrix(sentences)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    for i in range(num_sentences):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    final_text = '. '.join(summarize_text)
    return final_text


def clean(filedata):
    filedata = filedata.replace('\n', '. ')
    article = filedata.split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


@app.route('/summarize',methods=['POST'])
def summarize():
    text = request.args.get('data')
    final = generate_summary(text)
    return final
