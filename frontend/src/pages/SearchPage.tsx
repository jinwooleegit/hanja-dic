import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios';

const SearchContainer = styled.div`
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
`;

const SearchHeader = styled.div`
  margin-bottom: 2rem;
`;

const SearchTitle = styled.h1`
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 1rem;
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 0.8rem;
  font-size: 1.1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  margin-bottom: 1rem;
`;

const ResultList = styled.div`
  display: grid;
  gap: 1rem;
`;

const ResultItem = styled.div`
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #f5f5f5;
  }
`;

const Word = styled.div`
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
`;

const Pronunciation = styled.div`
  color: #666;
  margin-bottom: 0.5rem;
`;

const Meaning = styled.div`
  color: #333;
`;

const Type = styled.span`
  color: #4a90e2;
  margin-right: 0.5rem;
`;

interface WordResult {
  id: string;
  word: string;
  pronunciation: string;
  meaning: string;
  type: string;
}

const SearchPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState<WordResult[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const query = new URLSearchParams(location.search).get('q');
    if (query) {
      setSearchTerm(query);
      handleSearch(query);
    }
  }, [location]);

  const handleSearch = async (term: string) => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5000/api/search?q=${encodeURIComponent(term)}`);
      setResults(response.data);
    } catch (error) {
      console.error('검색 중 오류 발생:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResultClick = (id: string) => {
    navigate(`/word/${id}`);
  };

  return (
    <SearchContainer>
      <SearchHeader>
        <SearchTitle>검색 결과</SearchTitle>
        <SearchInput
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="다시 검색하기"
        />
      </SearchHeader>

      {loading ? (
        <div>검색 중...</div>
      ) : results.length > 0 ? (
        <ResultList>
          {results.map((result) => (
            <ResultItem key={result.id} onClick={() => handleResultClick(result.id)}>
              <Word>
                {result.word}
                {result.pronunciation && ` [${result.pronunciation}]`}
              </Word>
              <Type>{result.type}</Type>
              <Meaning>{result.meaning}</Meaning>
            </ResultItem>
          ))}
        </ResultList>
      ) : (
        <div>검색 결과가 없습니다.</div>
      )}
    </SearchContainer>
  );
};

export default SearchPage; 