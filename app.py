from flask import Flask, jsonify, request

app = Flask(__name__)

# Data model
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# GET all events (often required in labs)

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([e.to_dict() for e in events]), 200


# POST - create event

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Missing title"}), 400

    # safe ID generation
    new_id = events[-1].id + 1 if events else 1

    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH - update event

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Missing title"}), 400

    event = next((e for e in events if e.id == event_id), None)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    event.title = data["title"]

    return jsonify(event.to_dict()), 200



# DELETE - remove event

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events

    event = next((e for e in events if e.id == event_id), None)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != event_id]

    return jsonify({"message": "Event deleted"}), 200



# Run app

if __name__ == "__main__":
    app.run(debug=True)