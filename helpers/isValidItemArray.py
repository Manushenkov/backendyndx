

from constants import CATEGORY, OFFER
from helpers.isValidUuid import isValidUuid


def isValidItemArray(items):
    for item in items:
        if not ("type" in item and "name" in item and "id" in item and "parentId" in item):
            return False

        if not isValidUuid(item["id"]):
            return False

        if not isinstance(item["name"], str):
            return False

        if not (item["type"] == OFFER or item["type"] == CATEGORY):
            return False

        if item["type"] == OFFER:
            if "price" not in item or item["price"] == None or not isinstance(item["price"], int) or item["price"] < 0:
                return False

    return True
