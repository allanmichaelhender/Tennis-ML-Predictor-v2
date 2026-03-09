import { useEffect, useState } from 'react';
import api from './services/api'; // 🎯 This is the Axios helper we created

function App() {
  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState("Waiting for request...");

  useEffect(() => {
    setStatus("Pinging Backend...");
    
    // 🎯 This triggers the Vite Proxy
    api.get('/lab/model-performance')
      .then(res => {
        setData(res.data);
        setStatus("Connected! ✅");
      })
      .catch(err => {
        setStatus(`Failed: ${err.response?.status || err.message} ❌`);
      });
  }, []);

  return (
    <div style={{ padding: '2rem', background: '#0f172a', color: 'white', minHeight: '100vh' }}>
      <h1>Quant Lab Connection Test</h1>
      <p>Status: <span style={{ fontWeight: 'bold' }}>{status}</span></p>
      
      {data && (
        <div style={{ marginTop: '1rem', border: '1px solid #1e293b', padding: '1rem' }}>
          <p>ROI: {(data.summary.roi * 100).toFixed(2)}%</p>
          <p>Brier: {data.summary.brier_score.toFixed(4)}</p>
        </div>
      )}
    </div>
  );
}

export default App;
