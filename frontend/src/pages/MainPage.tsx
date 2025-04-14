import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import axios from 'axios';

interface HanjaResult {
  traditional: string;
  simplified: string;
  korean_pronunciation: string;
  chinese_pronunciation: string;
  radical: string;
  stroke_count: number;
  meaning: string;
  frequency: number;
}

const MainPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState<HanjaResult[]>([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSearch = async () => {
    if (!searchTerm.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/search?query=${searchTerm}`);
      setResults(response.data);
    } catch (error) {
      console.error('검색 중 오류 발생:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleResultClick = (hanja: string) => {
    navigate(`/hanja/${hanja}`);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          한자 사전
        </Typography>
        
        <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              label="한자 또는 발음 검색"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              disabled={loading}
              sx={{ minWidth: '100px' }}
            >
              <SearchIcon />
            </Button>
          </Box>
        </Paper>

        {loading && (
          <Typography align="center">검색 중...</Typography>
        )}

        {results.length > 0 && (
          <Paper elevation={3}>
            <List>
              {results.map((result, index) => (
                <ListItem
                  key={index}
                  button
                  onClick={() => handleResultClick(result.traditional)}
                >
                  <ListItemText
                    primary={
                      <Typography variant="h6">
                        {result.traditional}
                        {result.simplified !== result.traditional && ` (${result.simplified})`}
                      </Typography>
                    }
                    secondary={
                      <>
                        <Typography component="span">
                          {result.korean_pronunciation}
                          {result.chinese_pronunciation && ` (${result.chinese_pronunciation})`}
                        </Typography>
                        <br />
                        <Typography component="span" color="text.secondary">
                          {result.meaning}
                        </Typography>
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        )}
      </Box>
    </Container>
  );
};

export default MainPage; 