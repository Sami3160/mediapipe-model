import React, { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import * as cam from '@mediapipe/camera_utils';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';
import { Pose } from '@mediapipe/pose';

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
    if (!results.poseLandmarks) return;
  
    const landmarkNames = [
      "nose", "right_eye_inner", "right_eye", "right_eye_outer",
      "left_eye_inner", "left_eye", "left_eye_outer", "right_ear", "left_ear",
      "mouth_right", "mouth_left", "right_shoulder", "left_shoulder",
      "right_elbow", "left_elbow", "right_wrist", "left_wrist",
      "right_hip", "left_hip", "right_knee", "left_knee",
      "right_ankle", "left_ankle", "right_heel", "left_heel",
      "right_foot_index", "left_foot_index"
    ];
  
    // Extract only the required landmarks
    const poseData = {};
    landmarkNames.forEach((name, index) => {
      poseData[name] = results.poseLandmarks[index];
    });
    //delete facial things
    delete poseData.nose; // Remove the nose landmark
    delete poseData.right_eye_inner;
    delete poseData.right_eye;
    delete poseData.right_eye_outer;
    delete poseData.left_eye_inner;
    delete poseData.left_eye;
    delete poseData.left_eye_outer;
    delete poseData.right_ear;
    delete poseData.left_ear;
    delete poseData.mouth_right;
    delete poseData.mouth_left;
    

  
    console.table(poseData); // Log the object with labeled landmarks
  
    const canvasElement = canvasRef.current;
    const canvasCtx = canvasElement.getContext("2d");
  
    // Clear the canvas
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  
    // Draw the detected landmarks and connections
    drawConnectors(canvasCtx, results.poseLandmarks, Pose.POSE_CONNECTIONS, {
      color: "#00FF00",
      lineWidth: 4,
    });
    drawLandmarks(canvasCtx, results.poseLandmarks, {
      color: "#FF0000",
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
    <div className="App relative">
    <Webcam
      ref={webcamRef}
      // style={{ display: 'none' }} // Hide the webcam feed
    />
    <canvas ref={canvasRef} width={640} className='absolute top-0 left-0 z-10' height={480} />
  </div>
  )
}

export default App
