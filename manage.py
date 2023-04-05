#!/usr/bin/python3
"""deployment"""


def deploy():
    """Run deployment tasks"""
    from nurupishi import create_app, db
    from models import User, Bookmarks, Favorites, SearchHistory, Recipes

    app = create_app()
    app.app_context().push()
    db.create_all()

    stamp()
    migrate()
    upgrade()

deploy()

