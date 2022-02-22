import urllib.request
import json
import copy


# Enter below the Github username you want to get the E-Mail address from.
github_username = 'dabeaz'

URL = f"https://api.github.com/users/{github_username}/events/public"


def get_authors(input_data):
    """ Use recursion to find 'author' in input_data and return a list with all matches. """
    authors = []
    if isinstance(input_data, dict):
        for key in input_data:
            if key == "author":
                authors.append(input_data[key])

            elif isinstance(input_data[key], (list, dict)):
                authors.extend(get_authors(input_data[key]))

    elif isinstance(input_data, list):
        for elem in input_data:
            authors.extend(get_authors(elem))

    return authors


response = urllib.request.urlopen(URL)
response.text = response.read()
github_data = json.loads(response.text)


# Fetch data with our function get_authors()
authors_list = get_authors(github_data)


authors_dict = {}

for i in authors_list:
    # Some users could have multiple e-mail addresses, so take emails as keys for authors_dict instead of the names.
    authors_dict.update({i['email']: i['name']})


# Delete all entries containing '@users.noreply.github.com'
newDict_copy = copy.copy(authors_dict)  # create a shallow copy to be able do delete while iterating

for x in newDict_copy.keys():
    if '@users.noreply.github.com' in x:
        del authors_dict[x]


# Print results 🤗
if authors_dict:
    print(authors_dict)
else:
    print("This user hasn't uploaded anything or is smart enough to hide the email-address (possible via the settings).")
