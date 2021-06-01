import warnings
from types import SimpleNamespace
from typing import List, Union, Callable

import requests
from lxml import etree

from .models import Community, Collection, Item, ItemCreate, Bitstream

RESPONSE_TEST = 'REST api is running.'


class XMLResponse:
    def __init__(self, root_element: etree._Element):
        self.root = root_element
        self.tree = root_element.getroottree()

    @classmethod
    def fromstring(cls, string: bytes):
        return cls(etree.fromstring(string))

    def get_uuid(self):
        return self._get('UUID')

    def get_link(self):
        return self._get('link')

    def get_handle(self):
        return self._get('handle')

    def _get(self, key: str):
        return self.root.xpath(f'//{key}')[0].text

    def tostring(self):
        return etree.tostring(self.root,
                              pretty_print=True,
                              xml_declaration=True,
                              standalone=True,
                              encoding='UTF-8').decode('UTF-8')

    def print(self):
        return print(self.tostring())

    def __str__(self):
        return self.tostring()


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

    def get_items(self,
                  limit=100,
                  ):

        # Get all
        data = []
        i = 0
        while True:
            offset = i * limit
            # Default value of limit is 100
            response = self.get(self.url_items + f'?offset={offset:d}&limit={limit:d}')
            data_i = response.json()

            if len(data_i):
                data.extend(data_i)
            else:
                break

            i += 1

        l = list(map(lambda d: Item(**d), data))

        return l

    def add_item(self, item: ItemCreate,
                 collection_id: int) -> XMLResponse:

        url = self.url_collections + f'/{collection_id}/items'

        data = vars(item)

        # data.pop('__initialised__')

        # metadata = [{"key": "dc.title", "value": "Test 20201124 REST 2"},
        #             {"key": "dc.contributor.author", "value": "Einstein, Albert"},
        #             {"key": "dc.description.abstract", "value": "ABSTRACT 2"}
        #             ]

        class DCMetadata:
            def __init__(self,
                         title: Union[list, str],
                         author: Union[list, str] = None,
                         ):

                self.title = title
                self.author = author

            def get_metadata(self):

                metadata = []

                def add_title(title):
                    metadata.append({"key": "dc.title", "value": title})

                def add_author(author):
                    metadata.append({"key": "dc.contributor.author", "value": author})

                def foo(el, add_i: Callable[[str], None]):

                    if el is None:
                        return

                    l = el if isinstance(el, (list, tuple)) else [el]
                    for el_i in l:
                        add_i(el_i)

                foo(self.title, add_title)
                foo(self.author, add_author)

                return metadata

        dcm = DCMetadata(title=item.name)

        metadata = dcm.get_metadata()

        data['metadata'] = metadata

        response = self.post(url, json=data)

        if response.ok:
            xml = XMLResponse.fromstring(response.content)
        else:
            raise ConnectionError(response.content)

        return xml

    def get_bitstreams(self):
        response = self.get(self.url_bitstreams)
        data = response.json()

        l = _get_list_simple_namespace(data)
        return l

    def add_bitstream(self, bitstream: Bitstream):
        data = vars(bitstream)

        response = self.post(self.url_bitstreams, data=data)

        return  # TODO
