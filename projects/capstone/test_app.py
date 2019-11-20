import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class ActorTestCase(unittest.TestCase):
    """This test case represents tests for Actor endpoints."""

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = 'casting_agency_test'
        self.db_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(
            os.path.join(self.db_dir, self.database_name)
        )

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_actor = {
            "name": "Tonto Dikeh",
            "age": 40,
            "gender": "female"
        }

    def tearDown(self):
        pass

    def get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))


if __name__ == "__main__":
    unittest.main()
