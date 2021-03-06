#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import logging
from logging import FileHandler, Formatter
from itertools import groupby

# import babel
# import dateutil.parser
import datetime
from flask import (Response, flash, redirect, render_template, request,
                   url_for)
# from flask_migrate import Migrate
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form

from forms import *

from models import (Venue, Artist, Show, format_datetime, app, db)


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    venues = Venue.query.order_by('id').all()
    data = []

    for key, venues in groupby(sorted(venues, key=lambda v: [v.city, v.state]), key=lambda v: [v.city, v.state]):
        
        data.append({
            'city': key[0],
            'state': key[1],
            'venues': [{'id': venue.id, 'name': venue.name, 'num': len(venue.shows)} for venue in list(venues)]
        })
        print((data))

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', '')
    search_query = Venue.query.filter(
        Venue.name.ilike('%' + search_term + '%')).all()

    resultsData = []

    venue_shows = Venue.query.join('shows').all()

    for search in search_query:
        resultsData.append({
            "id": search.id,
            "name": search.name,
            "num_upcoming_shows": len(venue_shows)
        })

    response = {
        "count": len(search_query),
        "data": resultsData
    }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    active_venue = Venue.query.get(venue_id)
    venue_shows = Show.query.filter_by(venue_id=venue_id).order_by('id').all()

    past_shows = []
    upcoming_shows = []

    now = datetime.utcnow()

    for venue_show in venue_shows:
        artist = Artist.query.get(venue_show.artist_id)

        if venue_show.start_time:
            if now > venue_show.start_time:
                past_shows.append({
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": venue_show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
            else:
                upcoming_shows.append({
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": venue_show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })

    data = {
        "id": venue_id,
        "name": active_venue.name,
        "genres": active_venue.genres.split(','),
        "address": active_venue.address,
        "city": active_venue.city,
        "state": active_venue.state,
        "phone": active_venue.phone,
        "website": active_venue.website,
        "facebook_link": active_venue.facebook_link,
        "seeking_talent": active_venue.seeking_talent,
        "seeking_description": active_venue.seeking_description,
        "image_link": active_venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    data = Venue()
    error = False
    try:
        # TODO: insert form data as a new Venue record in the db, instead
        data.name = request.form['name']
        data.city = request.form['city']
        data.state = request.form['state']
        data.address = request.form['address']
        data.phone = request.form['phone']
        data.genres = ','.join(request.form.getlist('genres'))
        data.facebook_link = request.form['facebook_link']

        db.session.add(data)
        db.session.commit()
        # TODO: modify data to be the data object returned from db insertion
    except:
        error = True
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        flash('An error occured! Venue ' +
              request.form['name'] + ' could not be added.')

    finally:
        # on successful db insert, flash success
        if error == False:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    active_venue = Venue.query.get(venue_id)

    try:
        db.session.delete(active_venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        flash('Oh oh! Something went wrong when we tried deleting Venue ' +
              active_venue.name + ' please try again later.')
    finally:
        error = False
        flash('Venue ' +
              active_venue.name + ' has been sucessfully deleted.')

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = []
    artists = Artist.query.order_by('id').all()
    for artist in artists:
        data.append({
            'id': artist.id,
            'name': artist.name
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term', '')
    search_query = Artist.query.filter(
        Artist.name.ilike('%' + search_term + '%')).all()

    resultsData = []

    artist_shows = Artist.query.join('shows').all()

    for search in search_query:
        resultsData.append({
            "id": search.id,
            "name": search.name,
            "num_upcoming_shows": len(artist_shows)
        })

    response = {
        "count": len(search_query),
        "data": resultsData
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    active_artist = Artist.query.get(artist_id)
    artist_shows = Show.query.filter_by(
        artist_id=artist_id).order_by('id').all()

    past_shows = []
    upcoming_shows = []

    now = datetime.utcnow()

    for artist_show in artist_shows:
        venue = Venue.query.get(artist_show.venue_id)

        if artist_show.start_time:
            if now > artist_show.start_time:
                past_shows.append({
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": artist_show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
            else:
                upcoming_shows.append({
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": artist_show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })

    data = {
        "id": active_artist.id,
        "name": active_artist.name,
        "genres": active_artist.genres.split(','),
        "city": active_artist.city,
        "state": active_artist.state,
        "phone": active_artist.phone,
        "website": active_artist.website,
        "facebook_link": active_artist.facebook_link,
        "seeking_venue": active_artist.seeking_venue,
        "seeking_description": active_artist.seeking_description,
        "image_link": active_artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    active_artist = Artist.query.get(artist_id)

    form.name.default = active_artist.name
    form.city.default = active_artist.city
    form.state.default = active_artist.state
    form.phone.default = active_artist.phone
    form.genres.default = active_artist.genres.split(',')
    form.facebook_link.default = active_artist.facebook_link

    artist = {
        "id": active_artist.id,
        "name": active_artist.name
    }

    form.process()
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False
    active_artist = Artist.query.get(artist_id)

    try:
        active_artist.name = request.form['name']
        active_artist.city = request.form['city']
        active_artist.state = request.form['state']
        active_artist.phone = request.form['phone']
        active_artist.genres = ','.join(request.form.getlist('genres'))
        active_artist.facebook_link = request.form['facebook_link']

        db.session.commit()
    except:
        error = True
        db.session.rollback()

        flash('An error occurred. Artist ' +
              active_artist.name + ' could not be listed.')
    finally:
        if error == False:
            flash('Artist ' + request.form['name'] +
                  ' was successfully updated!')

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    active_venue = Venue.query.get(venue_id)

    form.name.default = active_venue.name
    form.city.default = active_venue.city
    form.state.default = active_venue.state
    form.address.default = active_venue.address
    form.phone.default = active_venue.phone
    form.genres.default = active_venue.genres.split(',')
    form.facebook_link.default = active_venue.facebook_link

    venue = {
        "id": active_venue.id,
        "name": active_venue.name
    }
    form.process()
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    error = False
    active_venue = Venue.query.get(venue_id)

    try:
        active_venue.name = request.form['name']
        active_venue.city = request.form['city']
        active_venue.state = request.form['state']
        active_venue.address = request.form['address']
        active_venue.phone = request.form['phone']
        active_venue.genres = ','.join(request.form.getlist('genres'))
        active_venue.facebook_link = request.form['facebook_link']

        db.session.commit()
    except:
        error = True
        db.session.rollback()

        flash('An error occurred. Venue ' +
              active_venue.name + ' could not be listed.')
    finally:
        if error == False:
            flash('Venue ' + request.form['name'] +
                  ' was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    data = Artist()
    error = False
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    try:
        data.name = request.form['name']
        data.city = request.form['city']
        data.state = request.form['state']
        data.phone = request.form['phone']
        data.genres = ','.join(request.form.getlist('genres'))
        data.facebook_link = request.form['facebook_link']

        db.session.add(data)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' +
              data.name + ' could not be listed.')
    finally:
        # on successful db insert, flash success
        if error == False:
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
    return render_template('pages/home.html')

    # TODO: modify data to be the data object returned from db insertion


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = []
    shows = Show.query.order_by('id').all()
    for show in shows:

        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    data = Show()
    error = False
    # TODO: insert form data as a new Show record in the db, instead
    try:
        data.start_time = request.form['start_time']
        data.artist_id = request.form['artist_id']
        data.venue_id = request.form['venue_id']

        db.session.add(data)
        db.session.commit()
    except:
        # TODO: on unsuccessful db insert, flash an error instead.
        error = True
        flash('An error occurred. This show could not be listed.')
    finally:
        # on successful db insert, flash success
        if error == False:
            flash('Show was successfully listed!')

    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


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
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
