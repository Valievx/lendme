import './styles/App.scss';
import { Main } from '../pages/Main';
import { Header } from '../widgets/Header/Header';
import { Route, Routes } from 'react-router-dom';

function App() {
	return (
		<>
			<Header />
			<Routes>
				<Route path="/" element={<Main />} />
			</Routes>
		</>
	);
}

export default App;
