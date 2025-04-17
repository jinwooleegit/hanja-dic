import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios';

const DetailContainer = styled.div`
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
`;

const BackButton = styled.button`
  padding: 0.5rem 1rem;
  background-color: #f5f5f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 1rem;

  &:hover {
    background-color: #e0e0e0;
  }
`;

const WordSection = styled.div`
  text-align: center;
  margin-bottom: 2rem;
`;

const WordText = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
`;

const Pronunciation = styled.div`
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 1rem;
`;

const InfoSection = styled.div`
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
`;

const InfoRow = styled.div`
  display: flex;
  margin-bottom: 1rem;
`;

const InfoLabel = styled.div`
  font-weight: bold;
  width: 120px;
  color: #666;
`;

const InfoValue = styled.div`
  flex: 1;
`;

const ErrorMessage = styled.div`
  color: #ff0000;
  text-align: center;
  margin-top: 2rem;
`;

interface WordDetail {
  id: string;
  word: string;
  pronunciation: string;
  type: string;
  meaning: string;
}

const WordDetailPage: React.FC = () => {
  const { word } = useParams<{ word: string }>();
  const navigate = useNavigate();
  const [wordData, setWordData] = useState<WordDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWordDetail = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/words/${word}`);
        setWordData(response.data);
        setError(null);
      } catch (error) {
        setError('단어를 찾을 수 없습니다.');
        setWordData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchWordDetail();
  }, [word]);

  if (loading) {
    return <div>로딩 중...</div>;
  }

  if (error) {
    return (
      <DetailContainer>
        <Header>
          <BackButton onClick={() => navigate(-1)}>← 돌아가기</BackButton>
        </Header>
        <ErrorMessage>{error}</ErrorMessage>
      </DetailContainer>
    );
  }

  if (!wordData) {
    return null;
  }

  return (
    <DetailContainer>
      <Header>
        <BackButton onClick={() => navigate(-1)}>← 돌아가기</BackButton>
        <h1>단어 상세 정보</h1>
      </Header>

      <WordSection>
        <WordText>{wordData.word}</WordText>
        {wordData.pronunciation && (
          <Pronunciation>[{wordData.pronunciation}]</Pronunciation>
        )}
      </WordSection>

      <InfoSection>
        <InfoRow>
          <InfoLabel>품사</InfoLabel>
          <InfoValue>{wordData.type}</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>의미</InfoLabel>
          <InfoValue>{wordData.meaning}</InfoValue>
        </InfoRow>
      </InfoSection>
    </DetailContainer>
  );
};

export default WordDetailPage; 