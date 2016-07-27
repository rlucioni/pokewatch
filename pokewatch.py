import requests

coordinates = ('42.364399098341', '-71.102836263782')


def build_url(coordinates):
    return 'https://pokevision.com/map/data/{}/{}'.format(*coordinates)


def get_data(coordinates):
    url = build_url(coordinates)
    # TODO: Timeout and other error handling.
    response = requests.get(url)

    return response.json()
