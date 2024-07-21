"use client";
import { useEffect, useState } from "react";
import Layout from "./layout/page";

const VideoStream = () => {
  const speak = (text: string | undefined) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      
      // Set language to English (India)
      utterance.lang = 'en-IN';
  
      // Adjust speech rate (0.1 to 10)
      utterance.rate = 1; // Adjust the value to change speech rate. Default is 1.
      
      window.speechSynthesis.speak(utterance);
    } else {
      console.error('Speech synthesis not supported');
    }
  };

  let ws = null;
  const [message, setMessage] = useState("");
  const [studentData, setStudentData] = useState({});

  useEffect(() => {
    let intervalId: string | number | NodeJS.Timeout | undefined; // For controlling the interval

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        const videoElement = document.getElementById("videoElement");
        if (videoElement) {
          videoElement.srcObject = stream;
        }
      })
      .catch((error) => {
        console.error("Error accessing camera:", error);
      });

    ws = new WebSocket("ws://localhost:8000/ws");

    const sendImage = async () => {
      const videoElement = document.getElementById("videoElement");
      if (!videoElement) return;

      const canvas = document.createElement("canvas");
      const context = canvas.getContext("2d");
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

      // Convert canvas image to Blob
      canvas.toBlob(async (blob) => {
        const reader = new FileReader();
        reader.onload = function (event) {
          if (ws.readyState === ws.OPEN) {
            ws.send(event.target.result); // Send binary data as ArrayBuffer
            console.log("Image sent");
          }
        };
        reader.readAsArrayBuffer(blob);
      }, "image/jpeg");
    };

    // Function to send an image every 5 seconds
    const startSendingImages = () => {
      intervalId = setInterval(() => {
        sendImage();
      }, 2500);
    };

    startSendingImages(); // Start sending images immediately

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      setMessage(response.message);
      setStudentData((prevStudentData) => {
        return { ...prevStudentData, ...response.student_data };
      });
    };

    return () => {
      if (ws) {
        ws.close();
      }
      if (intervalId) {
        clearInterval(intervalId); // Clear the interval on cleanup
      }
    };
  }, []);

  useEffect(() => {
    speak(message)
  },[message])

  return (
    <>
      <Layout
        component={
          <div className="w-full h-full flex flex-col items-center justify-center border-dotted">
            <video
              id="videoElement"
              width="100%"
              height="100%"
              autoPlay
              className="rounded-md"
            />
            <h2 className="text-lg font-bold mt-4">Attendance Status:</h2>
            <h1 className="text-2xl font-bold text-blue-600">{message}</h1>
          </div>
        }
        studentData={studentData}
      />
    </>
  );
};

export default VideoStream;
