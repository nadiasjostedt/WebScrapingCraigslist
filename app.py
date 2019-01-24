from application import app
from application.database import Database
from flask import Flask, request, flash, url_for, redirect, render_template
import pandas as pd

db = Database()

@app.route('/', methods=['GET', 'POST'])
def main():
    html_data = db.read().to_html()
    print(html_data)
    return render_template('index.html', immeubles=html_data)


# @app.route('/update', methods=['GET', 'POST'])
# def update():
#     if request.method == 'POST':
#         query = (request.form['ID'],
#                  request.form['listing_title'],
#                  request.form['listing_price'],
#                  request.form['listing_neighborhood'],
#                  request.form['link_to_listing'],
#                  request.form['listing_m2'],
#                  request.form['listing_pieces']
#         )
#         display_data = pd.DataFrame(data=db.update(*query), columns=db.column_names)
#         return render_template('main.html', immeubles=immeubles.query.all())
#     else:
#         title_id_up = request.args.get("title_id_up")
#         listing_title_up = request.args.get("listing_title_up")
#         listing_price_up = request.args.get('listing_price_up')
#         listing_m2_up = request.args.get('listing_m2_up')
#         listing_pieces_up = request.args.get('listing_pieces_up')
#         listing_neighborhood_up = request.args.get('listing_neighborhood_up')
#         link_to_listing_up = request.args.get('link_to_listing_up')
#         return render_template('update.html', title_id_up=title_id_up, listing_title_up=listing_title_up, listing_price_up=listing_price_up, listing_m2_up=listing_m2_up, listing_pieces_up=listing_pieces_up, listing_neighborhood_up=listing_neighborhood_up, link_to_listing_up=link_to_listing_up)
#
#
# @app.route("/delete", methods=["POST"])
# def delete():
#     appart = immeubles.query.filter_by(listing_id=request.form['title_id_del']).first()
#     db.session.delete(appart)
#     db.session.commit()
#     return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
