# from fastapi import FastAPI, File, UploadFile
# from video_processing.face_detection import recognize_faces

# app = FastAPI()

# @app.post("/recognize_student/")
# async def process_image(file: UploadFile = File(...)):
#     result = await recognize_faces(file)
#     return result

# main.py

# main.py

# main.py

# from fastapi import FastAPI
# from socketio import ASGIApp
# import socketio
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_socketio import SocketManager

# from video_processing.face_detection import handle_stream

# app = FastAPI()
# origins = [
#     "http://localhost:3000",
#     # Add more origins if needed
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# sio = socketio.Server()
# handler = ASGIApp(sio)

# @sio.on('connect')
# def connect(sid, environ):
#     print(f"Connected: {sid}")

# @sio.on('disconnect')
# def disconnect(sid):
#     print(f"Disconnected: {sid}")

# @sio.on('stream')
# async def stream(sid, data):
#     await handle_stream(sio, sid, data)
    
# @app.get('/')
# def read_root():
#     return {"Hello": "World"}

# from fastapi import FastAPI
# from fastapi_socketio import SocketManager
# from fastapi.middleware.cors import CORSMiddleware
# from video_processing.face_detection import handle_stream

# app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     # Add more origins if needed
# ]

# app.add_middleware(
#    CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Add the appropriate URL of your Next.js app
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# manager = SocketManager(app=app, cors_allowed_origins="*")


# @manager.on("connect")
# async def connect(sid, environ):
#     print(f"Connected: {sid}")


# @manager.on("disconnect")
# async def disconnect(sid):
#     print(f"Disconnected: {sid}")


# @manager.on("stream")
# async def stream(sid, data):
#     # Call your face detection logic or processing here
#     await handle_stream(sio, sid, data)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Adjust this with the correct URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         print(f"Received message: {data}")
#         await websocket.send_text(f"Message text was: {data}")

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)


from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from video_processing.face_detection import handle_stream
from video_processing.database_module import create_student, get_all_student_attendance 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this with the correct URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()  # Receive image data as bytes
        print("Received message: Image data")
        # Call your face detection logic or processing here
        await handle_stream(data,websocket)  # Pass the WebSocket, sid, and image data
        # await websocket.send_text("Image data received")

@app.get("/student_attendance")
def fetch_student_attendance():
    attendance_data = get_all_student_attendance()
    return attendance_data

@app.post("/create-student", response_model=dict)
async def create_student_endpoint(student: dict):
    try:
        # Call the create_student function
        inserted_id = create_student(student)
        
        if inserted_id:
            return {"status": "Student created successfully", "student_id": str(inserted_id)}
        else:
            return {"status": "Error creating student"}
    except Exception as e:
        return {"status": "Error creating student", "error_message": str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)


