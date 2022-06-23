from marshmallow import Schema, fields

class ConsumerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    country = fields.Str(required=True)
    city = fields.Str(required=True)
    adress = fields.Str(required=True)
    category = fields.Str(required=True)
    
class ProviderSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    country = fields.Str()
    city = fields.Str()
    adress = fields.Str()
    category = fields.Str(required=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class OfferSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    date_offer = fields.DateTime()
    offered_price = fields.Float()
    currency = fields.Str()
    contact_person = fields.Str()
    provider = fields.Str()

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    date_start = fields.DateTime()
    date_end = fields.DateTime()
    contact_person = fields.Str()
    phone = fields.Str()
    costs = fields.Float()
    currency = fields.Str()
    consumer = fields.Str()
