from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from whatsapp_api_client_python import API
from models import db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///whatsapp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)

greenAPI = API.GreenAPI("7103882600", "11354fa768754b4e87eb7650a97709e0f51b5d7cedca4679a0")

@app.route("/create_group", methods=["POST"])
def create_group():
    # Get data from the request
    data = request.json

    # Extract group name and chat IDs from the request data
    group_name = data.get("group_name")
    chat_ids = data.get("chat_ids", [])

    # Make sure you have the necessary data
    if not group_name or not chat_ids:
        return jsonify({"error": "Invalid request data"}), 400

    # Create the group
    create_group_response = greenAPI.groups.createGroup(group_name, chat_ids)

    # Handle the response
    if create_group_response.code == 200:
        chat_id = create_group_response.data.get("groupInfo", {}).get("id")
        if chat_id:
            # Send a message to the group
            send_message_response = greenAPI.sending.sendMessage(chat_id, "Message text")
            if send_message_response.code == 200:
                return jsonify({"success": True, "group_id": chat_id, "message_id": send_message_response.data.get("id")})
            else:
                return jsonify({"error": send_message_response.error}), 500
        else:
            return jsonify({"success": "Group chat created successfully"}), 200
    else:
        return jsonify({"error": create_group_response.error}), 500

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(**data)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
 


if __name__ == '__main__':
    main()

