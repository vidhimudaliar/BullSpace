import csv
import firebase_admin
from firebase_admin import credentials, db
import json

# Initialize Firebase Admin SDK with the correct database URL
cred = credentials.Certificate(
    "library-31a65-firebase-adminsdk-fbsvc-f36f24791a.json")
firebase_admin.initialize_app(
    cred, {
        'databaseURL':
        'https://library-31a65-default-rtdb.europe-west1.firebasedatabase.app/'
    })


# Function to load seats data from the CSV file
def load_seats_from_csv(csv_file):
    seats = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            seat = {
                'seat_id': row['label_name'].strip(),
                'x': int(row['bbox_x']),
                'y': int(row['bbox_y']),
                'width': int(row['bbox_width']),
                'height': int(row['bbox_height']),
                'image': row['image_name'],
                'image_width': int(row['image_width']),
                'image_height': int(row['image_height']),
                'status': 'available'  # Default status
            }
            seats.append(seat)
    return seats


# Function to load people data from the JSON file
def load_people_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        people = data.get('peopleResult', {}).get('values', [])
        return people


# Function to check if a person is inside the seat's bounding box
def is_person_in_seat(person, seat):
    person_x = person['boundingBox']['x']
    person_y = person['boundingBox']['y']

    seat_x = seat['x']
    seat_y = seat['y']
    seat_width = seat['width']
    seat_height = seat['height']

    return seat_x <= person_x <= seat_x + seat_width and seat_y <= person_y <= seat_y + seat_height


# Function to update seat status in Firebase
def update_seat_status_in_firebase(seat):
    seat_ref = db.reference(seat['seat_id'])

    try:
        current_value = seat_ref.get()
        if current_value is None:
            print(
                f"Seat {seat['seat_id']} does not exist in Firebase. Skipping update."
            )
            return

        seat_ref.set(seat['status'])
        print(
            f"✅ Updated seat {seat['seat_id']} to '{seat['status']}' in Firebase."
        )
    except Exception as e:
        print(f"❌ Failed to update seat {seat['seat_id']}: {e}")


# Main function to process seats and people
def process_seats_and_people(csv_file, json_file):
    seats = load_seats_from_csv(csv_file)
    people = load_people_from_json(json_file)

    if not seats:
        print("No seats loaded from CSV.")
        return
    if not people:
        print("No people detected in the JSON.")
        return

    for seat in seats:
        print(f"🔍 Processing seat: {seat['seat_id']}")
        seat['status'] = 'available'  # Reset status for each run

        for person in people:
            if is_person_in_seat(person, seat):
                seat['status'] = 'occupied'
                print(f"🚶‍♂️ Seat {seat['seat_id']} is occupied.")
                break

        update_seat_status_in_firebase(seat)


# Example usage
csv_file = 'seats-coordinates.csv'
json_file = 'floor5-3.json'
process_seats_and_people(csv_file, json_file)
