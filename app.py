from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Sathesh%4008@localhost:5432/NewDB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

# Create the database tables
with app.app_context():
    db.create_all()

# show all user
@app.route('/items/', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/items/', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json or not 'description' in request.json:
        abort(400)
    item = Item(name=request.json['name'], description=request.json['description'])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

# show user by ID
@app.route('/items/<int:item_id>/', methods=['GET'])
def get_item_by_id(item_id):
    # Retrieve the item by ID
    item = Item.query.get(item_id)
    
    # Check if the item exists
    if item is None:
        # Return a 404 error if the item is not found
        abort(404, description=f"Item with ID {item_id} not found.")
    
    # Return the item as JSON
    return jsonify(item.to_dict())

# Enter new user
@app.route('/items/<int:item_id>/', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404)
    if not request.json:
        abort(400)
    item.name = request.json.get('name', item.name)
    item.description = request.json.get('description', item.description)
    db.session.commit()
    return jsonify(item.to_dict())

# Delete User
@app.route('/items/<int:item_id>/', methods=['DELETE'])
def delete_item(item_id):
    # Retrieve the item by ID
    item = Item.query.get(item_id)
    
    # Check if the item exists
    if item is None:
        # Return a 404 error if the item is not found
        abort(404, description=f"Item with ID {item_id} not found.")
    
    # Delete the item from the database
    db.session.delete(item)
    db.session.commit()
    
    # Return a 204 No Content response
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
