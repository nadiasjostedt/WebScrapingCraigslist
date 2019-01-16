from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from crawler import Crawler as Crawl
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immeuble.sqlite3'
app.config['SECRET_KEY'] = "xdfghfg5456rftghret45etgt"
db = SQLAlchemy(app)


class Immeubles(db.Model):
    ID = db.Column('immeubles_id', db.Integer, primary_key=True)
    TITRE = db.Column(db.String(200))
    PRIX = db.Column(db.String(200))
    ARR = db.Column(db.String(200))
    LINK = db.Column(db.String(200))
    M2 = db.Column(db.String(200))
    PIECES = db.Column(db.String(200))

    def __init__(self, listing_title, listing_price, listing_m2,
                 listing_pieces, listing_neighborhood, link_to_listing):
        self.listing_title = listing_title
        self.listing_price = listing_price
        self.listing_neighborhood = listing_neighborhood
        self.link_to_listing = link_to_listing
        self.listing_m2 = listing_m2
        self.listing_pieces = listing_pieces


class CRUD(object):

    def __init__(self, app=app, db=db):
        self.request = request
        self.app = app
        self.db = db
        self.column_names = ['listing_title', 'listing_price', 'listing_m2',
                             'listing_pieces', 'listing_neighborhood',
                             'link_to_listing']
        self.crawler = Crawl()

    def initiate_database(self):
        data = self.crawler.get_site_data()
        engine = create_engine('sqlite://', echo=False)
        params = {
            'name': 'immeubles',
            'con': engine,
            'if_exists': 'replace',
            'index': True,
            'index_label': 'id'
        }
        data.to_sql(**params)

    @app.route('/create', methods=['GET', 'POST'])
    def create(self):
        if self.request.method == 'POST':
            if not self.request.form['listing_title'] or not self.request.form['listing_price'] or not self.request.form[
                'listing_m2'] or not self.request.form['listing_pieces'] or not self.request.form['listing_neighborhood'] or not \
                    self.request.form['link_to_listing']:
                flash('Please enter all the fields', 'error')
            else:
                new_record = Immeubles(*[self.request.form[column] for column in self.column_names])
                db.session.add(new_record)
                db.session.commit()
                flash('Record was successfully added: {}'.format(new_record))
        return render_template('main.html', immeubles=Immeubles.query.all())

    @app.route('/update', methods=['GET', 'POST'])
    def update(self):
        if request.method == 'POST':
            if not request.form['listing_title'] or not request.form['listing_price'] or not request.form[
                'listing_m2'] or not request.form['listing_pieces'] or not request.form['listing_neighborhood'] or not \
            request.form['link_to_listing']:
                flash('Please enter all the fields', 'error')
            else:
                appart = Immeubles.query.filter_by(listing_id=request.form['title_id']).first()
                appart.listing_title = request.form['listing_title']
                appart.listing_price = request.form['listing_price']
                appart.listing_m2 = request.form['listing_m2']
                appart.listing_pieces = request.form['listing_pieces']
                appart.listing_neighborhood = request.form['listing_neighborhood']
                appart.link_to_listing = request.form['link_to_listing']
                db.session.commit()
                return render_template('main.html', immeubles=Immeubles.query.all())
        else:
            title_id_up = request.args.get("title_id_up")
            listing_title_up = request.args.get("listing_title_up")
            listing_price_up = request.args.get('listing_price_up')
            listing_m2_up = request.args.get('listing_m2_up')
            listing_pieces_up = request.args.get('listing_pieces_up')
            listing_neighborhood_up = request.args.get('listing_neighborhood_up')
            link_to_listing_up = request.args.get('link_to_listing_up')
            return render_template('update.html', title_id_up=title_id_up, listing_title_up=listing_title_up,
                                   listing_price_up=listing_price_up, listing_m2_up=listing_m2_up,
                                   listing_pieces_up=listing_pieces_up, listing_neighborhood_up=listing_neighborhood_up,
                                   link_to_listing_up=link_to_listing_up)

    @app.route("/delete", methods=["POST"])
    def delete(self):
        appart = Immeubles.query.filter_by(listing_id=request.form['title_id_del']).first()
        self.db.session.delete(appart)
        db.session.commit()
        return redirect("/")
