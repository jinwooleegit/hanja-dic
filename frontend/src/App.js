import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// 컴포넌트 임포트
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import SearchResultPage from './pages/SearchResultPage';
import HanjaDetailPage from './pages/HanjaDetailPage';
import FavoritesPage from './pages/FavoritesPage';
import AboutPage from './pages/AboutPage';
import NotFoundPage from './pages/NotFoundPage';

// 테마 설정
const theme = createTheme({
  palette: {
    primary: {
      main: '#5D1049',
      light: '#7B2D64',
      dark: '#3F0D31',
    },
    secondary: {
      main: '#EEBF4D',
      light: '#F1CA6E',
      dark: '#E0AA26',
    },
    background: {
      default: '#F9F9F9',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: [
      '"Noto Sans KR"',
      '"Noto Serif KR"',
      'sans-serif',
    ].join(','),
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
    h3: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="app">
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/search" element={<SearchResultPage />} />
              <Route path="/hanja/:id" element={<HanjaDetailPage />} />
              <Route path="/favorites" element={<FavoritesPage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App; 