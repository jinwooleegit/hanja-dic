import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Divider,
  Button,
  Tabs,
  Tab,
  Chip,
  List,
  ListItem,
  ListItemText,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  ButtonGroup,
  useTheme,
  IconButton
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import TranslateIcon from '@mui/icons-material/Translate';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import ShareIcon from '@mui/icons-material/Share';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';

// 상세 한자 정보 (실제로는 API 호출로 데이터를 가져옴)
const MOCK_HANJA_DETAIL = {
  id: 1,
  traditional: '愛',
  simplified: '爱',
  pronunciation: {
    korean: '애',
    chinese: {
      pinyin: 'ài',
      cantonese: 'oi3'
    },
    japanese: 'ai',
  },
  meaning: '사랑 애',
  meanings: [
    '사랑하다',
    '좋아하다',
    '귀여워하다',
    '아끼다',
    '친애하다'
  ],
  radical: '心',
  radicalMeaning: '마음 심',
  strokes: 13,
  level: '초등학교 5학년',
  frequency: 98,
  examples: [
    { hanja: '愛情', hangul: '애정', meaning: '사랑하는 마음' },
    { hanja: '戀愛', hangul: '연애', meaning: '남녀 간의 사랑' },
    { hanja: '博愛', hangul: '박애', meaning: '널리 사랑함' },
    { hanja: '慈愛', hangul: '자애', meaning: '사랑과 자비' },
    { hanja: '親愛', hangul: '친애', meaning: '친하고 사랑함' }
  ],
  compounds: [
    { id: 101, hanja: '愛國', pronunciation: '애국', meaning: '나라를 사랑함' },
    { id: 102, hanja: '愛好', pronunciation: '애호', meaning: '좋아하고 즐김' },
    { id: 103, hanja: '愛人', pronunciation: '애인', meaning: '사랑하는 사람' },
    { id: 104, hanja: '友愛', pronunciation: '우애', meaning: '친구로서 사랑함' },
    { id: 105, hanja: '自愛', pronunciation: '자애', meaning: '자신을 사랑함' },
    { id: 106, hanja: '愛護', pronunciation: '애호', meaning: '사랑하고 보호함' }
  ],
  history: {
    origin: '갑골문에서는 사람이 무릎을 꿇고 있는 모습을 나타내었으며, 후에 \'마음(心)\'이 추가되어 정성스러운 마음을 표현하게 되었다.',
    evolution: ['갑골문', '금문', '전서', '예서', '해서'],
    similar: ['憐', '恩', '慈']
  }
};

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ py: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
};

