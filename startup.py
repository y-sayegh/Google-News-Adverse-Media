"""
Azure App Service startup file
This file is used by Azure to start the Flask application
"""
from app import app

if __name__ == "__main__":
    app.run()
