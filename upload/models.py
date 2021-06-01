"""
https://wiki.lyrasis.org/display/DSDOC6x/REST+API#RESTAPI-Model-Objectdatatypes
"""

from typing import List

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class Community:
    """
    { "id":456,
      "name":"Reports Community",
      "handle":"10766/10213",
      "type":"community",
      "link":"/rest/communities/456",
      "expand":["parentCommunity","collections","subCommunities","logo","all"],
      "logo":null,
      "parentCommunity":null,
      "copyrightText":"",
      "introductoryText":"",
      "shortDescription":"Collection contains materials pertaining to the Able Family",
      "sidebarText":"",
      "countItems":3,
      "subcommunities":[],
      "collections":[]
    }
    """

    id: int
    name: str
    # handle,
    # type,
    # link,
    # expand,
    # logo,
    # parentCommunity,
    # copyrightText,
    # introductoryText,
    # shortDescription,
    # sidebarText,
    # countItems,
    # subcommunities,
    # collections


@dataclass
class Collection:
    """
    { "id":730,
      "name":"Annual Reports Collection",
      "handle":"10766/10214",
      "type":"collection",
      "link":"/rest/collections/730",
      "expand":["parentCommunityList","parentCommunity","items","license","logo","all"],
      "logo":null,
      "parentCommunity":null,
      "parentCommunityList":[],
      "items":[],
      "license":null,
      "copyrightText":"",
      "introductoryText":"",
      "shortDescription":"",
      "sidebarText":"",
      "numberItems":3
    }
    """

    uuid: str
    name: str
    handle: str
    type: str
    expand: List[str]
    parentCommunityList: list
    items: list
    copyrightText: str
    introductoryText: str
    shortDescription: str
    sidebarText: str
    numberItems: int
    link: str

    logo: type = None
    parentCommunity: type = None
    license: type = None


# TODO change name?
class ItemCreate(BaseModel):
    """
    Creating a new item, before posting to OAI-PMH
    """

    name: str

    bitstreams: List[str] = None

    def __init__(self, *args, **kwargs):
        super(ItemCreate, self).__init__(*args, **kwargs)


class Item(ItemCreate, BaseModel):
    """
    { "id":14301,
      "name":"2015 Annual Report",
      "handle":"123456789/13470",
      "type":"item",
      "link":"/rest/items/14301",
      "expand":["metadata","parentCollection","parentCollectionList","parentCommunityList","bitstreams","all"],
      "lastModified":"2015-01-12 15:44:12.978",
      "parentCollection":null,
      "parentCollectionList":null,
      "parentCommunityList":null,
      "bitstreams":null,
      "archived":"true",
      "withdrawn":"false"
    }
    """

    # id: int
    uuid: str
    link: str
    handle: str
    lastModified: str

    archived: bool  # True
    withdrawn: bool  # False  # str

    # TODO fix? Expected that every item has a name.
    name: str = None

    type: str  # "item"  # Should be "item"

    parentCollection: str = None
    parentCollectionList: list = None
    parentCommunityList: list = None

    bitstreams: str = None

    expand: List[str]  # = ["metadata", "parentCollection", "parentCollectionList", "parentCommunityList", "bitstreams",
    #   "all"
    #   ]

    # TODO check if this can be added or not:
    # metadata: list=None  # This one was not defined in the model


@dataclass
class Bitstream:
    """
    { "id":47166,
      "name":"appearance and physiology 100 percent copied from wikipedia.pdf",
      "handle":null,
      "type":"bitstream",
      "link":"/rest/bitstreams/47166",
      "expand":["parent","policies","all"],
      "bundleName":"ORIGINAL",
      "description":"",
      "format":"Adobe PDF",
      "mimeType":"application/pdf",
      "sizeBytes":129112,
      "parentObject":null,
      "retrieveLink":"/bitstreams/47166/retrieve",
      "checkSum":{"value":"62778292a3a6dccbe2662a2bfca3b86e","checkSumAlgorithm":"MD5"},
      "sequenceId":1,
      "policies":null
    }
    """

    # id: int
    name: str
