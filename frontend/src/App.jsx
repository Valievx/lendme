import { useState } from 'react';
import './App.scss';
import { Button } from './shared/ui/Button/Button';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div className="card">
        <h1>Vite + React</h1>
        <Button onClick={() => setCount((count) => count + 1)}>count is {count}</Button>
      </div>
    </>
  );
}

export default App;
