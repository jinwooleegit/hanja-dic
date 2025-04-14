import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  Box,
  Grid,
  Divider,
  Button,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import axios from 'axios';

interface HanjaDetail {
  traditional: string;
  simplified: string;
  korean_pronunciation: string;
  chinese_pronunciation: string;
  radical: string;
  stroke_count: number;
  meaning: string;
  examples: string;
  frequency: number;
}

const HanjaDetailPage: React.FC = () => {
  const { character } = useParams<{ character: string }>();
  const [hanja, setHanja] = useState<HanjaDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHanja = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/hanja/${character}`);
        setHanja(response.data);
      } catch (error) {
        console.error('한자 정보를 불러오는 중 오류 발생:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHanja();
  }, [character]);

  if (loading) {
    return (
      <Container>
        <Typography>로딩 중...</Typography>
      </Container>
    );
  }

  if (!hanja) {
    return (
      <Container>
        <Typography>한자를 찾을 수 없습니다.</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
          sx={{ mb: 2 }}
        >
          돌아가기
        </Button>

        <Paper elevation={3} sx={{ p: 3 }}>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Typography variant="h2" component="h1">
              {hanja.traditional}
              {hanja.simplified !== hanja.traditional && (
                <Typography variant="h4" component="span" color="text.secondary">
                  {' '}({hanja.simplified})
                </Typography>
              )}
            </Typography>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Typography variant="h6" gutterBottom>
                발음
              </Typography>
              <Typography>
                한글: {hanja.korean_pronunciation}
                <br />
                중국어: {hanja.chinese_pronunciation}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="h6" gutterBottom>
                기본 정보
              </Typography>
              <Typography>
                부수: {hanja.radical}
                <br />
                획수: {hanja.stroke_count}
                <br />
                검색 횟수: {hanja.frequency}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
            </Grid>

            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                뜻
              </Typography>
              <Typography>{hanja.meaning}</Typography>
            </Grid>

            {hanja.examples && (
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  예시
                </Typography>
                <Typography style={{ whiteSpace: 'pre-line' }}>
                  {hanja.examples}
                </Typography>
              </Grid>
            )}
          </Grid>
        </Paper>
      </Box>
    </Container>
  );
};

export default HanjaDetailPage; 