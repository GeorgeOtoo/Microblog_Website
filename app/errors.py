from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() #failed database session do not interfere with db access
    return render_template('500.html'), 500 #error code number for database