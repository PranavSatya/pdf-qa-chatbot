// Upload.js

import React, { useState } from 'react';
import axios from 'axios';

function Upload({ onUpload }) {
  // ============ 📦 Local State ============
  const [file, setFile] = useState(null);      // Holds the selected file
  const [status, setStatus] = useState("");    // Displays upload status

  // ============ 📤 Handle File Upload ============
  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);  // Append selected file to form data

    try {
      setStatus("Uploading...");
      const response = await axios.post("http://localhost:8000/upload/", formData); // Send to backend

      setStatus("Uploaded successfully!");
      onUpload(response.data.filename); // Notify parent component of uploaded file
    } catch (err) {
      setStatus("Upload failed.");
    }
  };

  // ============ 📄 Render Upload UI ============
  return (
    <div className="upload-section">
      {/* File Selector */}
      <input
        type="file"
        accept=".pdf"
        onChange={e => setFile(e.target.files[0])}
      />

      {/* Upload Trigger */}
      <button onClick={handleUpload}>Upload PDF</button>

      {/* Status Message */}
      <p>{status}</p>
    </div>
  );
}

export default Upload;
