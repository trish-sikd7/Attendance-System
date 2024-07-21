from pymongo import MongoClient
from bson import ObjectId
from base64 import b64encode

def get_student_details(image_id):
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection URL
    db = client["students_db"]  # Replace with your database name
    collection = db["students_collection"]  # Replace with your collection name

    # Define a projection to specify the fields you want to retrieve
    projection = {
        "_id": False,  # Exclude the MongoDB document ID
        "image_id": True,
        "name": True,
        "department": True,
        "year": True,
        "roll_no": True,
        "email": True,
        "phone": True,
        "image_data":True
    }

    # Query MongoDB to fetch student details based on the provided image_id
    student_data = collection.find_one({"image_id": image_id}, projection)

    return student_data

def save_student_attendance(student_data, image_data):
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection URL
    db = client["students_db"]  # Replace with your database name
    collection = db["students_attendance"]  # Collection for storing attendance

    # Encode image data to base64 for storage in MongoDB
    encoded_image = b64encode(image_data).decode('utf-8')

    # Extracting timestamp from student_data
    timestamp = student_data.get("timestamp")

    # Prepare the document to be inserted into the collection
    attendance_document = {
        "_id": ObjectId(),  # Generate a new ObjectId for the document
        "image_id": student_data["image_id"],
        "name": student_data["name"],
        "department": student_data["department"],
        "year": student_data["year"],
        "roll_no": student_data["roll_no"],
        "email": student_data["email"],
        "phone": student_data["phone"],
        "timestamp": timestamp,
        "image_data": encoded_image
    }

    # Insert the attendance record into the MongoDB collection
    collection.insert_one(attendance_document)
    
def get_all_student_attendance():
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection URL
    db = client["students_db"]  # Replace with your database name
    collection = db["students_attendance"]  # Collection for storing attendance

    # Define a projection to exclude the _id field
    projection = {"_id": False}

    # Retrieve all attendance records from the collection without including the _id field
    all_attendance = list(collection.find({}, projection))

    return all_attendance

def create_student(student_data):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["students_db"]
        collection = db["students_collection"]

        # Define the query to find the document based on the image_id
        query = {"image_id": student_data["image_id"]}

        # Update or insert the student data into the collection
        result = collection.update_one(query, {"$set": student_data}, upsert=True)

        # Return the inserted or updated document ID
        return result.upserted_id or result.modified_count

    except Exception as e:
        # Log or handle the exception as needed
        print(f"Error creating/updating student: {e}")
        return None