import React, { useState } from 'react';
import axios from 'axios';

const EmailComposer = () => {
  const [emailText, setEmailText] = useState('');

  const handleChange = async (e) => {
    const newText = e.target.value;
    setEmailText(newText);

    if (newText) {
      const response = await axios.post('https://api.openai.com/v1/engines/davinci/completions', 
      {
        prompt: newText,
        max_tokens: 50,
      }, 
      {
        headers: {
          'Authorization': `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      });

      setEmailText(newText + response.data.choices[0].text);
    }
  };

  return (
    <div>
      <textarea
        value={emailText}
        onChange={handleChange}
        placeholder="Compose your email..."
        rows="10"
        cols="50"
      />
    </div>
  );
};

export default EmailComposer;
