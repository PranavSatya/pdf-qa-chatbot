// Question.js

import React, { useState } from 'react';
import axios from 'axios';

// 🔍 Component to handle question input and answer display
function Question({ filename }) {
  // ========== 📦 Local State ==========
  const [question, setQuestion] = useState(""); // User's question input
  const [answer, setAnswer] = useState("");     // Answer fetched from backend

  // ========== 📤 Ask Question Handler ==========
  const askQuestion = async () => {
    try {
      // Send filename and question to backend API
      const response = await axios.post("http://localhost:8000/ask/", {
        filename,
        question
      });

      // Store the received answer
      setAnswer(response.data.answer);
    } catch (err) {
      // Handle any errors gracefully
      setAnswer("Error getting answer.");
    }
  };

  // ========== 📄 Render UI ==========
  return (
    <div className="question-section">
      {/* Text input for user's question */}
      <input
        type="text"
        value={question}
        onChange={e => setQuestion(e.target.value)}
        placeholder="Ask a question about the PDF"
      />

      {/* Ask button to trigger API call */}
      <button onClick={askQuestion}>Ask</button>

      {/* Display the answer if available */}
      {answer && (
        <p>
          <strong>Answer:</strong> {answer}
        </p>
      )}
    </div>
  );
}

export default Question;
