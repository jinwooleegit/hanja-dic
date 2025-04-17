import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import axios from 'axios'; // axios 임포트
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
  Alert,
  Skeleton
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import SortIcon from '@mui/icons-material/Sort';
import FilterListIcon from '@mui/icons-material/FilterList';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

// 백엔드 API 기본 URL
const API_BASE_URL = 'http://localhost:8000'; // 환경 변수 등으로 관리하는 것이 좋음

// 로딩 중 스켈레톤 컴포넌트
const HanjaCardSkeleton = () => {
  return (
    <Card sx={{ height: '100%', minHeight: 180 }}>
      <CardContent>
        <Skeleton variant="text" width="80%" height={60} />
        <Skeleton variant="text" width="40%" />
        <Skeleton variant="text" width="60%" />
        <Box sx={{ mt: 2 }}>
          <Skeleton variant="rectangular" width="100%" height={30} />
        </Box>
      </CardContent>
    </Card>
  );
};

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
  const [sortBy, setSortBy] = useState('frequency'); // 기본 정렬: 빈도순
  const [filterBy, setFilterBy] = useState('all');
  
  const itemsPerPage = 8;
  
  // 페이지 변경 시 스크롤을 맨 위로 이동
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [page]);
  
  // 검색어 변경 시 결과 업데이트
  useEffect(() => {
    if (initialQuery) {
      handleSearch(initialQuery);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.search]); // location.search가 변경될 때마다 실행

  const handleSearch = async (queryToSearch = searchQuery) => {
    if (!queryToSearch.trim()) return;
    
    setLoading(true);
    setError(null);
    setPage(1); // 새 검색 시 페이지 1로 초기화
    
    try {
      // 백엔드 API 호출
      const response = await axios.post(`${API_BASE_URL}/hanja/search`, { 
        query: queryToSearch.trim() 
      });
      
      // 데이터 정렬 (초기 로드 시)
      const sortedData = sortData(response.data, sortBy);
      setResults(sortedData);

    } catch (err) {
      console.error("Search API error:", err);
      if (err.response && err.response.status === 404) {
        setError('검색 결과가 없습니다.');
        setResults([]); // 결과 없음 명시적 처리
      } else {
        setError('검색 중 오류가 발생했습니다. 백엔드 서버 상태를 확인해주세요.');
      }
    } finally {
      setLoading(false);
    }
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // URL 업데이트하여 useEffect 트리거
    navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
  };
  
  // 데이터 정렬 함수
  const sortData = (data, sortKey) => {
    return [...data].sort((a, b) => {
      if (sortKey === 'frequency') return (b.frequency || 0) - (a.frequency || 0);
      if (sortKey === 'strokes') return (a.stroke_count || 0) - (b.stroke_count || 0);
      // 다른 정렬 기준 추가 가능
      return 0;
    });
  };

  const handleSortChange = (event) => {
    const newSortBy = event.target.value;
    setSortBy(newSortBy);
    const sortedResults = sortData(results, newSortBy);
    setResults(sortedResults);
  };
  
  const handleFilterChange = (event) => {
    setFilterBy(event.target.value);
    // TODO: 필터링 로직 구현 (API 재호출 또는 클라이언트 측 필터링)
  };
  
  // 현재 페이지에 표시할 결과 계산
  const maxPage = Math.ceil(results.length / itemsPerPage);
  const currentResults = results.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage
  );

  // 로딩 중 스켈레톤 UI 표시
  const renderSkeletons = () => {
    return Array(4).fill(0).map((_, index) => (
      <Grid item xs={12} sm={6} md={3} key={`skeleton-${index}`}>
        <HanjaCardSkeleton />
      </Grid>
    ));
  };

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
          <IconButton type="submit" aria-label="search" disabled={loading}>
            {loading ? <CircularProgress size={24} /> : <SearchIcon />}
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
                disabled // 필터 기능은 아직 미구현
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
      ) : results.length === 0 && initialQuery ? (
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
            {loading ? (
              renderSkeletons()
            ) : currentResults.map((result) => (
              <Grid item key={result.id || result.traditional} xs={12} sm={6} md={3}>
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
                          label={`${result.stroke_count || '-'}획`} 
                          size="small" 
                          color="primary" 
                          variant="outlined"
                        />
                      </Box>
                      
                      {result.simplified && result.traditional !== result.simplified && (
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          간체자: {result.simplified}
                        </Typography>
                      )}
                      
                      <Typography variant="h6" gutterBottom>
                        {result.korean_pronunciation}
                      </Typography>
                      
                      <Typography color="text.secondary" noWrap>
                        {result.meaning}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                        <Chip 
                          label={`${result.radical || '-'}부`} 
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