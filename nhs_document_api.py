import json
from flask import Flask, request, jsonify

# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb

# import scraper
app = Flask(__name__)

# Initialize ChromaDB client and create/load a collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="nhs-files")




@app.route('/update_collection', methods=['GET'])
def update_collection_from_file():
    # Read data from the JSON file
    with open('nhs_data.json', 'r') as file:
        nhs_content = json.load(file)

    nhs_content_texts_list = []
    for item in nhs_content:
        content = item["content"]
        if isinstance(content, list):
            # If content is a list, join the elements into a single string
            content = " ".join(content)
        elif not isinstance(content, str):
            # If content is neither a list nor a string, convert it to string
            content = str(content)
        nhs_content_texts_list.append(content)
    nhs_content_urls_list = [{"url": item["url"]} for item in nhs_content]
    nhs_content_names_list = [item["name"] for item in nhs_content]

    # Here, you should add the code to update your collection
    # For example, if you're using a database or a search engine, you would insert or update the records here
    collection.add(
        documents=nhs_content_texts_list,
        metadatas=nhs_content_urls_list,
        ids=nhs_content_names_list
    )

    return jsonify({"message": "Collection updated from file"}), 200


@app.route('/query', methods=['GET'])
def query_collection():
    query_text = request.args.get('query')
    n_results = int(request.args.get('n_results', 2))
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)




# @app.route('/update_collection', methods=['POST'])
# def scrape_nhs_and_update_collection():  
#     # nhs_content format:
#     # [{"name":condition_name,"url":full_url,"content":section_texts}]
#     nhs_content = scraper.fetch_nhs_content()

#     nhs_content_texts_list = []
#     for item in nhs_content:
#         content = item["content"]
#         if isinstance(content, list):
#             # If content is a list, join the elements into a single string
#             content = " ".join(content)
#         elif not isinstance(content, str):
#             # If content is neither a list nor a string, convert it to string
#             content = str(content)
#         nhs_content_texts_list.append(content)
#     nhs_content_urls_list = [{"url":item["url"]} for item in nhs_content]
#     nhs_content_names_list = [item["name"] for item in nhs_content]

#     # print(nhs_content_texts_list)
#     collection.add(
#         documents=nhs_content_texts_list,
#         metadatas=nhs_content_urls_list,
#         ids=nhs_content_names_list
#     )
#     return jsonify({"message": "Collection updated"}), 200
