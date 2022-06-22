from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response

from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from datetime import datetime
from constants import DAY, ERROR_400, ERROR_404, OFFER

from helpers.isDatetimeValid import isDatetimeValid
from helpers.isValidItemArray import isValidItemArray
from helpers.isValidUuid import isValidUuid
from helpers.itemToJson import itemToJson

app = Flask(__name__)
# conn_url = 'postgresql+psycopg2://yourUserDBName:yourUserDBPassword@yourDBDockerContainerName/yourDBName'

# docker run --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String)
    parentId = db.Column(db.String(40), ForeignKey('item.id'), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    type = db.Column(db.String)
    date = db.Column(db.String)
    children = relationship('Item', cascade="all, delete-orphan",
                            backref=backref('parent', remote_side=[id])
                            )

    def __init__(self, id, name, parentId, price, type, date):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.price = price
        self.type = type
        self.date = date


@app.route('/nodes/<id>', methods=["GET"])
def nodes(id):
    if not isValidUuid(id):
        return ERROR_400, 400

    item = Item.query.get(id)
    if item is None:
        return ERROR_404, 404

    return itemToJson(item)


@app.route('/sales', methods=["GET"])
def sales():
    date = request.args.get('date')

    if not isDatetimeValid(date):
        return ERROR_400, 400

    requestedDateIso = date
    requestedDateDatetime = datetime.fromisoformat(date.replace('Z', '+00:00'))
    requestedDateDayBefore = datetime.isoformat(requestedDateDatetime - DAY)

    items = Item.query.filter(
        Item.type == OFFER, Item.date <= requestedDateIso, Item.date >= requestedDateDayBefore).all()

    res = [itemToJson(item) for item in items]

    return {"items": res}


@app.route('/delete/<id>', methods=["DELETE"])
def deleteNode(id):
    if not isValidUuid(id):
        return ERROR_400, 400

    item = db.session.get(Item, id)
    if item is None:
        return ERROR_404, 404

    db.session.delete(item)
    db.session.commit()

    return '', 200


@app.route('/imports', methods=['POST'])
def imports():
    data = request.get_json()
    items = data["items"]
    date = data["updateDate"]

    if not (isDatetimeValid(date) and isValidItemArray(items)):
        return ERROR_400, 400

    for importedItem in items:
        id = importedItem["id"]
        name = importedItem["name"]
        parentId = importedItem["parentId"]

        price = None
        if 'price' in importedItem:
            price = importedItem["price"]

        type = importedItem["type"]

        existingItem = Item.query.get(id)

        if existingItem is None:
            data = Item(id, name, parentId, price, type, date)
            db.session.add(data)
        else:
            existingItem.name = name
            existingItem.parentId = parentId
            existingItem.price = price
            existingItem.date = date

    db.session.commit()

    for importedItem in items:
        item = Item.query.get(importedItem["id"]).parent

        while item is not None:
            item.date = date
            item = item.parent

    db.session.commit()

    return Response("", status=200, mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.run(port=80)
