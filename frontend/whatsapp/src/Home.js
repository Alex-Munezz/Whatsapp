import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [groupName, setGroupName] = useState('');
  const [chatIds, setChatIds] = useState('');
  const [resultMessage, setResultMessage] = useState('');

  const handleCreateGroup = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/create_group', {
        group_name: groupName,
        chat_ids: chatIds.split(',').map(id => id.trim()), // Assuming chat IDs are comma-separated
      });

      if (response.data.success) {
        setResultMessage(`Group created successfully!`);
      } else {
        setResultMessage(`Error: ${response.data.error}`);
      }
    } catch (error) {
      setResultMessage('An error occurred while creating the group.');
    }
  };

  return (
    <div className="create-group-page">
      <h1>Create a WhatsApp Group</h1>
      <div className="form-container">
        <label>Group Name:</label>
        <input 
        type="text" 
        value={groupName} 
        onChange={(e) => setGroupName(e.target.value)} 
        required
        />

        <label>Phone numbers (comma-separated):<br />Please ensure not to write any symbols and add "@c.us" after your number </label>
        <textarea 
        value={chatIds}
        placeholder='example : 2547xxxxxxxx@c.us' 
        onChange={(e) => setChatIds(e.target.value)} 
        required
        />
        <button onClick={handleCreateGroup}>Create Group</button>
         <br />
         <br />
        {resultMessage && <div className={resultMessage.includes('Error') ? 'error-message' : 'success-message'}>
          {resultMessage}
        </div>}
      </div>
    </div>
  );
};

export default Home;
