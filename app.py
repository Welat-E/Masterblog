from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_blog_posts():
    with open("data.json", "r") as f:
        blog_posts = json.load(f)
    return blog_posts


def save_blog_posts(blog_posts):
    with open("data.json", "w") as f:
        json.dump(blog_posts, f, indent=4)

def fetch_post_by_id(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route("/")
def index():
    blog_posts = load_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = load_blog_posts()

    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        new_id = len(blog_posts) + 1

        new_post = {
            "id": new_id,
            "title": title,
            "author": author,
            "content": content
        }
        blog_posts.append(new_post)

        with open("data.json", "w") as f:
            json.dump(blog_posts, f, indent=4)
       
        return redirect(url_for('index'))
        
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_blog_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)

    with open("data.json", "w") as f:
        json.dump(blog_posts, f, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        blog_posts = load_blog_posts()
        for p in blog_posts:
            if p['id'] == post_id:
                p['title'] = title
                p['author'] = author
                p['content'] = content
                break

        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run()
