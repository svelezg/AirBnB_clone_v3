#!/usr/bin/python3
"""
Contains the App test
"""

import pep8
import unittest
import os
import tempfile
import pytest
from api.v1.app import app
from flask import Flask, Blueprint, render_template, abort, jsonify, make_response
from models import storage
from api.v1.views import app_views
from models.engine import db_storage


class TestDBStorageDocs(unittest.TestCase):
    def test_pep8_conformance_app(self):
        """Test that api/v1/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_app_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(app.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(app.__doc__) >= 1,
                        "file_storage.py needs a docstring")


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        # os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        # db.drop_all()
        # db.create_all()

    def tearDown(self):
        pass

    @app_views.route('/status', strict_slashes=False)
    def test_main_page(self):
        response = self.app.get('/status', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
