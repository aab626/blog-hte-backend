from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

# Admin password
ADMIN_PASSWORD = 'miau123'

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
    # Retrieve max post id
    result = db.aggregate([
        {"$sort": {"id": -1}},
        {"$limit": 1},
        {"$project": {"_id": 0, "id": 1}}
        ])
    
    result_document = next(result, None)
    max_id = result_document['id']

    result = db.insert_one({
        'title': request.json['title'],
        'body': request.json['body'],
        'author': request.json['author'],
        'timestamp': request.json['timestamp'],
        'edited': False,
        'id': max_id + 1
    })

    return jsonify({'result': result.acknowledged})

# Get list of posts
@app.route('/posts', methods=['GET'])
def getPosts():
    posts = list(db.find({}).sort('id', -1))
    for i in range(len(posts)):
        posts[i]['_id'] = str(posts[i]['_id'])

    return jsonify(posts) 

# Get single post
@app.route('/posts/<id>', methods=['GET'])
def getPost(id):
    post = db.find_one({'_id': ObjectId(id)})
    post['_id'] = str(post['_id'])
    return jsonify(post)

# Delete single post
@app.route('/posts/<id>', methods=['DELETE'])
def deletePost(id):
    result = db.delete_one({'_id': ObjectId(id)})
    return jsonify({'result': result.acknowledged})

# Update (edit) single post
@app.route('/posts/<id>', methods=['PUT'])
def updatePost(id):
    print(id);
    print(request.json);
    result = db.update_one(
        {
            '_id': ObjectId(id)
        },
        {
            '$set': {
                'title': request.json['title'],
                'body': request.json['body'],
                'author': request.json['author'],
                'edited': True
            }
        }
    )
    
    return jsonify({'result': result.acknowledged})

# Check admin login (too lazy to add a new db)
@app.route('/login', methods=['POST'])
def checkAdminLogin():
    result = request.json['password'] == ADMIN_PASSWORD
    return jsonify({'result': result})


# Run app
if __name__ == '__main__':
    app.run(host='192.168.0.100', debug=True)
