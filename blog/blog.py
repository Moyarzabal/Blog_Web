from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)

@app.before_first_request
def setup():
    db.create_all()

@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('blog_index.html', articles=articles)

@app.route('/article/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        article = Article(title=title, body=body)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_article.html')

@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = Article.query.get(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.body = request.form['body']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_article.html', article=article)

@app.route('/article/<int:article_id>/delete', methods=['POST'])
def delete_article(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8080, debug=True)
