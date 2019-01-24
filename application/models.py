from flask_sqlalchemy import SQLAlchemy
import app


db = SQLAlchemy(app)


class Immeubles(db.Model):
    listing_id = db.Column('immeubles_id', db.Integer, primary_key=True)
    listing_title = db.Column(db.String(200))
    listing_price = db.Column(db.String(200))
    listing_neighborhood = db.Column(db.String(200))
    link_to_listing = db.Column(db.String(200))
    listing_m2 = db.Column(db.String(200))
    listing_pieces = db.Column(db.String(200))

    def __init__(self, listing_title, listing_price, listing_m2, listing_pieces, listing_neighborhood, link_to_listing):
        self.listing_title = listing_title
        self.listing_price = listing_price
        self.listing_neighborhood = listing_neighborhood
        self.link_to_listing = link_to_listing
        self.listing_m2 = listing_m2
        self.listing_pieces = listing_pieces


db.create_all()
