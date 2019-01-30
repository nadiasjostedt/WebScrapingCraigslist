from application import app
from application.database import Database
from flask import Flask, request, flash, url_for, redirect, render_template
import pandas as pd

db = Database()

n = db.read().shape[0] - 1
immeubles = db.read()

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html', df=db.read(), b=n )
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method != 'POST':
        return render_template('add.html')
    if request.method == 'POST':
        if not request.form['listing_title'] or not  request.form['listing_price'] or not  request.form['listing_m2'] or not  request.form['listing_pieces'] or not  request.form['listing_neighborhood'] or not  request.form['link_to_listing']:
            flash('Please enter all the fields', 'error')
        else:
            db.create(request.form['listing_title'], request.form['listing_price'], request.form['listing_neighborhood'], request.form['link_to_listing'], request.form['listing_m2'], request.form['listing_pieces'])


    return render_template('main.html', df=db.read(), b=n )

@app.route('/update', methods=['GET', 'POST'])
def update():
     if request.method == 'POST':
         query = (int(request.form['title_id']),
                  request.form['listing_title'],
                  request.form['listing_price'],
                  request.form['listing_neighborhood'],
                  request.form['link_to_listing'],
                  request.form['listing_m2'],
                  request.form['listing_pieces']
         )
         display_data = pd.DataFrame(data=db.update(*query), columns=db.column_names)
         return render_template('main.html', df=db.read(), b=n )
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
     db.delete(int(request.form['title_id_del']))

     return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
