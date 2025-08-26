from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BlogPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost

post_schema = BlogPostSchema()
posts_schema = BlogPostSchema(many=True)


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not data or not data.get("title") or not data.get("content") or not data.get("category"):
        return jsonify({"error": "Missing required fields"}), 400

    tags = ",".join(data.get("tags", []))
    new_post = BlogPost(
        title=data["title"],
        content=data["content"],
        category=data["category"],
        tags=tags
    )
    db.session.add(new_post)
    db.session.commit()
    return post_schema.jsonify(new_post), 201

@app.route("/posts", methods=["GET"])
def get_posts():
    term = request.args.get("term")
    if term:
        posts = BlogPost.query.filter(
            (BlogPost.title.ilike(f"%{term}%")) |
            (BlogPost.content.ilike(f"%{term}%")) |
            (BlogPost.category.ilike(f"%{term}%"))
        ).all()
    else:
        posts = BlogPost.query.all()
    return posts_schema.jsonify(posts), 200


@app.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    post = BlogPost.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return post_schema.jsonify(post), 200


@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    post = BlogPost.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    post.category = data.get("category", post.category)
    post.tags = ",".join(data.get("tags", post.tags.split(",")))

    db.session.commit()
    return post_schema.jsonify(post), 200


@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = BlogPost.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    db.session.delete(post)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)
