import React, { useState } from 'react';

function App() {
  const [race1, setRace1] = useState('');
  const [race2, setRace2] = useState('');
  const [name1, setName1] = useState('');
  const [name2, setName2] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFuse = async () => {
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/fuse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          race1,
          race2,
          name1,
          name2
        })
      });

      if (!response.ok) {
        throw new Error('后端返回错误');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('请求失败，请确认 Flask 后端在运行且输入无误。');
      console.error(err);
    }
  };

  const renderDemon = (title, demon) => (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '1em' }}>
      <h3>{title}</h3>
      <p><strong>Name:</strong> {demon.name}</p>
      <p><strong>Race:</strong> {demon.race}</p>
      <p><strong>Level:</strong> {demon.lvl}</p>
      <p><strong>Trait:</strong> {demon.trait}</p>
      <p><strong>Inherits:</strong> {demon.inherits}</p>
      <p><strong>Item (normal):</strong> {demon.item}</p>
      <p><strong>Item (rare):</strong> {demon.itemr}</p>
      <p><strong>Stats:</strong> {demon.stats}</p>
      <p><strong>Resists:</strong> {demon.resists}</p>
      <p><strong>Skills:</strong></p>
      <ul>
        {Object.entries(demon.skills).map(([skill, level]) => (
          <li key={skill}>{skill}: Lv {level}</li>
        ))}
      </ul>
    </div>
  );

  return (
    <div style={{ padding: '2em', fontFamily: 'sans-serif' }}>
      <h1>🎭 P5R Fusion Calculator</h1>

      <div style={{ marginBottom: '1em' }}>
        <label>种族 1 (Race 1): </label>
        <input value={race1} onChange={e => setRace1(e.target.value)} />
      </div>
      <div style={{ marginBottom: '1em' }}>
        <label>种族 2 (Race 2): </label>
        <input value={race2} onChange={e => setRace2(e.target.value)} />
      </div>
      <div style={{ marginBottom: '1em' }}>
        <label>恶魔名 1 (Name 1): </label>
        <input value={name1} onChange={e => setName1(e.target.value)} />
      </div>
      <div style={{ marginBottom: '1em' }}>
        <label>恶魔名 2 (Name 2): </label>
        <input value={name2} onChange={e => setName2(e.target.value)} />
      </div>

      <button onClick={handleFuse}>开始融合</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div style={{ marginTop: '2em' }}>
          {renderDemon("通过种族融合结果", result.fusion_by_race)}
          {renderDemon("通过名称融合结果", result.fusion_by_name)}
        </div>
      )}
    </div>
  );
}

export default App;
