import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Divider,
  Chip,
  IconButton,
  CircularProgress,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  useTheme,
  Alert
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import SortIcon from '@mui/icons-material/Sort';
import FilterListIcon from '@mui/icons-material/FilterList';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

// 임시 데이터 (실제 구현에서는 API 호출로 대체)
const MOCK_SEARCH_RESULTS = [
  { id: 1, traditional: '愛', simplified: '爱', pronunciation: '애', meaning: '사랑 애', frequency: 100, radical: '心', strokes: 13 },
  { id: 2, traditional: '安', simplified: '安', pronunciation: '안', meaning: '편안할 안', frequency: 95, radical: '宀', strokes: 6 },
  { id: 3, traditional: '暗', simplified: '暗', pronunciation: '암', meaning: '어두울 암', frequency: 70, radical: '日', strokes: 13 },
  { id: 4, traditional: '案', simplified: '案', pronunciation: '안', meaning: '책상 안', frequency: 85, radical: '木', strokes: 10 },
  { id: 5, traditional: '岸', simplified: '岸', pronunciation: '안', meaning: '언덕 안', frequency: 65, radical: '山', strokes: 8 },
  { id: 6, traditional: '按', simplified: '按', pronunciation: '안', meaning: '누를 안', frequency: 75, radical: '手', strokes: 9 },
  { id: 7, traditional: '雁', simplified: '雁', pronunciation: '안', meaning: '기러기 안', frequency: 45, radical: '隹', strokes: 12 },
  { id: 8, traditional: '顔', simplified: '颜', pronunciation: '안', meaning: '얼굴 안', frequency: 80, radical: '頁', strokes: 18 },
  { id: 9, traditional: '闇', simplified: '暗', pronunciation: '암', meaning: '어두울 암', frequency: 30, radical: '門', strokes: 17 },
  { id: 10, traditional: '杏', simplified: '杏', pronunciation: '행', meaning: '살구 행', frequency: 40, radical: '木', strokes: 7 },
  { id: 11, traditional: '行', simplified: '行', pronunciation: '행', meaning: '다닐 행', frequency: 95, radical: '行', strokes: 6 },
  { id: 12, traditional: '幸', simplified: '幸', pronunciation: '행', meaning: '다행 행', frequency: 85, radical: '干', strokes: 8 },
];

