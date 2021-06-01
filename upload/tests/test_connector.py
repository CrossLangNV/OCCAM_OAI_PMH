import unittest

from upload.connector import ConnectorDSpaceREST, XMLResponse
from upload.models import ItemCreate, BitstreamCreate

"""
Confluence documentation:
https://wiki.lyrasis.org/display/DSDOC6x/REST+API
"""

URL_DSPACE = "http://localhost:8080"
# Fill in your details here to be posted to the login form.
EMAIL = "test@test.edu"
PASSWORD = "admin"


class TestConnectorDSpaceRESTInit(unittest.TestCase):
    def test_init(self):
        """
        Check if the connector can be called and doesn't crash

        :return:
        """
        with ConnectorDSpaceREST(URL_DSPACE) as connector:
            print(connector)


class TestConnectorDSpaceREST(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)

    def tearDown(self) -> None:
        self.connector.close()

    def test_login(self):
        JSESSIONID = self.connector.login(EMAIL, PASSWORD)

        self.assertTrue(JSESSIONID, "Should return something")
        self.assertIsInstance(JSESSIONID, str, "Should return the cookie session ID as a string")

    def test_get_communities(self):
        l = self.connector.get_communities()
        self.assertTrue(len(l), "Should return something")

    def test_get_collections(self):
        l = self.connector.get_collections()
        self.assertTrue(len(l), "Should return something")

    def test_get_items(self):
        l = self.connector.get_items()
        self.assertTrue(len(l), "Should return something")

    def test_get_bitstreams(self):
        l = self.connector.get_bitstreams()
        self.assertTrue(len(l), "Should return something")


class TestConnectorDSpaceRESTAddItem(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

    def tearDown(self) -> None:
        self.connector.close()

    def test_add_doc_classifier(self):
        collection0 = list(filter(lambda x: "Demo 3" in x.name, self.connector.get_collections()))[0]
        collection_id = collection0.uuid

        def get_item_create():
            d = {
                "name": "2015 Annual Report",
                # # TODO can be added, but don't know how.
                # "bitstreams": [1],
            }
            item = ItemCreate(**d)
            return item

        item = get_item_create()

        items_before = self.connector.get_items()

        xml = self.connector.add_item(item, collection_id)
        print(xml)

        items_after = self.connector.get_items()

        with self.subTest("One item is added"):
            self.assertEqual(len(items_before) + 1, len(items_after))

        get_uuid = lambda item: item.uuid
        l_uuid_before = list(map(get_uuid, items_before))
        l_uuid_after = list(map(get_uuid, items_after))
        l_diff = list(filter(lambda item: get_uuid(item) not in l_uuid_before, items_after))

        with self.subTest("One new item"):
            self.assertEqual(len(l_diff), 1)

        last_item = l_diff[0]

        with self.subTest("Equal text"):
            self.assertEqual(last_item.name, xml._get("name"))

        with self.subTest("Equal uuid"):
            self.assertEqual(last_item.uuid, xml.get_uuid())

        with self.subTest("Equal link"):
            self.assertEqual(last_item.link, xml.get_link())

        with self.subTest("Equal handle"):
            self.assertEqual(last_item.handle, xml.get_handle())

        for key in vars(item).keys():  # d.keys():
            with self.subTest(f"Equal item: {key}"):
                value_last_item = getattr(last_item, key)
                value_item = getattr(item, key)

                self.assertEqual(value_last_item, value_item)




class TestConnectorDSpaceRESTAddBitstream(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

    def tearDown(self) -> None:
        self.connector.close()

    def test_add(self):

        collection0 = list(filter(lambda x: "Demo 3" in x.name, self.connector.get_collections()))[0]
        collection_id = collection0.uuid

        bitstream = BitstreamCreate(
            name="Document classification model for NBB vs Belgian Official Gazette. Tensorflow model."
        )

        item0 = ItemCreate(name='temp item')
        xml = self.connector.add_item(item0, collection_id)
        item0_uuid = xml.get_uuid()
        try:
            r = self.connector.add_bitstream(bitstream, item0_uuid)

            self.assertTrue(r)

        finally:
            self.connector.delete_item(item0_uuid)


class TestConnectorDSpaceRESTdeleteItem(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

    def tearDown(self) -> None:
        self.connector.close()

    def test_delete(self):
        # Get all items that I want to delete

        items = self.connector.get_items()

        def f_filter(item):
            return (item.name is None) or ("2015 Annual Report" in item.name)

        for item in filter(f_filter, items):
            self.connector.delete_item(item.uuid)

        items_after = self.connector.get_items()
        items_after_filter = list(filter(f_filter, items_after))

        self.assertTrue(items_after, "Should maintain some items")
        self.assertFalse(items_after_filter, "Should have removed all filted ones")


class TestXMLResponse(unittest.TestCase):
    def test_str(self):
        response_content = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><item><link>/rest/items/ebb7f718-88f5-4083-a8fd-c915787c5015</link><expand>metadata</expand><expand>parentCollection</expand><expand>parentCollectionList</expand><expand>parentCommunityList</expand><expand>bitstreams</expand><expand>all</expand><handle>123456789/67</handle><name>Test 20201124 REST 2</name><type>item</type><UUID>ebb7f718-88f5-4083-a8fd-c915787c5015</UUID><archived>true</archived><lastModified>Mon May 31 10:02:24 UTC 2021</lastModified><withdrawn>false</withdrawn></item>'

        xml = XMLResponse.fromstring(response_content)

        s_xml = str(xml)

        def _concatenate_lines(s):
            return "".join(map(str.strip, s_xml.splitlines()))

        def _ingore_single_double_quotes(s):
            return s.replace("'", '"')

        self.assertEqual(
            _ingore_single_double_quotes(_concatenate_lines(s_xml)),
            _ingore_single_double_quotes(response_content.decode("UTF-8")),
        )
