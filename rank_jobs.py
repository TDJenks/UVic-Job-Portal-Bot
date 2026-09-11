import json
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Returns cosine similarity of a and b
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Returns a match score based on qualification embeddings and cv embeddings using cosine similarity
def match_score(q_emb, cv_emb):
    similarity_scores = []
    for qual in q_emb:
        similarity = -1
        for experience in cv_emb:
            similarity = max(similarity, cosine_sim(qual, experience))
        similarity_scores.append(similarity)

    i = 0
    total = 0
    for score in similarity_scores:
        total += score
        i += 1

    match_score = total/i
    return match_score        

# Creates a map: job -> qualifications
def init_qualification_dict():
    with open('jobs.json', 'r') as file:
        data = json.load(file)
    qualification_dict = {}
    for job_title, job_info in data.items():
        qualification_dict[job_title] = job_info['Qualifications:']
    return qualification_dict

# Creates embeddings from cv using sentence transformer model
def init_cv_embeddings():
    cv_sentences = []
    with open("CV.txt", "r") as cv:
        for sentence in cv.read().split("\n"):
            if re.search(r"\w", sentence):
                cv_sentences.append(sentence)
    return model.encode(cv_sentences)

def main():
    q_dict = init_qualification_dict()
    cv_emb = init_cv_embeddings()
    score_dict = {}

    for job, quals in q_dict.items():
        qual_sentences = []
        for sentence in quals.split('\n'):
            if re.search(r"\w", sentence):
                qual_sentences.append(sentence)
        qual_embeddings = model.encode(qual_sentences)
        score = match_score(qual_embeddings, cv_emb)
        score_dict[job] = score

    rankings = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
    with open("ranks.txt", "w", encoding="utf-8") as f:
        for key, value in rankings.items():
            f.write(f"{key}: {value}\n")


    


if __name__ == "__main__":
    main()