const SearchResultPage = () => {
  const theme = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const initialQuery = queryParams.get('q') || '';
  
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState('frequency');
  const [filterBy, setFilterBy] = useState('all');
  
  const itemsPerPage = 8;
  const maxPage = Math.ceil(results.length / itemsPerPage);
  
  // 페이지 변경 시 스크롤을 맨 위로 이동
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [page]);
  
  // 검색어 변경 시 결과 업데이트
  useEffect(() => {
    if (initialQuery) {
      handleSearch();
    }
  }, [initialQuery]);
  
  const handleSearch = () => {
    setLoading(true);
    setError(null);
    
    // API 호출 시뮬레이션
    setTimeout(() => {
      try {
        // 실제 구현에서는 axios나 fetch를 사용한 API 호출로 대체
        const filtered = MOCK_SEARCH_RESULTS.filter(item => {
          const query = searchQuery.toLowerCase();
          return (
            item.traditional.includes(query) ||
            item.simplified.includes(query) ||
            item.pronunciation.includes(query) ||
            item.meaning.toLowerCase().includes(query)
          );
        });
        
        // 정렬
        const sorted = [...filtered].sort((a, b) => {
          if (sortBy === 'frequency') return b.frequency - a.frequency;
          if (sortBy === 'strokes') return a.strokes - b.strokes;
          return 0;
        });
        
        setResults(sorted);
        setPage(1);
        setLoading(false);
      } catch (err) {
        setError('검색 중 오류가 발생했습니다. 다시 시도해주세요.');
        setLoading(false);
      }
    }, 800);
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    handleSearch();
    // URL 업데이트
    navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
  };
  
  const handleSortChange = (event) => {
    setSortBy(event.target.value);
    
    // 정렬 적용
    const sorted = [...results].sort((a, b) => {
      if (event.target.value === 'frequency') return b.frequency - a.frequency;
      if (event.target.value === 'strokes') return a.strokes - b.strokes;
      return 0;
    });
    
    setResults(sorted);
  };
  
  const handleFilterChange = (event) => {
    setFilterBy(event.target.value);
    // 필터링 로직은 향후 구현
  };
  
  // 현재 페이지에 표시할 결과
  const currentResults = results.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage
  );

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
          sx={{ mb: 2 }}
        >
          홈으로
        </Button>
        
        <Paper
          component="form"
          elevation={2}
          sx={{
            p: '8px 16px',
            display: 'flex',
            alignItems: 'center',
            mb: 3,
            borderRadius: 2
          }}
          onSubmit={handleSubmit}
        >
          <TextField
            fullWidth
            placeholder="한자, 한글, 뜻으로 검색..."
            variant="standard"
            InputProps={{ disableUnderline: true }}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ flexGrow: 1 }}
          />
          <IconButton type="submit" aria-label="search">
            <SearchIcon />
          </IconButton>
        </Paper>
        
        <Typography variant="h5" component="h1" gutterBottom>
          '{initialQuery}' 검색 결과
        </Typography>
        
        <Divider sx={{ my: 2 }} />
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2, mb: 3 }}>
          <Box>
            <Typography variant="body2" color="text.secondary">
              총 {results.length}개의 결과
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl size="small" variant="outlined" sx={{ minWidth: 120 }}>
              <InputLabel id="sort-label">정렬</InputLabel>
              <Select
                labelId="sort-label"
                value={sortBy}
                onChange={handleSortChange}
                label="정렬"
                startAdornment={<SortIcon fontSize="small" sx={{ mr: 1 }} />}
              >
                <MenuItem value="frequency">빈도순</MenuItem>
                <MenuItem value="strokes">획수순</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl size="small" variant="outlined" sx={{ minWidth: 120 }}>
              <InputLabel id="filter-label">필터</InputLabel>
              <Select
                labelId="filter-label"
                value={filterBy}
                onChange={handleFilterChange}
                label="필터"
                startAdornment={<FilterListIcon fontSize="small" sx={{ mr: 1 }} />}
              >
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="radical-heart">심방변</MenuItem>
                <MenuItem value="radical-water">수변</MenuItem>
                <MenuItem value="radical-grass">초두</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>
      </Box>
      
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ mb: 4 }}>{error}</Alert>
      ) : results.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 2 }}>
          <Typography variant="h6" gutterBottom>
            검색 결과가 없습니다.
          </Typography>
          <Typography color="text.secondary">
            다른 검색어로 다시 시도해보세요.
          </Typography>
        </Paper>
      ) : (
        <>
          <Grid container spacing={3}>
            {currentResults.map((result) => (
              <Grid item key={result.id} xs={12} sm={6} md={3}>
                <Card 
                  elevation={2}
                  sx={{ 
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    borderRadius: 2,
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 6,
                    }
                  }}
                >
                  <CardActionArea 
                    component={Link} 
                    to={`/hanja/${result.traditional}`}
                    sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}
                  >
                    <CardContent sx={{ width: '100%' }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                        <Typography variant="h3" component="div">
                          {result.traditional}
                        </Typography>
                        <Chip 
                          label={`${result.strokes}획`} 
                          size="small" 
                          color="primary" 
                          variant="outlined"
                        />
                      </Box>
                      
                      {result.traditional !== result.simplified && (
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          간체자: {result.simplified}
                        </Typography>
                      )}
                      
                      <Typography variant="h6" gutterBottom>
                        {result.pronunciation}
                      </Typography>
                      
                      <Typography color="text.secondary">
                        {result.meaning}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                        <Chip 
                          label={`${result.radical}부`} 
                          size="small" 
                          color="secondary"
                          variant="outlined"
                        />
                      </Box>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
          
          {maxPage > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={maxPage}
                page={page}
                onChange={(e, value) => setPage(value)}
                color="primary"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
        </>
      )}
    </Container>
  );
};

export default SearchResultPage; 