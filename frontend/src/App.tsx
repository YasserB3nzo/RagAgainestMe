import { useEffect, useState } from 'react';
import { getHealth } from './lib/api';

function App() {
  const [message, setMessage] = useState('Checking backend...');

  useEffect(() => {
    getHealth()
      .then((data) => setMessage('✅ Backend: ' + data.status))
      .catch(() => setMessage('❌ Backend is not available'));
  }, []);

  return (
    <div>
      <h1>RAG Against the Machine</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
