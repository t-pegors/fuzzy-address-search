from flask import Flask, render_template, request, jsonify
import webbrowser
import random
from io import StringIO
import threading
#from webtool import app

#from config import Config
from webtool.fuzzy_search import bag_of_ngrams, clean_address_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
import numpy as np

#from webtool import app
global file_extension
global df
#df = pd.DataFrame()
global columns

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    global file_extension
    file_extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# def transform(text_file_contents):
#     return text_file_contents.replace("=", ",")

@app.route('/')
@app.route('/index')
def main():
    return render_template('fuzzy_search.html')


@app.route('/_upload_file', methods=['POST'])
def upload_file():



    if 'input_file' not in request.files:
        resp = jsonify({'message': '<span style="color:red">No file part in the request</span>'})
        resp.status_code = 400
        return resp

    file = request.files.getlist('input_file')[0]

    if file and allowed_file(file.filename):
        stream = StringIO(file.stream.read().decode("UTF8"))
        global df
        df = pd.read_csv(stream, encoding='utf-8', dtype=str, error_bad_lines=False)
        columns = list(df.columns)

        resp = jsonify(message='File successfully uploaded: ' + str(len(df)) + ' rows found.',
                       columns=json.dumps(columns))
        resp.status_code = 201
        return resp

    else:
        resp = jsonify(message='<span style="color:red">Error uploading file</span>')
        resp.status_code = 400
        return resp


@app.route('/_build_vocab', methods=['POST'])
def build_vocab():
    global tfidf_matrix
    global vectorizer
    global column

    column = request.form['column']
    print('column:', column)

    if column:
        try:
            global df
            df = df.replace(np.nan, '', regex=True)
            vectorizer = TfidfVectorizer(min_df=1, encoding='utf-8', analyzer=bag_of_ngrams)
            vectorizer = vectorizer.fit(df[column])
            tfidf_matrix = vectorizer.transform(df[column])
            resp = jsonify({'message': 'Build complete.'})
            resp.status_code = 201
            return resp
        except:
            resp = jsonify({'message': '<span style="color:red">Build fail.</span>'})
            resp.status_code = 400
            return resp
    else:
        resp = jsonify({'message': '<span style="color:red">Build fail.</span>'})
        resp.status_code = 400
        return resp


@app.route('/_search', methods=['GET'])
def search():
    search_addresses = json.loads(request.args.get('address'))
    threshold = request.args.get('threshold')

    df_results_final = pd.DataFrame()

    for address in search_addresses:
        # get tf-idf scores for all words in search address
        address_vector = vectorizer.transform([address])
        # compare this search vector to all other vectors in matrix (cosine similarity)
        results_array = cosine_similarity(address_vector, tfidf_matrix)
        # add these scores as a column to the database
        df_results = df.copy()
        results_array = results_array[0] * 100  # turn scores into percents
        df_results.insert(loc=0, column='SIMILARITY_SCORE', value=results_array.round(2))
        df_results.insert(loc=1, column='SEARCH_ADDRESS', value=address)
        # only return those rows that scored above the requested threshold
        df_results = df_results[df_results['SIMILARITY_SCORE'] > int(threshold)].sort_values(by='SIMILARITY_SCORE',
                                                                                             ascending=False)

        df_results_final = df_results_final.append(df_results)

    #print(df_results_final)
    cols = list(df_results_final)
    cols.insert(2, cols.pop(cols.index(column)))
    #print(cols)
    #df_results_final = df_results_final.index[:, cols]

    if len(df_results_final) > 0:
        resp = df_results_final.to_json(orient='records')
        return resp
    else:
        resp = jsonify({'message': '<span style="color:red">Search fail.</span>'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':

    app.run(host='127.0.0.1', port='5000', debug=False)
