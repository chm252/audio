import './App.css';

import React, {useState} from "react";
import axios from "axios";

function App() {
  //State for storing uploaded audio file
  const [files, setFiles] = useState(null);
  //State for storing transcriptions data from backend database
  const [transcriptions, setTranscriptions] = useState([]);
  //State for storing query of substring
  const [query, setQuery] = useState("");

  /**
   * Handles file upload and sends the file to the backend.
   * Displays an alert with the transcribed text upon successful upload.
   * Displays an alert if no file is uploaded.
   */  
    const handleTranscribe = async () => {
    const formData = new FormData();
    if (!files) {
      alert("Please upload a file.");
      return;
    }
    formData.append("file", files[0]);
    const res = await axios.post("http://127.0.0.1:8000/transcribe", formData);
    const transcription = res['data']['transcription']
    alert("File uploaded for transcription\n\"" + transcription + "\"");
  };
  /**
   * Fetches all stored transcriptions from the backend database.
   */
  const handleDisplayAll = async () => {
    const res = await axios.get(`http://127.0.0.1:8000/transcriptions`);
    setTranscriptions(res['data']['data']);
  };
  /**
   * Fetches transcriptions that contain substring which matches the user's search query.
   */
  const handleSearch = async () => {
    const res = await axios.get(`http://127.0.0.1:8000/search?query=${query}`);
    setTranscriptions(res['data']['results']);
  };

  return (
    <div>
      <h1 className="header">Audio Transcription</h1>
      {/* File Upload Input */}
      <input className="choose-file-button" type="file" onChange={(e) => setFiles(e.target.files)} />
      <button className="transcribe-button" onClick={handleTranscribe}>Transcribe</button>
            
      {/* Button to fetch all transcriptions */}
      <button className="display-all-button" onClick={handleDisplayAll}> Display All </button>

      {/* Search Input and Button */}
      <input className="search-bar" type="text" onChange={(e) => setQuery(e.target.value)} />
      <button className="search-button" onClick={handleSearch}> Search </button>

      {/* Display List of Transcriptions */}
      <h2>Transcriptions</h2>
      <ul>
        {transcriptions.map((item, index) => (
          <li key={index}>{item[1]}: {item[2]}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

