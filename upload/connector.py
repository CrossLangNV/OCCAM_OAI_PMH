import warnings
from types import SimpleNamespace
from typing import List

import requests

from .models import Community, Collection, Item, Bitstream

RESPONSE_TEST = 'REST api is running.'


class ConnectorDSpaceREST(requests.Session):
    """
    Connector to the DSpace REST API

    Make sure to close connection.
    Example:
    `
    with ConnectorDSpaceREST() as connector:
        connector.login(email, password)
    `

    """

    def __init__(self, url_dspace: str):
        """

        :param url_dspace: url to dspace server. E.g. 'http://test.dspace.com'
        """
        super(ConnectorDSpaceREST, self).__init__()

        self.url_rest = url_dspace + '/rest'  # DSpace REST API
        response_test = requests.get(self.url_rest + '/test')

        if response_test.text != RESPONSE_TEST:
            warnings.warn(f'url_dspace is expected to be incorrect. {self.url_rest} should lead to the rest API.',
                          UserWarning)

        self.url_communities = self.url_rest + '/communities'
        self.url_collections = self.url_rest + '/collections'
        self.url_items = self.url_rest + '/items'
        self.url_bitstreams = self.url_rest + '/bitstreams'

    def login(self, email: str, password: str) -> str:
        """ Needed when editing the elements (post, put, delete)

        :param email:
        :param password:
        :return: a JSESSIONID as string
        """
        response = self.post(self.url_rest + '/login', data={
            'email': email,
            'password': password
        })

        JSESSIONID = response.cookies.get('JSESSIONID')
        return JSESSIONID

    def get_communities(self) -> List[SimpleNamespace]:
        response = self.get(self.url_communities)
        data = response.json()

        l = list(map(lambda d: Community(**d), data))
        return l

    def add_community(self):
        response = self.post(self.url_communities)

        return  # TODO

    def get_collections(self):
        response = self.get(self.url_collections)
        data = response.json()

        l = list(map(lambda d: Collection(**d), data))
        return l

    def add_collection(self, collection: Collection):
        return

    def get_items(self):
        response = self.get(self.url_items)
        data = response.json()

        l = _get_list_simple_namespace(data)
        return l

    def add_item(self, item: Item,
                 collection_id: int):
        data = vars(item)

        url = self.url_collections + f'/{collection_id}/items'

        # TODO change

        # data =        {"metadata":
        #      {"dc.title": "Test 20201124 REST 2",
        #       "dc.contributor.author": "Einstein, Albert",
        #       "dc.description.abstract":  "ABSTRACT 2"
        #       }
        #  }
        #
        # data =              {"dc.title": "Test 20201124 REST 2",
        #       "dc.contributor.author": "Einstein, Albert",
        #       "dc.description.abstract":  "ABSTRACT 2"
        #       }

        body = {"metadata":
                    [{"key": "dc.title",
                      "value": "Test 20201124 REST 2"}, {"key": "dc.contributor.author", "value": "Einstein, Albert"},
                     {
                         "key": "dc.description.abstract", "value": "ABSTRACT 2"}]}


        response = self.post(url, json=body)
        return

    def get_bitstreams(self):
        response = self.get(self.url_bitstreams)
        data = response.json()

        l = _get_list_simple_namespace(data)
        return l

    def add_bitstream(self, bitstream: Bitstream):
        data = vars(bitstream)

        response = self.post(self.url_bitstreams, data=data)

        return  # TODO
