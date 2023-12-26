from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL
import shortuuid
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'ABcjbeqruyhcbveHDBUdsc@&*hg2yedbwycb' 
Bootstrap5(app)

# creating database
db = SQLAlchemy(app)

class Database(db.Model):
    # a 6 letter unique id shall be given to each
    id = db.Column(db.String(6), primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)

with app.app_context():
    db.create_all()


# creating flask form
class ShortenForm(FlaskForm):
    long_url = StringField('Enter URL:', validators=[URL('Please enter a valid url')])
    submit = SubmitField('Shorten URL')

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShortenForm()
    if form.validate_on_submit():
        long_url = form.long_url.data
        # generating the unique 6 letters id to identify the data
        short_url = shortuuid.uuid()[:6]

        new_url_set = Database(id=short_url, long_url=long_url)
        db.session.add(new_url_set)
        db.session.commit()

        # creating the short url (clickable link in this case)
        short_url = url_for('redirect_to_long_url', short_url=short_url, _external=True)
        

        return render_template('index.html', form=form, short_url=short_url)

    return render_template('index.html', form=form)

# redirect the final url
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    mapped_url = db.session.execute(db.select(Database).where(Database.id==short_url)).scalar()
    if mapped_url:
        long_url = mapped_url.long_url
        return redirect(long_url)
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=False)
