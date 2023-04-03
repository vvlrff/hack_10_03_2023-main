import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage';
import CardPage from './pages/CardPage';
import NotFoundPage from './pages/NotFoundPage';
import CardsPage from './pages/CardsPage';
import Layout from './components/Layout';
import CountryPage from './pages/CountryPage';
import CategoryPage from './pages/CategoryPage';


function App() {
  return (
    <>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path='cards/' element={<CardsPage />} />
          <Route path='cards/country/:country' element={<CountryPage />} />
          <Route path='cards/category/:category' element={<CategoryPage />} />
          <Route path='card/:id_data' element={<CardPage />} />
          <Route path='*' element={<NotFoundPage />} />
        </Route>
      </Routes>
    </>
  );
}

export default App;
