from mongoengine import Document, StringField,FloatField,IntField,DateTimeField,BooleanField
from datetime import datetime






class ZPointCollection(Document):
    point_set_name=StringField(required=True)
    price=FloatField(required=True)
    points=IntField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow) 
    image = StringField(default="https://default-image-url.com")
    is_adjustable=BooleanField(required=True)
    status=BooleanField(default=True)
