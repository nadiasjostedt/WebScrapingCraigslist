from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immeuble.sqlite3'
app.config['SECRET_KEY'] = "xdfghfg5456rftghret45etgt"

db = SQLAlchemy(app)


class immeubles(db.Model):
    listing_id = db.Column('immeubles_id', db.Integer, primary_key=True)
    listing_title = db.Column(db.String(200))
    listing_price = db.Column(db.Float)
    listing_m2 = db.Column(db.Integer)
    listing_pieces = db.Column(db.Integer)
    listing_neighborhood = db.Column(db.String(200))
    link_to_listing = db.Column(db.String(200))

    def __init__(self, listing_title, listing_price, listing_m2, listing_pieces, listing_neighborhood, link_to_listing):
        self.listing_title = listing_title
        self.listing_price = listing_price
        self.listing_m2 = listing_m2
        self.listing_pieces = listing_pieces
        self.listing_neighborhood = listing_neighborhood
        self.link_to_listing = link_to_listing


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