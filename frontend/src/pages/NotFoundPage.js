import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Container, Typography, Box, Button, Paper } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import HomeIcon from '@mui/icons-material/Home';

const NotFoundPage = () => {
  return (
    <Container maxWidth="md" sx={{ py: 8 }}>
      <Paper 
        elevation={0}
        sx={{ 
          p: 5, 
          borderRadius: 4,
          textAlign: 'center',
          bgcolor: 'background.paper',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center'
        }}
      >
        <Typography 
          variant="h1" 
          gutterBottom
          sx={{ 
            fontSize: { xs: '8rem', md: '12rem' },
            fontWeight: 700,
            fontFamily: '"Noto Serif KR", serif',
            color: 'primary.main',
            letterSpacing: '-4px',
            lineHeight: 1,
            mb: 2
          }}
        >
          誤
        </Typography>
        
        <Typography 
          variant="h4" 
          component="h1" 
          gutterBottom
          sx={{ mb: 1 }}
        >
          페이지를 찾을 수 없습니다
        </Typography>
        
        <Typography 
          variant="body1" 
          color="text.secondary"
          sx={{ mb: 4, maxWidth: 400 }}
        >
          요청하신 페이지가 존재하지 않거나, 이동되었거나, 사용할 수 없는 상태입니다.
        </Typography>
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2 }}>
          <Button
            component={RouterLink}
            to="/"
            variant="contained"
            color="primary"
            size="large"
            startIcon={<HomeIcon />}
          >
            홈으로 이동
          </Button>
          
          <Button
            component={RouterLink}
            to="/search"
            variant="outlined"
            color="primary"
            size="large"
            startIcon={<SearchIcon />}
          >
            한자 검색하기
          </Button>
        </Box>
        
        <Box sx={{ mt: 6, p: 3, bgcolor: 'background.default', borderRadius: 2, maxWidth: 500 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            "誤"는 무슨 뜻인가요?
          </Typography>
          <Typography variant="body2" color="text.secondary">
            한자 '誤(오)'는 '그르칠 오'로, '잘못되다' 또는 '실수하다'라는 의미를 가지고 있습니다.
            404 오류는 웹 페이지를 찾을 수 없을 때 발생합니다.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default NotFoundPage; 