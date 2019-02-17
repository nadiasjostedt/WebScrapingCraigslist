from application import app
from application.database import Database
from flask import request, flash, redirect, render_template
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--num_to_render',
                    default=50,
                    help="Number of records to render")
parser.add_argument('--save',
                    default=True,
                    help="True or False, save database")
args = vars(parser.parse_args())
print('args are : {}'.format(args))


db = Database()


def export_data():
    if args['save']:
        print('Saving apartment data...')
        db.export_to_csv(db.data)
        db.export_to_json(db.data)
    else:
        print("'Saving option is turned off. Run script with '--save=True'")


@app.route('/', methods=['GET', 'POST'])
def main():
    b = min(args['num_to_render'], db.data.shape[0])
    return render_template('main.html', df=db.read(), b=b)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = (  # prixmin, prixmax, m2min, m2max, piecesmin, piecesmax
            int(request.form['pricemin']),
            int(request.form['pricemax']),
            int(request.form['m2min']),
            int(request.form['m2max']),
            int(request.form['piecesmin']),
            int(request.form['piecesmax'])
        )
        df = db.search(*query)
    else:
        df = db.read()

    if request.form['export'] == 'export csv and Json':
        export_data()

    b = min(args['num_to_render'], df.shape[0])

    return render_template('main.html', df=df, b=b)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if not request.form['listing_title'] or not \
                request.form['listing_price'] or not \
                request.form['listing_m2'] or not \
                request.form['listing_pieces'] or not \
                request.form['listing_neighborhood'] or not \
                request.form['link_to_listing']:
            flash('Please enter all the fields', 'error')
        else:
            # titre, prix, arr, link, m2, pieces
            query = (request.form['listing_title'],
                     request.form['listing_price'],
                     request.form['listing_neighborhood'],
                     request.form['link_to_listing'],
                     request.form['listing_m2'],
                     request.form['listing_pieces'])

            db.create(*query)
            b = min(args['num_to_render'], db.data.shape[0])

            return render_template('main.html', df=db.data, b=b)
    else:
        return render_template('add.html')


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
        db.update(*query)
        b = min(args['num_to_render'], db.data.shape[0])
        return render_template('main.html', df=db.data, b=b)
    else:
        query = {
            'title_id_up': request.args.get("title_id_up"),
            'listing_title_up': request.args.get("listing_title_up"),
            'listing_price_up': request.args.get('listing_price_up'),
            'listing_m2_up': request.args.get('listing_m2_up'),
            'listing_pieces_up': request.args.get('listing_pieces_up'),
            'listing_neighborhood_up': request.args.get('listing_neighborhood_up'),
            'link_to_listing_up': request.args.get('link_to_listing_up')
        }
        return render_template('update.html', **query)


@app.route("/delete", methods=["POST"])
def delete():
    db.delete(int(request.form['title_id_del']))
    return redirect("/")


if __name__ == '__main__':
    print('Starting up application...')
    app.run(debug=False)
