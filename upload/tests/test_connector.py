from upload.connector import ConnectorDSpaceREST
from upload.models import Community, Collection, Item,Bitstream
import unittest
from types import SimpleNamespace

URL_DSPACE = 'http://localhost:8080'
# Fill in your details here to be posted to the login form.
EMAIL = 'test@test.edu'
PASSWORD = 'admin'

class TestConnectorDSpaceRESTInit(unittest.TestCase):

    def test_init(self):
        """
        Check if the connector can be called

        :return:
        """
        with ConnectorDSpaceREST(URL_DSPACE) as connector:
            connector


class TestConnectorDSpaceREST(unittest.TestCase):

    def setUp(self) -> None:

        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)

    def tearDown(self) -> None:
        self.connector.close()

    def test_login(self):
        JSESSIONID = self.connector.login(EMAIL,
                             PASSWORD)

        self.assertTrue(JSESSIONID, 'Should return something')
        self.assertIsInstance(JSESSIONID, str, 'Should return the cookie session ID as a string')

    def test_get_communities(self):
        l = self.connector.get_communities()

        self.assertTrue(l, 'Should return something')


class TestConnectorDSpaceRESTAddItem(unittest.TestCase):

    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

    def tearDown(self) -> None:
        self.connector.close()

    def test_add_doc_classifier(self):
        d =     { "id":14301,
          "name":"2015 Annual Report",
          "handle":"123456789/13470",
          "type":"item",
          "link":"/rest/items/14301",
          "expand":["metadata","parentCollection","parentCollectionList","parentCommunityList","bitstreams","all"],
          "lastModified":"2015-01-12 15:44:12.978",
          "parentCollection":None,
          "parentCollectionList":None,
          "parentCommunityList":None,
          "bitstreams":None,
          "archived":"true",
          "withdrawn":"false"
        }

        collection0 = self.connector.get_collections()[0]
        collection_id = collection0.uuid

        if 0:
            item = Item(name='Document classification model for NBB vs Belgian Official Gazette. Tensorflow model.')
        else:
            item = SimpleNamespace(**d)

        r = self.connector.add_item(item,
                                    collection_id)

        self.assertTrue(r)


class TestConnectorDSpaceRESTAddBitstream(unittest.TestCase):

    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

    def tearDown(self) -> None:
        self.connector.close()

    def test_add_doc_classifier(self):
        bitstream = Bitstream(name='Document classification model for NBB vs Belgian Official Gazette. Tensorflow model.')

        r = self.connector.add_bitstream(bitstream)

        self.assertTrue(r)

