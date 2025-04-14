import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  Grid, 
  Divider, 
  List, 
  ListItem,
  ListItemIcon,
  ListItemText,
  Card,
  CardContent,
  Avatar,
  useTheme
} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import HistoryEduIcon from '@mui/icons-material/HistoryEdu';
import EmojiObjectsIcon from '@mui/icons-material/EmojiObjects';
import LocalLibraryIcon from '@mui/icons-material/LocalLibrary';

const AboutPage = () => {
  const theme = useTheme();

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* 소개 섹션 */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          한자 사전 소개
        </Typography>
        <Divider sx={{ width: 100, borderColor: theme.palette.primary.main, borderWidth: 2, mb: 4 }} />
        
        <Typography variant="body1" paragraph>
          한자 사전은 누구나 쉽게 한자를 검색하고 학습할 수 있도록 제작된 웹 서비스입니다. 한자의 기본 정보부터 어원, 관련 단어까지 다양한 정보를 제공합니다.
        </Typography>
        
        <Typography variant="body1" paragraph>
          한국어에 포함된 한자어의 이해는 우리말을 올바르게 사용하고 이해하는 데 큰 도움이 됩니다. 
          또한 중국어, 일본어 등 한자 문화권 언어를 학습하는 데에도 기반이 됩니다.
        </Typography>
      </Box>
      
      {/* 주요 기능 섹션 */}
      <Paper elevation={2} sx={{ p: 4, mb: 6, borderRadius: 2 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          주요 기능
        </Typography>
        
        <List>
          <ListItem>
            <ListItemIcon>
              <CheckCircleOutlineIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="한자 검색" 
              secondary="한자, 한글 발음, 뜻으로 검색 가능합니다."
            />
          </ListItem>
          
          <ListItem>
            <ListItemIcon>
              <CheckCircleOutlineIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="상세 정보 제공" 
              secondary="한자의 획수, 부수, 어원, 정의 등 다양한 정보를 제공합니다."
            />
          </ListItem>
          
          <ListItem>
            <ListItemIcon>
              <CheckCircleOutlineIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="관련 단어 및 예문" 
              secondary="한자를 활용한 단어와 예문을 통해 실제 사용법을 익힐 수 있습니다."
            />
          </ListItem>
          
          <ListItem>
            <ListItemIcon>
              <CheckCircleOutlineIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="다국어 발음 지원" 
              secondary="한국어, 중국어(표준어/광동어), 일본어 발음을 제공합니다."
            />
          </ListItem>
        </List>
      </Paper>
      
      {/* 한자 학습의 중요성 섹션 */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          한자 학습의 중요성
        </Typography>
        <Divider sx={{ width: 100, borderColor: theme.palette.primary.main, borderWidth: 2, mb: 4 }} />
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: theme.palette.primary.main, width: 60, height: 60 }}>
                    <HistoryEduIcon fontSize="large" />
                  </Avatar>
                </Box>
                <Typography variant="h6" component="h3" gutterBottom align="center">
                  언어 이해력 향상
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  우리말의 약 60%는 한자어로 구성되어 있습니다. 한자를 알면 단어의 의미를 더 정확하게 이해할 수 있고, 어휘력이 풍부해집니다.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: theme.palette.primary.main, width: 60, height: 60 }}>
                    <EmojiObjectsIcon fontSize="large" />
                  </Avatar>
                </Box>
                <Typography variant="h6" component="h3" gutterBottom align="center">
                  사고력 발달
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  한자는 형태, 소리, 의미가 결합된 문자로, 한자 학습은 논리적 사고력과 분석력을 키우는 데 도움이 됩니다.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: theme.palette.primary.main, width: 60, height: 60 }}>
                    <LocalLibraryIcon fontSize="large" />
                  </Avatar>
                </Box>
                <Typography variant="h6" component="h3" gutterBottom align="center">
                  동아시아 문화 이해
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  한자는 동아시아 문화권의 공통된 문자로, 한자를 통해 중국, 일본 등 한자 문화권의 문화와 사고방식을 이해할 수 있습니다.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
      
      {/* 데이터 출처 섹션 */}
      <Paper variant="outlined" sx={{ p: 4, mb: 6, borderRadius: 2 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          데이터 출처
        </Typography>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          한자 사전의 데이터는 다음과 같은 출처에서 수집되었습니다:
        </Typography>
        
        <List dense>
          <ListItem>
            <ListItemText 
              primary="국립국어원 표준국어대사전"
              secondary="https://stdict.korean.go.kr"
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="네이버 한자사전"
              secondary="https://hanja.dict.naver.com"
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="Unicode Han Database"
              secondary="https://unicode.org/charts/unihan.html"
            />
          </ListItem>
        </List>
        
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          본 사이트는 교육 및 개인 학습 목적으로 제작되었으며, 모든 저작권은 원 출처에 있습니다.
        </Typography>
      </Paper>
      
      {/* 연락처 섹션 */}
      <Box>
        <Typography variant="h5" component="h2" gutterBottom>
          연락처
        </Typography>
        <Divider sx={{ width: 100, borderColor: theme.palette.primary.main, borderWidth: 2, mb: 4 }} />
        
        <Typography variant="body1" paragraph>
          한자 사전에 대한 문의사항이나 개선 제안은 아래로 연락주세요.
        </Typography>
        
        <Typography variant="body1">
          이메일: contact@hanjadictionary.com
        </Typography>
      </Box>
    </Container>
  );
};

export default AboutPage; 