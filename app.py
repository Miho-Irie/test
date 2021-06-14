from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tea.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100))
    year = db.Column(db.Integer)
    season = db.Column(db.String(10))
    kind = db.Column(db.String(10))
    detail = db.Column(db.String(200))
    img = db.Column(db.String(30))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.date).all()
        return render_template('index.html', posts=posts)

    else:
        date = request.form.get('date')
        name = request.form.get('name')
        place = request.form.get('place')
        year = request.form.get('year')
        season = request.form.get('season')
        kind = request.form.get('kind')
        detail = request.form.get('detail')
        img = request.form.get('img')

        date = datetime.strptime(date, '%Y-%m-%d')
        new_post = Post(date=date, name=name, place=place, year=year, season=season, kind=kind, detail=detail, img=img)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)

    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        post.name = request.form.get('name')
        post.place = request.form.get('place')
        post.year = request.form.get('year')
        post.season = request.form.get('season')
        post.kind = request.form.get('kind')
        post.detail = request.form.get('detail')
        post.img = request.form.get('img')

        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)