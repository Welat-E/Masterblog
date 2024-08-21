from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_blog_posts():
    """Load blog posts from the JSON file."""
    with open("data.json", "r") as f:
        return json.load(f)


def save_blog_posts(blog_posts):
    """Save blog posts to the JSON file."""
    with open("data.json", "w") as f:
        json.dump(blog_posts, f, indent=4)


def fetch_post_by_id(post_id):
    """Fetch a single post by its ID."""
    blog_posts = load_blog_posts()
    return next((post for post in blog_posts if post["id"] == post_id), None)


@app.route("/")
def index():
    """Render the index page with all blog posts."""
    blog_posts = load_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Handle adding a new blog post."""
    if request.method == "POST":
        blog_posts = load_blog_posts()
        new_post = {
            "id": len(blog_posts) + 1,
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "content": request.form.get("content"),
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """Handle deleting a blog post."""
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Handle updating a blog post."""
    post = fetch_post_by_id(post_id)
    if not post:
        return "Post not found", 404

    if request.method == "POST":
        post["title"] = request.form.get("title")
        post["author"] = request.form.get("author")
        post["content"] = request.form.get("content")
        blog_posts = load_blog_posts()
        for p in blog_posts:
            if p["id"] == post_id:
                p.update(post)
                break
        save_blog_posts(blog_posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run()
