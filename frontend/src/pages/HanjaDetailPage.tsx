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

const CharacterSection = styled.div`
  text-align: center;
  margin-bottom: 2rem;
`;

const HanjaCharacter = styled.div`
  font-size: 4rem;
  margin-bottom: 1rem;
`;

const SimplifiedCharacter = styled.div`
  font-size: 2rem;
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

const ExamplesSection = styled.div`
  margin-top: 2rem;
`;

const ExampleItem = styled.div`
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 1rem;
`;

interface HanjaDetail {
  id: string;
  traditional: string;
  simplified: string;
  korean_pronunciation: string;
  chinese_pronunciation: string;
  radical: string;
  stroke_count: number;
  meaning: string;
  examples: Array<{
    korean: string;
    hanja: string;
    meaning: string;
  }>;
}

const HanjaDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [hanja, setHanja] = useState<HanjaDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHanjaDetail = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/hanja/${id}`);
        setHanja(response.data);
      } catch (error) {
        console.error('한자 정보를 불러오는 중 오류 발생:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHanjaDetail();
  }, [id]);

  if (loading) {
    return <div>로딩 중...</div>;
  }

  if (!hanja) {
    return <div>한자를 찾을 수 없습니다.</div>;
  }

  return (
    <DetailContainer>
      <Header>
        <BackButton onClick={() => navigate(-1)}>← 돌아가기</BackButton>
        <h1>한자 상세 정보</h1>
      </Header>

      <CharacterSection>
        <HanjaCharacter>{hanja.traditional}</HanjaCharacter>
        {hanja.simplified !== hanja.traditional && (
          <SimplifiedCharacter>{hanja.simplified}</SimplifiedCharacter>
        )}
      </CharacterSection>

      <InfoSection>
        <InfoRow>
          <InfoLabel>한글 발음</InfoLabel>
          <InfoValue>{hanja.korean_pronunciation}</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>중국어 발음</InfoLabel>
          <InfoValue>{hanja.chinese_pronunciation}</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>부수</InfoLabel>
          <InfoValue>{hanja.radical}</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>획수</InfoLabel>
          <InfoValue>{hanja.stroke_count}획</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>의미</InfoLabel>
          <InfoValue>{hanja.meaning}</InfoValue>
        </InfoRow>
      </InfoSection>

      {hanja.examples.length > 0 && (
        <ExamplesSection>
          <h2>예문</h2>
          {hanja.examples.map((example, index) => (
            <ExampleItem key={index}>
              <div>{example.korean}</div>
              <div>{example.hanja}</div>
              <div>{example.meaning}</div>
            </ExampleItem>
          ))}
        </ExamplesSection>
      )}
    </DetailContainer>
  );
};

export default HanjaDetailPage; 