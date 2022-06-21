
import math
from constants import CATEGORY


def itemToJson(item):
    dict = {"id": item.id, "name": item.name,
            "type": item.type, "parentId": item.parentId, "date": item.date, "price": item.price}

    if item.type == CATEGORY:
        dict["children"] = []
        for child in item.children:
            dict["children"].append(itemToJson(child))

        prices = 0
        sum = 0

        stack = [dict]

        while len(stack) > 0:
            cur = stack.pop()

            for child in cur["children"]:
                if child["type"] == CATEGORY:
                    stack.append(child)
                else:
                    prices += 1
                    sum += child["price"]

        if (prices > 0):
            dict["price"] = math.floor(sum / prices)
        else:
            dict["price"] = None

    else:
        dict["children"] = None

    return dict
