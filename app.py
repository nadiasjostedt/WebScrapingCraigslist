from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, MetaData, Column, String, Integer
from crawler import Crawler

app = Flask(__name__)
engine = create_engine("sqlite:///immeuble.sqlite3")  # Access the DB Engine
if not engine.dialect.has_table(engine, 'immeubles'):  # If table don't exist, Create.
    metadata = MetaData(engine)
    # Create a table with the appropriate Columns
    Table('immeubles', metadata,
          Column('immeubles_id', Integer, primary_key=True, nullable=False),
          Column('listing_title', String), Column('listing_price', String),
          Column('listing_m2', String), Column('listing_pieces', String),
          Column('listing_neighborhood', String),Column('link_to_listing', String))
    # Implement the creation
    metadata.create_all()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immeuble.sqlite3'
app.config['SECRET_KEY'] = "xdfghfg5456rftghret45etgt"
with engine.connect() as con:
    rs = con.execute('DELETE from immeubles')
    con.closed

db = SQLAlchemy(app)
c= Crawler()
df = c.get_site_data()
class immeubles(db.Model):
    listing_id = db.Column('immeubles_id', db.Integer, primary_key=True) #title, price, m2_and_peices, neighborhood, link
    listing_title = db.Column(db.String(200))
    listing_price = db.Column(db.String(200))
    listing_m2 = db.Column(db.String(200))
    listing_pieces = db.Column(db.String(200))
    listing_neighborhood = db.Column(db.String(200))
    link_to_listing = db.Column(db.String(200))

    def __init__(self, listing_title, listing_price, listing_m2, listing_pieces, listing_neighborhood, link_to_listing):
        self.listing_title = listing_title
        self.listing_price = listing_price
        self.listing_m2 = listing_m2
        self.listing_pieces = listing_pieces
        self.listing_neighborhood = listing_neighborhood
        self.link_to_listing = link_to_listing

for i in range(50):
    immeuble = immeubles(df.iat[i, 0], df.iat[i, 1].replace('€', ''), df.iat[i, 4], df.iat[i, 5], df.iat[i, 2], df.iat[i, 3] )
    db.session.add(immeuble)
    db.session.commit()
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method != 'POST':
        return render_template('add.html')
    if request.method == 'POST':
        if not request.form['listing_title'] or not  request.form['listing_price'] or not  request.form['listing_m2'] or not  request.form['listing_pieces'] or not  request.form['listing_neighborhood'] or not  request.form['link_to_listing']:
            flash('Please enter all the fields', 'error')
        else:
            immeuble = immeubles(request.form['listing_title'], request.form['listing_price'], request.form['listing_m2'], request.form['listing_pieces'], request.form['listing_neighborhood'], request.form['link_to_listing'])

            db.session.add(immeuble)
            db.session.commit()
            flash('Record was successfully added')
    return render_template('main.html', immeubles=immeubles.query.all())


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if not request.form['listing_title'] or not  request.form['listing_price'] or not  request.form['listing_m2'] or not  request.form['listing_pieces'] or not  request.form['listing_neighborhood'] or not  request.form['link_to_listing']:
            flash('Please enter all the fields', 'error')
        else:
            immeuble = immeubles(request.form['listing_title'], request.form['listing_price'], request.form['listing_m2'], request.form['listing_pieces'], request.form['listing_neighborhood'], request.form['link_to_listing'])

            db.session.add(immeuble)
            db.session.commit()
            flash('Record was successfully added')
    return render_template('main.html', immeubles=immeubles.query.all())

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        if not request.form['listing_title'] or not  request.form['listing_price'] or not  request.form['listing_m2'] or not  request.form['listing_pieces'] or not  request.form['listing_neighborhood'] or not  request.form['link_to_listing']:
            flash('Please enter all the fields', 'error')
        else:
            #immeuble = immeubles(request.form['listing_title'], request.form['listing_price'], request.form['listing_m2'], request.form['listing_pieces'], request.form['listing_neighborhood'], request.form['link_to_listing'])
            appart = immeubles.query.filter_by(listing_id=request.form['title_id']).first()
            appart.listing_title = request.form['listing_title']
            appart.listing_price = request.form['listing_price']
            appart.listing_m2 = request.form['listing_m2']
            appart.listing_pieces = request.form['listing_pieces']
            appart.listing_neighborhood = request.form['listing_neighborhood']
            appart.link_to_listing = request.form['link_to_listing']
            db.session.commit()
            return render_template('main.html', immeubles=immeubles.query.all())
    else:
        title_id_up = request.args.get("title_id_up")
        listing_title_up = request.args.get("listing_title_up")
        listing_price_up = request.args.get('listing_price_up')
        listing_m2_up = request.args.get('listing_m2_up')
        listing_pieces_up = request.args.get('listing_pieces_up')
        listing_neighborhood_up = request.args.get('listing_neighborhood_up')
        link_to_listing_up = request.args.get('link_to_listing_up')
        return render_template('update.html', title_id_up=title_id_up, listing_title_up=listing_title_up, listing_price_up=listing_price_up, listing_m2_up=listing_m2_up, listing_pieces_up=listing_pieces_up, listing_neighborhood_up=listing_neighborhood_up, link_to_listing_up=link_to_listing_up)

@app.route("/delete", methods=["POST"])
def delete():
    appart = immeubles.query.filter_by(listing_id=request.form['title_id_del']).first()
    db.session.delete(appart)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)