import sys
from flask import (
  abort,
  jsonify,
  render_template,
  request,
  flash,
  redirect, url_for
)
import logging
from logging import Formatter, FileHandler
from sqlalchemy import create_engine, text
from sqlalchemy.orm import load_only
from forms import *
from init import app, csrf
from models import *
from jinja_filters import format_datetime

app.jinja_env.filters['datetime'] = format_datetime


@app.route('/status')
def status():
    responseBody = {}
    error = False
    try:
        eng = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        conn = eng.connect()
        conn.close()
        responseBody['msg'] = "database is up"
    except Exception as e:
        error = True
        responseBody['msg'] = "database is down !"
        print(sys.exc_info())
    finally:
        if error:
            return jsonify(responseBody), 500
        else:
            return jsonify(responseBody)


@app.route('/')
def index():
    return render_template('pages/home.html')


@app.route('/items')
def items():
    form = ItemForm()
    items = Item.query.all()
    return render_template('pages/items.html', items=items, form=form)


@app.route('/items/search', methods=['POST'])
def search_items():
    form = ItemForm()
    search_term = request.form.get('search_term', '')
    items = Item.query.filter(Item.name.ilike('%'+search_term+'%')).all()
    response = {
      "count": 0,
      "data": []
    }
    for item in items:
        response["count"] += 1
        response["data"].append({
          "id": item.id,
          "name": item.name
        })
    return render_template(
      'pages/search_items.html',
      results=response,
      search_term=search_term,
      form=form
    )


@app.route('/items/<int:item_id>')
def show_item(item_id):
    form = ItemEditForm()
    # shows the item page with the given item_id
    item = Item.query.filter_by(id=item_id).first_or_404()
    return render_template('pages/show_item.html', item=item, form=form)


@app.route('/items/<int:item_id>/edit', methods=['GET'])
def edit_item(item_id):
    form = ItemEditForm()
    item = Item.query.filter_by(id=item_id).first_or_404()
    return render_template('forms/edit_item.html', form=form, item=item)


@app.route('/items/<int:item_id>/edit', methods=['POST'])
def edit_item_submission(item_id):
    form = ItemEditForm()
    if form.validate_on_submit():
        try:
            item = Item.query.filter_by(id=item_id).first_or_404()
            item.name = form.name.data
            item.properties = form.properties.data
            db.session.commit()
            # on successful db insert, flash success
            flash('Item ' + item.name + ' was successfully updated!')
            db.session.close()
            return redirect(url_for('show_item', item_id=item_id))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash(
              'An error occurred. Item ' +
              request.form.get("name") +
              ' could not be updated.'
            )
            return render_template('forms/edit_item.html', form=form)
    else:
        flash(form.errors)
        return render_template('forms/edit_item.html', form=form)


@app.route('/items/create', methods=['GET'])
def create_item_form():
    form = ItemForm()
    return render_template('forms/new_item.html', form=form)


@app.route('/items/create', methods=['POST'])
def create_item_submission():
    form = ItemForm()
    if form.validate_on_submit():
        try:
            item = Item(
              name=form.name.data,
              properties=form.properties.data,
            )
            db.session.add(item)
            db.session.commit()
            # on successful db insert, flash success
            flash('Item ' + item.name + ' was successfully listed!')
            db.session.close()
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash(
              'An error occurred. Item ' +
              request.form.get("name") +
              ' could not be listed.')
            return render_template('forms/new_item.html', form=form)
    else:
        flash(form.errors)
        return render_template('forms/new_item.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
          '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.run()
# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
