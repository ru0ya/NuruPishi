#!/usr/bin/python3
from nurupishi import create_app


if __name__ == "__main__":
    app = create_app(app_id="APP_ID", app_key="APP_KEY")
    app.run(debug=True)
