// src/App.js

// Core React imports
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Importing styles

function App() {
  // ======================
  // 🔧 State Definitions
  // ======================
  const [pdfFile, setPdfFile] = useState(null);             // Selected PDF file
  const [filename, setFilename] = useState("");             // Uploaded filename
  const [question, setQuestion] = useState("");             // User input question
  const [messages, setMessages] = useState([]);             // Chat history
  const [isThinking, setIsThinking] = useState(false);      // Typing animation flag
  const bottomRef = useRef();                               // For auto-scroll

  // ======================
  // ⏬ Scroll to bottom on message update
  // ======================
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  // ======================
  // 📄 File Input Change Handler
  // ======================
  const handleFileChange = (e) => {
    setPdfFile(e.target.files[0]);
  };

  // ======================
  // 📤 Upload PDF to backend
  // ======================
  const handleUpload = async () => {
    if (!pdfFile) return alert("📄 Please select a PDF file");

    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      const res = await axios.post("http://localhost:8000/upload/", formData);
      setFilename(res.data.filename); // Save filename for question referencing

      // Bot response in chat
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: `✅ PDF **${res.data.filename}** uploaded.` },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "❌ Upload failed. Try again." },
      ]);
    }
  };

  // ======================
  // ❓ Ask a Question to Backend
  // ======================
  const handleAsk = async () => {
    if (!question.trim() || !filename) return;

    // Append user question to chat
    setMessages((prev) => [...prev, { type: "user", text: question }]);
    setQuestion(""); // Clear input
    setIsThinking(true); // Show typing animation

    const formData = new FormData();
    formData.append("filename", filename);
    formData.append("question", question);

    try {
      const res = await axios.post("http://localhost:8000/ask/", formData);
      setMessages((prev) => [...prev, { type: "bot", text: res.data.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "⚠️ Could not get answer." },
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  // ======================
  // 📱 Render UI
  // ======================
  return (
    <div className="chat-wrapper">
      {/* 🔹 Header */}
      <div className="chat-header">
        <h1>Lexa 🧠 PDF Q&A Assistant</h1>

        {/* Upload Section */}
        <div className="upload-button-container">
          <label className="animated-upload-btn">
            📄 Upload PDF
            <input type="file" onChange={handleFileChange} hidden />
          </label>
          <button onClick={handleUpload}>📤 Upload</button>
        </div>
      </div>

      {/* 🔹 Chat Body */}
      <div className="chat-body">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-bubble ${msg.type}`}>
            {msg.text}
          </div>
        ))}

        {/* Typing Animation */}
        {isThinking && (
          <div className="chat-bubble bot typing">Lexa is thinking...</div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* 🔹 Chat Footer */}
      <div className="chat-footer">
        <input
          type="text"
          placeholder="Ask something from the PDF..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleAsk}>Send</button>
      </div>
    </div>
  );
}

export default App;
