import json
#from sentence_transformers import SentenceTransformer, util

#model = SentenceTransformer('all-MiniLM-L6-v2')

def convert_json_to_dict():
    with open('jobs.json', 'r') as file:
        data = json.load(file)
    qualification_dict = {}

    for job_title, job_info in data.items():
        qualification_dict[job_title] = job_info['Qualifications:']

    print(qualification_dict['Lucid Vision Labs Inc%%Junior Software Developer Co-op'])


def main():
    convert_json_to_dict()


if __name__ == "__main__":
    main()