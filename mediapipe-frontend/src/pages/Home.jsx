import React, { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import { Pose } from '@mediapipe/pose';
import * as cam from '@mediapipe/camera_utils';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';



function App() {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const pose = new Pose({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
    });

    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    pose.onResults(onResults);

    const camera = new cam.Camera(webcamRef.current.video, {
      onFrame: async () => {
        await pose.send({ image: webcamRef.current.video });
      },
      width: 640,
      height: 480,
    });
    camera.start();
  }, []);

  function onResults(results) {
    const canvasElement = canvasRef.current;
    const canvasCtx = canvasElement.getContext('2d');

    // Clear the canvas
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

    // Draw the detected landmarks and connections
    drawConnectors(canvasCtx, results.poseLandmarks, Pose.POSE_CONNECTIONS, {
      color: '#00FF00',
      lineWidth: 4,
    });
    drawLandmarks(canvasCtx, results.poseLandmarks, {
      color: '#FF0000',
      lineWidth: 2,
    });

    // Provide feedback based on posture
    const feedback = getPostureFeedback(results.poseLandmarks);
    console.log(feedback);
  }

  function getPostureFeedback(landmarks) {
    let feedback = [];

    // Example: Check head position relative to shoulders
    const headYDiff = landmarks[0].y - landmarks[11].y; // Comparing head and shoulder positions

    if (headYDiff > 0.03) {
      feedback.push("Lift your head slightly.");
    } else if (headYDiff < -0.03) {
      feedback.push("Lower your head slightly.");
    }

    // Additional checks for shoulders, back, etc.
    // You can add more logic here based on the landmarks

    return feedback.length ? feedback.join(" ") : "Great posture! Keep it up!";
  }

  return (
    <div className="display relative rounded-3xl overflow-hidden w-full max-w-lg xl:max-w-xl bg-deep-space">
      <div className="absolute inset-0 bg-gradient-to-r from-neon-blue to-neon-green opacity-5 z-10"></div>
      <Webcam
        ref={webcamRef}
        className="webcam rounded-3xl w-full opacity-90"
        width="100%"
        height="auto"
      />
      <canvas
        ref={canvasRef}
        className="canvas absolute top-0 left-0 rounded-3xl w-full h-full z-20"
      />
      <div className="absolute top-4 left-4 bg-deep-space bg-opacity-70 text-neon-blue px-3 py-1 rounded-full text-sm font-medium z-30 backdrop-filter backdrop-blur-sm">
        Live Feed
      </div>
    </div>
  );
}
export default function Home() {
  return (
    <div className='items-center'>
      {/* <h1 className='text-3xl'>Home Page</h1> */}
      <App />
    </div>
  )
}
