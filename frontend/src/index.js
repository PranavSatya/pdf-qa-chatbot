// Importing the core React library
import React from 'react';

// Importing the ReactDOM library for interacting with the DOM
import ReactDOM from 'react-dom/client';

// Importing the main App component
import App from './App';

// Importing global styles for the app
import './App.css';

// Creating a root element using the new createRoot API (React 18+)
const root = ReactDOM.createRoot(document.getElementById('root'));

// Rendering the App component inside <React.StrictMode> for highlighting potential problems
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
