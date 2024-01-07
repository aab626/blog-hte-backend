from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

# Init Flask
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/blog-hte'

# Allow communication between servers
CORS(app)

# DB connection
mongo = PyMongo(app)
db = mongo.db.posts

print(db)

# Routing
# Create post
@app.route('/posts', methods=['POST'])
def createPost():
    # result = db.insert_one({
    #     'title': request.json['title'],
    #     'body': request.json['body'],
    #     'author': request.json['author'],
    #     'timestamp': request.json['timestamp']
    # })

    # return jsonify(str(result.inserted_id))
    return 'placeholder'

# Get list of posts
@app.route('/posts', methods=['GET'])
def getPosts():
    posts = list(db.find({}))
    for i in range(len(posts)):
        posts[i]['_id'] = str(posts[i]['_id'])

    return jsonify(posts)

# Get single post
@app.route('/post/<id>', methods=['GET'])
def getPost(id):
    return 'placeholder'

# Delete single post
@app.route('/users/<id>', methods=['DELETE'])
def deletePost(id):
    return 'placeholder'

# Update (edit) single post
@app.route('/users/<id>', methods=['PUT'])
def updatePost(id):
    return 'placeholder'





if __name__ == '__main__':
    app.run(debug=True)
