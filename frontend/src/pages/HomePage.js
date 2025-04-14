import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
  useTheme
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import SchoolIcon from '@mui/icons-material/School';
import TranslateIcon from '@mui/icons-material/Translate';

// 인기 한자 목록 (예시 데이터)
const POPULAR_HANJA = [
  { id: 1, character: '愛', pronunciation: '애', meaning: '사랑 애' },
  { id: 2, character: '山', pronunciation: '산', meaning: '메 산' },
  { id: 3, character: '水', pronunciation: '수', meaning: '물 수' },
  { id: 4, character: '日', pronunciation: '일', meaning: '날 일' },
  { id: 5, character: '月', pronunciation: '월', meaning: '달 월' },
  { id: 6, character: '木', pronunciation: '목', meaning: '나무 목' },
  { id: 7, character: '火', pronunciation: '화', meaning: '불 화' },
  { id: 8, character: '金', pronunciation: '금', meaning: '쇠 금' },
  { id: 9, character: '土', pronunciation: '토', meaning: '흙 토' },
  { id: 10, character: '心', pronunciation: '심', meaning: '마음 심' },
];

// 주요 기능 항목
const FEATURES = [
  { 
    title: '한자 검색', 
    icon: <SearchIcon fontSize="large" color="primary" />, 
    description: '한자, 음, 뜻으로 손쉽게 검색하고 결과를 빠르게 확인하세요.' 
  },
  { 
    title: '상세 정보', 
    icon: <MenuBookIcon fontSize="large" color="primary" />, 
    description: '한자의 획순, 부수, 음, 뜻 등 상세 정보를 제공합니다.' 
  },
  { 
    title: '학습 도구', 
    icon: <SchoolIcon fontSize="large" color="primary" />, 
    description: '한자를 효과적으로 학습할 수 있는 다양한 도구를 제공합니다.' 
  },
];

const HomePage = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  
  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };
  
  const handleHanjaClick = (id, character) => {
    navigate(`/hanja/${character}`);
  };

  return (
    <Box sx={{ 
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column'
    }}>
      {/* 히어로 섹션 */}
      <Box 
        sx={{ 
          background: `linear-gradient(to right, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
          pt: 10,
          pb: 8,
          color: 'white'
        }}
      >
        <Container maxWidth="md">
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
              한자 사전
            </Typography>
            <Typography variant="h5" sx={{ mb: 4, fontWeight: 'normal' }}>
              쉽고 빠르게 한자를 검색하고 학습하세요
            </Typography>
            
            <Paper 
              component="form" 
              elevation={3}
              sx={{ 
                p: '12px 16px', 
                display: 'flex', 
                alignItems: 'center',
                maxWidth: 600,
                mx: 'auto',
                borderRadius: 4
              }}
              onSubmit={handleSearch}
            >
              <TextField
                fullWidth
                placeholder="한자, 한글, 뜻으로 검색..."
                variant="standard"
                InputProps={{ disableUnderline: true }}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <Button 
                type="submit"
                variant="contained" 
                sx={{ 
                  borderRadius: 3,
                  ml: 1,
                  px: 3
                }}
              >
                검색
              </Button>
            </Paper>
          </Box>
        </Container>
      </Box>
      
      {/* 인기 한자 섹션 */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Box sx={{ mb: 5 }}>
          <Typography variant="h4" component="h2" gutterBottom textAlign="center">
            자주 찾는 한자
          </Typography>
          <Divider sx={{ width: 100, mx: 'auto', mb: 4, borderColor: theme.palette.primary.main, borderWidth: 2 }} />
          
          <Grid container spacing={2} justifyContent="center">
            {POPULAR_HANJA.map((hanja) => (
              <Grid item key={hanja.id} xs={6} sm={4} md={2}>
                <Card 
                  elevation={2}
                  sx={{ 
                    borderRadius: 2,
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 6,
                    }
                  }}
                >
                  <CardActionArea onClick={() => handleHanjaClick(hanja.id, hanja.character)}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h3" component="div" gutterBottom>
                        {hanja.character}
                      </Typography>
                      <Typography color="text.secondary">
                        {hanja.pronunciation} ({hanja.meaning})
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
      
      {/* 기능 소개 섹션 */}
      <Box sx={{ bgcolor: 'background.paper', py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" component="h2" gutterBottom textAlign="center">
            주요 기능
          </Typography>
          <Divider sx={{ width: 100, mx: 'auto', mb: 6, borderColor: theme.palette.primary.main, borderWidth: 2 }} />
          
          <Grid container spacing={4}>
            {FEATURES.map((feature, index) => (
              <Grid item key={index} xs={12} md={4}>
                <Box sx={{ textAlign: 'center' }}>
                  <Box sx={{ mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" component="h3" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography color="text.secondary">
                    {feature.description}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
      
      {/* CTA 섹션 */}
      <Box 
        sx={{ 
          bgcolor: theme.palette.secondary.main,
          color: theme.palette.secondary.contrastText,
          py: 6
        }}
      >
        <Container maxWidth="md">
          <Box sx={{ textAlign: 'center' }}>
            <TranslateIcon sx={{ fontSize: 48, mb: 2 }} />
            <Typography variant="h4" component="h2" gutterBottom>
              지금 바로 한자 검색을 시작하세요
            </Typography>
            <Typography variant="subtitle1" sx={{ mb: 4 }}>
              한자의 의미와 사용법을 쉽고 빠르게 알아보세요.
            </Typography>
            <Button 
              variant="contained" 
              color="primary"
              size="large"
              onClick={() => navigate('/search')}
              sx={{ 
                px: 4, 
                py: 1.5,
                backgroundColor: theme.palette.primary.dark,
                '&:hover': {
                  backgroundColor: theme.palette.primary.main,
                }
              }}
            >
              검색 시작하기
            </Button>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage; 