const HanjaDetailPage = () => {
  const theme = useTheme();
  const { id } = useParams();
  const navigate = useNavigate();
  const [hanjaData, setHanjaData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);

  // 한자 데이터 불러오기 (API 호출 시뮬레이션)
  useEffect(() => {
    setLoading(true);
    setError(null);
    
    // 실제 구현에서는 API 호출로 변경
    const timer = setTimeout(() => {
      try {
        setHanjaData(MOCK_HANJA_DETAIL);
        setLoading(false);
      } catch (err) {
        setError('한자 정보를 불러오는 중 오류가 발생했습니다.');
        setLoading(false);
      }
    }, 800);
    
    return () => clearTimeout(timer);
  }, [id]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  // 발음 재생 (실제로는 발음 API와 연동해야 함)
  const playPronunciation = () => {
    alert('한자 발음 재생 기능은 준비 중입니다.');
  };
  
  // 공유하기
  const shareHanja = () => {
    if (navigator.share) {
      navigator.share({
        title: `한자 사전 - ${hanjaData.traditional}`,
        text: `${hanjaData.traditional} (${hanjaData.pronunciation.korean}) - ${hanjaData.meaning}`,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href)
        .then(() => alert('링크가 클립보드에 복사되었습니다.'))
        .catch(() => alert('링크 복사에 실패했습니다.'));
    }
  };

  if (loading) {
    return (
      <Container>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error || !hanjaData) {
    return (
      <Container>
        <Box sx={{ mt: 4 }}>
          <Alert severity="error">
            {error || '한자 정보를 찾을 수 없습니다.'}
          </Alert>
          <Button 
            startIcon={<ArrowBackIcon />} 
            onClick={() => navigate(-1)}
            sx={{ mt: 2 }}
          >
            뒤로 가기
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate(-1)}
        sx={{ mb: 3 }}
      >
        뒤로 가기
      </Button>
      
      {/* 한자 기본 정보 카드 */}
      <Paper 
        elevation={2} 
        sx={{ 
          p: 3, 
          mb: 4, 
          borderRadius: 2,
          background: `linear-gradient(to right, ${theme.palette.primary.main}15, ${theme.palette.background.paper})` 
        }}
      >
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
              <Typography variant="h1" component="div" gutterBottom sx={{ fontSize: '5rem', lineHeight: 1.2 }}>
                {hanjaData.traditional}
              </Typography>
              
              <Box>
                {hanjaData.traditional !== hanjaData.simplified && (
                  <Chip 
                    label={`간체자: ${hanjaData.simplified}`} 
                    size="small" 
                    sx={{ mb: 1 }}
                  />
                )}
                <Chip 
                  label={`${hanjaData.strokes}획`} 
                  color="primary"
                  size="small" 
                />
              </Box>
            </Box>
            
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
              <Typography variant="h4" component="div">
                {hanjaData.pronunciation.korean}
              </Typography>
              <IconButton size="small" onClick={playPronunciation} sx={{ ml: 1 }}>
                <VolumeUpIcon fontSize="small" />
              </IconButton>
            </Box>
            
            <Typography variant="h6" color="text.secondary" gutterBottom>
              {hanjaData.meaning}
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
              {hanjaData.meanings.map((meaning, index) => (
                <Chip 
                  key={index}
                  label={meaning} 
                  color="secondary"
                  variant="outlined"
                  size="small"
                />
              ))}
            </Box>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', justifyContent: { xs: 'flex-start', md: 'flex-end' } }}>
              <ButtonGroup variant="outlined" size="small" sx={{ mb: 2 }}>
                <Button startIcon={<SaveAltIcon />}>저장</Button>
                <Button startIcon={<ShareIcon />} onClick={shareHanja}>공유</Button>
                <Button startIcon={<FavoriteBorderIcon />}>즐겨찾기</Button>
              </ButtonGroup>
            </Box>
            
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Paper variant="outlined" sx={{ p: 2, borderRadius: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    부수
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="h5">
                      {hanjaData.radical}
                    </Typography>
                    <Typography color="text.secondary">
                      {hanjaData.radicalMeaning}
                    </Typography>
                  </Box>
                </Paper>
              </Grid>
              
              <Grid item xs={6}>
                <Paper variant="outlined" sx={{ p: 2, borderRadius: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    급수
                  </Typography>
                  <Typography variant="h5">
                    {hanjaData.level}
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={12}>
                <Paper variant="outlined" sx={{ p: 2, borderRadius: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    외국어 발음
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        중국어(병음)
                      </Typography>
                      <Typography>
                        {hanjaData.pronunciation.chinese.pinyin}
                      </Typography>
                    </Box>
                    <Divider orientation="vertical" flexItem />
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        중국어(광동어)
                      </Typography>
                      <Typography>
                        {hanjaData.pronunciation.chinese.cantonese}
                      </Typography>
                    </Box>
                    <Divider orientation="vertical" flexItem />
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        일본어
                      </Typography>
                      <Typography>
                        {hanjaData.pronunciation.japanese}
                      </Typography>
                    </Box>
                  </Box>
                </Paper>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
      
      {/* 탭 네비게이션 */}
      <Box sx={{ mb: 2 }}>
        <Tabs 
          value={tabValue} 
          onChange={handleTabChange} 
          variant="scrollable"
          scrollButtons="auto"
          textColor="primary"
          indicatorColor="primary"
        >
          <Tab icon={<MenuBookIcon />} label="단어" />
          <Tab icon={<InfoOutlinedIcon />} label="상세정보" />
          <Tab icon={<FormatListBulletedIcon />} label="예문" />
          <Tab icon={<TranslateIcon />} label="어원" />
        </Tabs>
      </Box>
      
      {/* 단어 탭 패널 */}
      <TabPanel value={tabValue} index={0}>
        <Typography variant="h6" gutterBottom>
          관련 단어
        </Typography>
        <Grid container spacing={2}>
          {hanjaData.compounds.map((compound) => (
            <Grid item key={compound.id} xs={12} sm={6} md={4}>
              <Card 
                variant="outlined"
                sx={{ 
                  height: '100%', 
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 2,
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Typography variant="h6">
                      {compound.hanja}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                      {compound.pronunciation}
                    </Typography>
                  </Box>
                  <Typography color="text.secondary">
                    {compound.meaning}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>
      
      {/* 상세정보 탭 패널 */}
      <TabPanel value={tabValue} index={1}>
        <Typography variant="h6" gutterBottom>
          한자 정보
        </Typography>
        <Paper variant="outlined" sx={{ p: 3, borderRadius: 2 }}>
          <List>
            <ListItem>
              <ListItemText 
                primary="한자" 
                secondary={`${hanjaData.traditional}${hanjaData.traditional !== hanjaData.simplified ? ' (간체자: ' + hanjaData.simplified + ')' : ''}`}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="독음" 
                secondary={hanjaData.pronunciation.korean}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="뜻" 
                secondary={hanjaData.meaning}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="부수" 
                secondary={`${hanjaData.radical} (${hanjaData.radicalMeaning})`}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="획수" 
                secondary={hanjaData.strokes}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="급수" 
                secondary={hanjaData.level}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="빈도" 
                secondary={`${hanjaData.frequency}% (자주 사용됨)`}
              />
            </ListItem>
          </List>
        </Paper>
      </TabPanel>
      
      {/* 예문 탭 패널 */}
      <TabPanel value={tabValue} index={2}>
        <Typography variant="h6" gutterBottom>
          예문
        </Typography>
        <List>
          {hanjaData.examples.map((example, index) => (
            <React.Fragment key={index}>
              <ListItem>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography variant="h6" component="span">
                        {example.hanja}
                      </Typography>
                      <Typography 
                        variant="body1" 
                        component="span" 
                        color="text.secondary"
                        sx={{ ml: 2 }}
                      >
                        {example.hangul}
                      </Typography>
                    </Box>
                  }
                  secondary={example.meaning}
                />
              </ListItem>
              {index < hanjaData.examples.length - 1 && <Divider component="li" />}
            </React.Fragment>
          ))}
        </List>
      </TabPanel>
      
      {/* 어원 탭 패널 */}
      <TabPanel value={tabValue} index={3}>
        <Typography variant="h6" gutterBottom>
          한자 어원
        </Typography>
        <Paper variant="outlined" sx={{ p: 3, borderRadius: 2, mb: 3 }}>
          <Typography variant="body1" paragraph>
            {hanjaData.history.origin}
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
            {hanjaData.history.evolution.map((stage, index) => (
              <Chip key={index} label={stage} variant="outlined" />
            ))}
          </Box>
          
          <Typography variant="subtitle1" gutterBottom>
            유사 한자
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            {hanjaData.history.similar.map((char, index) => (
              <Chip 
                key={index} 
                label={char} 
                color="primary"
                onClick={() => navigate(`/hanja/${char}`)}
              />
            ))}
          </Box>
        </Paper>
      </TabPanel>
    </Container>
  );
};

export default HanjaDetailPage; 