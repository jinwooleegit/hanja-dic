import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Divider,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Skeleton
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import FavoriteIcon from '@mui/icons-material/Favorite';

// 백엔드 API 기본 URL
const API_BASE_URL = 'http://localhost:8000';

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

const FavoritesPage = () => {
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 즐겨찾기 목록 불러오기
  useEffect(() => {
    const fetchFavorites = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get(`${API_BASE_URL}/hanja/favorites`);
        setFavorites(response.data);
      } catch (err) {
        console.error("Favorites API error:", err);
        setError('즐겨찾기 목록을 불러오는 중 오류가 발생했습니다.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchFavorites();
  }, []);

  // 로딩 중 스켈레톤 UI 표시
  const renderSkeletons = () => {
    return Array(8).fill(0).map((_, index) => (
      <Grid item xs={12} sm={6} md={3} key={`skeleton-${index}`}>
        <HanjaCardSkeleton />
      </Grid>
    ));
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/')}
        sx={{ mb: 3 }}
      >
        홈으로
      </Button>
      
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          <FavoriteIcon color="error" sx={{ mr: 1, verticalAlign: 'middle' }} />
          즐겨찾기 한자
        </Typography>
        <Divider sx={{ mb: 3 }} />
        
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        
        {loading ? (
          <Grid container spacing={3}>
            {renderSkeletons()}
          </Grid>
        ) : favorites.length > 0 ? (
          <Grid container spacing={3}>
            {favorites.map((hanja) => (
              <Grid item xs={12} sm={6} md={3} key={hanja.id || hanja.traditional}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardActionArea 
                    component={Link} 
                    to={`/hanja/${encodeURIComponent(hanja.traditional)}`}
                    sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}
                  >
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <Typography variant="h4" component="div" gutterBottom>
                          {hanja.traditional}
                        </Typography>
                        {hanja.frequency && (
                          <Chip 
                            label={`빈도 ${hanja.frequency}`} 
                            size="small" 
                            color="primary"
                            variant="outlined"
                          />
                        )}
                      </Box>
                      
                      <Typography color="text.secondary">
                        {hanja.korean_pronunciation}
                      </Typography>
                      
                      <Typography variant="body2" sx={{ mb: 1.5, fontWeight: 'medium' }}>
                        {hanja.meaning && hanja.meaning.split(',')[0]}
                      </Typography>
                      
                      <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
                        획수: {hanja.stroke_count}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              즐겨찾기한 한자가 없습니다
            </Typography>
            <Button 
              variant="contained" 
              component={Link} 
              to="/search"
              sx={{ mt: 2 }}
            >
              한자 검색하기
            </Button>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default FavoritesPage; 