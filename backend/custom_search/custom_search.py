import requests
import urllib.parse
import json

def get_results_from_sites(query, language, sites, start):

    # For non-restricted search.
    request_url = 'https://www.googleapis.com/customsearch/v1/?'

    # Append the API key from Google to the request url.
    # api_key = 'AIzaSyALJ62P1LfEWV27MXQ4tMwoyARpL_3OHXk' # Should be separated.
    api_key = 'AIzaSyAiAuRbe4tqM1ku1f27ncecwIvhVbXkCYQ' # new key.
    request_url = request_url + f'key={api_key}'

    # Append the search engine ID for the custom search engine.
    search_engine_id = '0c51adcadf5f24e19' # Should be separated.
    request_url = request_url + f'&cx={search_engine_id}'

    # Append the list of websites to the query.
    for i in range(len(sites)):
        query = query + f' site:{sites[i]}'
        if i < len(sites)-1: # Do not add an 'OR' after the last website.
            query = query + ' OR'

    # Append the encoded query.
    encoded_query = urllib.parse.quote(query)
    request_url = request_url + f'&q={encoded_query}'

    # Append the language choice.
    request_url = request_url + f'&lr=lang_{language}'

    # Append the specific required fields (for performance).
    # request_url = request_url + f'&fields=items(title,link,pagemap/metatags(og:image,article:published_time,og:site_name,og:description,sailthru.title,author))'
    request_url = request_url + f'&fields=items(title,link,snippet)'

    # Append the start index.
    request_url = request_url + f'&start={start}'

    # Print the final URL.
    print('\n' + request_url + '\n')

    # Send the GET request.
    response = requests.get(request_url)

    # If the resonse is not OK, return.
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return

    # Load response items.
    response_text_json = json.loads(response.text)
    response_text_json_items = response_text_json["items"]

    # Return the response items.
    return response_text_json_items

# Test
# sites = [
#     'theguardian.com',
#     'nytimes.com',
#     'bbc.com',
#     'cnn.com',
#     'huffpost.com',
#     'foxnews.com',
#     'nbcnews.com',
#     'washingtonpost.com',
#     'wsj.com',
#     'theverge.com'
# ]
# results = get_results_from_sites('python','en',sites)
# for result in results:
#     print(f"title: {result['title']}")
#     print(f"link: {result['link']}")
#     for key in result['pagemap']['metatags'][0].keys():
#         print(f"{key}: {result['pagemap']['metatags'][0][key]}")
#     print("\n")    