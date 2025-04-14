import React, { useState } from 'react';
import {
  TextField,
  Button,
  Box,
  Typography,
  Paper,
  Grid,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import axios from 'axios';

const Search = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`http://localhost:8000/hanja/${query}`);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || '검색 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs>
            <TextField
              fullWidth
              label="한자 검색"
              variant="outlined"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              onClick={handleSearch}
              disabled={loading}
              startIcon={<SearchIcon />}
            >
              검색
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {loading && (
        <Typography align="center">검색 중...</Typography>
      )}

      {error && (
        <Typography color="error" align="center">
          {error}
        </Typography>
      )}

      {result && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h4" component="div" sx={{ mb: 2 }}>
                {result.traditional}
                {result.simplified && ` (${result.simplified})`}
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                한글 발음
              </Typography>
              <Typography variant="body1">
                {result.korean_pronunciation}
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                중국어 발음
              </Typography>
              <Typography variant="body1">
                {result.chinese_pronunciation}
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                부수
              </Typography>
              <Typography variant="body1">
                {result.radical}
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1" color="text.secondary">
                획수
              </Typography>
              <Typography variant="body1">
                {result.stroke_count}획
              </Typography>
            </Grid>
            
            <Grid item xs={12}>
              <Typography variant="subtitle1" color="text.secondary">
                뜻
              </Typography>
              <Typography variant="body1">
                {result.meaning}
              </Typography>
            </Grid>
            
            {result.examples && (
              <Grid item xs={12}>
                <Typography variant="subtitle1" color="text.secondary">
                  예문
                </Typography>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                  {result.examples}
                </Typography>
              </Grid>
            )}
          </Grid>
        </Paper>
      )}
    </Box>
  );
};

export default Search; 