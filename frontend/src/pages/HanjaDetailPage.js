import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios'; // axios 임포트
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
import FavoriteIcon from '@mui/icons-material/Favorite';

// 백엔드 API 기본 URL
const API_BASE_URL = 'http://localhost:8000';

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
  const { id: hanjaChar } = useParams(); // URL 파라미터에서 한자 가져오기
  const navigate = useNavigate();
  const [hanjaData, setHanjaData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriteLoading, setFavoriteLoading] = useState(false);

  // 한자 데이터 불러오기
  useEffect(() => {
    const fetchHanjaDetail = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get(`${API_BASE_URL}/hanja/details/${encodeURIComponent(hanjaChar)}`);
        setHanjaData(response.data);
        setIsFavorite(response.data.favorite || false);
      } catch (err) {
        console.error("Hanja Detail API error:", err);
        if (err.response && err.response.status === 404) {
          setError('해당 한자 정보를 찾을 수 없습니다.');
        } else {
          setError('한자 정보를 불러오는 중 오류가 발생했습니다.');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchHanjaDetail();
  }, [hanjaChar]); // URL의 한자가 변경될 때마다 실행

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  // 발음 재생 (Google Text-to-Speech API 연동)
  const playPronunciation = (text, language = 'ko-KR') => {
    setIsPlaying(true);
    
    // Text-to-Speech API를 위한 URL 생성
    // 참고: Google TTS API를 사용하려면 API 키가 필요함
    // 여기서는 Web Speech API를 사용하는 방법으로 구현
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language;
    
    utterance.onend = () => {
      setIsPlaying(false);
    };
    
    utterance.onerror = () => {
      console.error('TTS Error');
      setIsPlaying(false);
    };
    
    window.speechSynthesis.speak(utterance);
  };
  
  // 한국어 발음 재생
  const playKoreanPronunciation = () => {
    if (!hanjaData || !hanjaData.korean_pronunciation) return;
    playPronunciation(hanjaData.korean_pronunciation, 'ko-KR');
  };
  
  // 중국어 발음 재생
  const playChinesePronunciation = () => {
    if (!hanjaData || !hanjaData.chinese_pronunciation) return;
    playPronunciation(hanjaData.chinese_pronunciation, 'zh-CN');
  };
  
  // 일본어 발음 재생
  const playJapanesePronunciation = () => {
    if (!hanjaData || !hanjaData.japanese_pronunciation) return;
    playPronunciation(hanjaData.japanese_pronunciation, 'ja-JP');
  };
  
  // 공유하기
  const shareHanja = () => {
    if (navigator.share && hanjaData) {
      navigator.share({
        title: `한자 사전 - ${hanjaData.traditional}`,
        text: `${hanjaData.traditional} (${hanjaData.korean_pronunciation || '-'}) - ${hanjaData.meaning || '-'}`,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href)
        .then(() => alert('링크가 클립보드에 복사되었습니다.'))
        .catch(() => alert('링크 복사에 실패했습니다.'));
    }
  };

  // 즐겨찾기 토글
  const toggleFavorite = async () => {
    if (!hanjaData) return;
    
    setFavoriteLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/hanja/favorite/${encodeURIComponent(hanjaChar)}`);
      setIsFavorite(response.data.favorite);
      // 토스트 메시지 표시 (선택사항)
      const message = response.data.favorite ? '즐겨찾기에 추가되었습니다.' : '즐겨찾기에서 제거되었습니다.';
      alert(message); // 실제 구현시 토스트 컴포넌트로 대체
    } catch (err) {
      console.error("Favorite toggle error:", err);
      alert('즐겨찾기 상태 변경 중 오류가 발생했습니다.');
    } finally {
      setFavoriteLoading(false);
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

  // 데이터 구조 접근 시 null 체크 추가
  const pronunciation = hanjaData.pronunciation || {};
  const chinesePronunciation = pronunciation.chinese || {};
  const history = hanjaData.history || {};
  const examples = hanjaData.examples || [];
  const compounds = hanjaData.compounds || [];
  const meanings = hanjaData.meanings || [hanjaData.meaning]; // 기본 뜻을 배열로 처리

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
                {hanjaData.traditional !== hanjaData.simplified && hanjaData.simplified && (
                  <Chip 
                    label={`간체자: ${hanjaData.simplified}`}
                    size="small"
                    sx={{ mb: 1 }}
                  />
                )}
                <Chip 
                  label={`${hanjaData.stroke_count || '-'}획`} 
                  color="primary"
                  size="small"
                />
              </Box>
            </Box>
            
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
              <Typography variant="h4" component="div">
                {hanjaData.korean_pronunciation || '-'}
              </Typography>
              <IconButton 
                size="small" 
                onClick={playKoreanPronunciation} 
                sx={{ ml: 1 }}
                disabled={isPlaying || !hanjaData.korean_pronunciation}
              >
                <VolumeUpIcon fontSize="small" color={isPlaying ? "primary" : "action"} />
              </IconButton>
            </Box>
            
            {/* 중국어 발음 */}
            {hanjaData.chinese_pronunciation && (
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
                <Typography variant="body1" color="text.secondary">
                  중국어: {hanjaData.chinese_pronunciation}
                </Typography>
                <IconButton 
                  size="small" 
                  onClick={playChinesePronunciation} 
                  sx={{ ml: 1 }}
                  disabled={isPlaying}
                >
                  <VolumeUpIcon fontSize="small" />
                </IconButton>
              </Box>
            )}
            
            {/* 일본어 발음 */}
            {hanjaData.japanese_pronunciation && (
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
                <Typography variant="body1" color="text.secondary">
                  일본어: {hanjaData.japanese_pronunciation}
                </Typography>
                <IconButton 
                  size="small" 
                  onClick={playJapanesePronunciation} 
                  sx={{ ml: 1 }}
                  disabled={isPlaying}
                >
                  <VolumeUpIcon fontSize="small" />
                </IconButton>
              </Box>
            )}
            
            <Typography variant="h6" color="text.secondary" gutterBottom>
              {hanjaData.meaning || '-'}
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
              {meanings.map((meaning, index) => (
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
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
              <ButtonGroup variant="outlined" aria-label="한자 기능">
                <Button 
                  startIcon={isFavorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
                  onClick={toggleFavorite}
                  disabled={favoriteLoading}
                >
                  {isFavorite ? '즐겨찾기 됨' : '즐겨찾기'}
                </Button>
                <Button startIcon={<ShareIcon />} onClick={shareHanja}>
                  공유하기
                </Button>
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
                      {hanjaData.radical || '-'}
                    </Typography>
                    <Typography color="text.secondary">
                      {history.radicalMeaning || '-'}
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
                    {hanjaData.level || '-'}
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
                        {chinesePronunciation.pinyin || '-'}
                      </Typography>
                    </Box>
                    <Divider orientation="vertical" flexItem />
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        중국어(광동어)
                      </Typography>
                      <Typography>
                        {chinesePronunciation.cantonese || '-'}
                      </Typography>
                    </Box>
                    <Divider orientation="vertical" flexItem />
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        일본어
                      </Typography>
                      <Typography>
                        {pronunciation.japanese || '-'}
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
        {compounds.length > 0 ? (
          <Grid container spacing={2}>
            {compounds.map((compound) => (
              <Grid item key={compound.id || compound.hanja} xs={12} sm={6} md={4}>
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
        ) : (
          <Typography color="text.secondary">관련 단어 정보가 없습니다.</Typography>
        )}
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
                secondary={`${hanjaData.traditional}${hanjaData.simplified && hanjaData.traditional !== hanjaData.simplified ? ' (간체자: ' + hanjaData.simplified + ')' : ''}`}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="독음" 
                secondary={hanjaData.korean_pronunciation || '-'}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="뜻" 
                secondary={hanjaData.meaning || '-'}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="부수" 
                secondary={`${hanjaData.radical || '-'} (${history.radicalMeaning || '-'})`}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="획수" 
                secondary={hanjaData.stroke_count || '-'}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="급수" 
                secondary={hanjaData.level || '-'}
              />
            </ListItem>
            <Divider component="li" />
            <ListItem>
              <ListItemText 
                primary="빈도" 
                secondary={`${hanjaData.frequency !== undefined ? hanjaData.frequency + '%' : '-'} ${hanjaData.frequency !== undefined ? '(자주 사용됨)' : ''}`}
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
        {examples.length > 0 ? (
          <List>
            {examples.map((example, index) => (
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
                {index < examples.length - 1 && <Divider component="li" />}
              </React.Fragment>
            ))}
          </List>
        ) : (
          <Typography color="text.secondary">예문 정보가 없습니다.</Typography>
        )}
      </TabPanel>
      
      {/* 어원 탭 패널 */}
      <TabPanel value={tabValue} index={3}>
        <Typography variant="h6" gutterBottom>
          한자 어원
        </Typography>
        <Paper variant="outlined" sx={{ p: 3, borderRadius: 2, mb: 3 }}>
          <Typography variant="body1" paragraph>
            {history.origin || '어원 정보가 없습니다.'}
          </Typography>
          
          {history.evolution && history.evolution.length > 0 && (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
              {history.evolution.map((stage, index) => (
                <Chip key={index} label={stage} variant="outlined" />
              ))}
            </Box>
          )}
          
          {history.similar && history.similar.length > 0 && (
            <>
              <Typography variant="subtitle1" gutterBottom>
                유사 한자
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
                {history.similar.map((char, index) => (
                  <Chip 
                    key={index} 
                    label={char} 
                    color="primary"
                    onClick={() => navigate(`/hanja/${char}`)}
                    clickable
                  />
                ))}
              </Box>
            </>
          )}
        </Paper>
      </TabPanel>
    </Container>
  );
};

export default HanjaDetailPage; 