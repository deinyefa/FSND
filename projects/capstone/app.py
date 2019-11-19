import os
from flask import Flask, abort, jsonify, request
from models import setup_db, Actor, Movie, format_date
from flask_cors import CORS

QUESTIONS_PER_PAGE = 10


def paginate_response(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    responses = [response.format() for response in selection]

    return responses[start:end]


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.jinja_env.filters['date'] = format_date

    '''
    implement endpoint
        GET /actors
            it should be a public endpoint
        returns status code 200 and json {"success": True, "actors": actors}
        where actors is the list of actors paged by 10
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors')
    def get_actors():
        try:
            actors = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_response(request, actors)

            return jsonify({
                'actors': current_actors,
                'total_actors': len(Actor.query.all()),
                'success': True
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    implement endpoint
        POST /actors
            it should be a private endpoint
        returns status code 200 and json {"success": True, "actors": actors}
        where actors is the list of actors paged by 10
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()

        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)

        try:
            actor = Actor(
                name=actor_name,
                age=actor_age,
                gender=actor_gender
            )
            actor.insert()

            actors = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_response(request, actors)

            return jsonify({
                'actors': current_actors,
                'created': actor.id,
                'total_actors': len(Actor.query.all()),
                'success': True,
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    implement endpoint
        PATCH /actors/actor_id
            it should be a private endpoint
        returns status code 200 and json {"success": True, "actors": actors}
        where actors is the list of actors paged by 10
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        body = request.get_json()

        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            if actor_name:
                actor.name = actor_name
            if actor_age:
                actor.age = actor_age
            if actor_gender:
                actor.gender = actor_gender

            actor.update()

            return jsonify({
                'actor': actor.format(),
                'success': True
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    implement endpoint
        DELETE /actors/actor_id
            it should be a private endpoint
        returns status code 200 and json {"success": True, "actor": actor}
        where actors is the list of actors paged by 10
        or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()
            actors = Actor.query.order_by(Actor.id).all()

            return jsonify({
                'actors': paginate_response(request, actors),
                'deleted_actor': actor.format(),
                'success': True
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    implement endpoint
        GET /movies
            it should be a public route
        returns status code 200 and json {"success": True, "movies": movies}
        where movies is the list of movies paged by 10
        or appropriate status code indicating reason for failure
    '''
    @app.route('/movies')
    def get_movies():
        try:
            movies = Movie.query.order_by(Movie.id).all()

            return jsonify({
                "movies": paginate_response(request, movies),
                "total_movies": len(Movie.query.all()),
                "success": True
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    implement endpoint
        POST /movies
            it should be a private route
        returns status code 200 {"success":True, "movies":movies}
        where movies is a list of all movies pages in 10s
        or appropriate error code
    '''
    @app.route('/movies', methods=['POST'])
    def create_movies():
        body = request.get_json()
        movie_title = body.get('title', None)
        movie_release_date = body.get('release_date', None)

        try:
            movie = Movie(
                title=movie_title,
                release_date=movie_release_date
            )
            movie.insert()
            movies = Movie.query.order_by(Movie.id).all()

            return jsonify({
                "movies": paginate_response(request, movies),
                "total_movies": len(movies),
                "success": True
            })
        except Exception as e:
            print(e)
            abort(422)
            movie.rollback()

    '''
    implement endpoint
        PATCH /movies/movie_id
            it should be a private route
        return status code 200 {"success":True, "movie",movie}
        where movie is the updated movie
        or an appropriate error code
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def edit_movie(movie_id):
        body = request.get_json()
        movie_title = body.get('title', None)
        movie_release_date = body.get('release_date', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        try:

            if movie is None:
                abort(404)

            if movie_title:
                movie.title = movie_title
            if movie_release_date:
                movie.release_date = movie_release_date

            movie.update()

            return jsonify({
                "movie": movie.format(),
                "success": True
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    implement endpoint
        DELETE /movies/movie_id
            it should be a private route
        return status code 200 {"success":True, "movies":movies}
        where movies is the remaining movies after deletion pages 10
        or an appropriate error code
    '''
    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    def remove_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()
            movies = Movie.query.order_by(Movie.id).all()

            return jsonify({
                "movies": paginate_response(request, movies),
                "deleted_movie": movie.format(),
                "success": True
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/')
    def get_greeting():
        excited = 'true'
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
