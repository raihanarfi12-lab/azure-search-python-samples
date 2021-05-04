import logging
import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from shared_code import azure_config

environment_vars = azure_config()

#curl --header "Content-Type: application/json" \
#  --request POST \
#  --data '{"q":"code","top":"5", "suggester":"sg"}' \
#  http://localhost:7071/api/Suggest

# Set Azure Search endpoint and key
endpoint = f'https://{environment_vars["search_service_name"]}.search.windows.net'
key = environment_vars["search_api_key"]

# Your index name
index_name = 'good-books'

# Create Azure SDK client
search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

def main(req: func.HttpRequest) -> func.HttpResponse:

    # variables sent in body
    req_body = req.get_json()
    q = req_body.get('q')
    top = req_body.get('top')
    suggester = req_body.get('suggester')

    if q:
        logging.info(f"/Suggest q = {q}")
        suggestions = search_client.suggest(search_text="code", suggester_name="sg", top=5)
        return func.HttpResponse(body=f"{suggestions}", status_code=200)
    else:
        return func.HttpResponse(
             "No query param found.",
             status_code=200
        )