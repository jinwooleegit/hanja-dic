import React from 'react';
import { Box, Container, Typography, Link, Divider } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Footer = () => {
  return (
    <Box
      sx={{
        bgcolor: 'background.paper',
        py: 3,
        mt: 'auto',
        borderTop: '1px solid',
        borderColor: 'divider'
      }}
      component="footer"
    >
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ mb: { xs: 2, md: 0 } }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              한자 사전
            </Typography>
            <Typography variant="body2" color="text.secondary">
              한자를 쉽고 빠르게 검색하고 학습할 수 있는 서비스입니다.
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: { xs: 2, sm: 4 } }}>
            <Box>
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                메뉴
              </Typography>
              <Link component={RouterLink} to="/" color="inherit" underline="hover" display="block" sx={{ mb: 1 }}>
                홈
              </Link>
              <Link component={RouterLink} to="/search" color="inherit" underline="hover" display="block" sx={{ mb: 1 }}>
                검색
              </Link>
              <Link component={RouterLink} to="/about" color="inherit" underline="hover" display="block">
                소개
              </Link>
            </Box>
            
            <Box>
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                참고 자료
              </Typography>
              <Link href="https://hanja.dict.naver.com/" target="_blank" rel="noopener" color="inherit" underline="hover" display="block" sx={{ mb: 1 }}>
                네이버 한자사전
              </Link>
              <Link href="https://dict.daum.net/index.do?dic=hanja" target="_blank" rel="noopener" color="inherit" underline="hover" display="block" sx={{ mb: 1 }}>
                다음 한자사전
              </Link>
              <Link href="https://www.unicode.org/charts/PDF/U4E00.pdf" target="_blank" rel="noopener" color="inherit" underline="hover" display="block">
                유니코드 한자
              </Link>
            </Box>
          </Box>
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} 한자 사전. All rights reserved.
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: { xs: 1, sm: 0 } }}>
            개인정보 처리방침 | 이용약관
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer; 