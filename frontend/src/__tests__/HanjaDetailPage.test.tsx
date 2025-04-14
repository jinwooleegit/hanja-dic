import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import HanjaDetailPage from '../pages/HanjaDetailPage';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('HanjaDetailPage', () => {
  beforeEach(() => {
    mockedAxios.get.mockReset();
  });

  it('로딩 상태 테스트', () => {
    render(
      <BrowserRouter>
        <Routes>
          <Route path="/hanja/:character" element={<HanjaDetailPage />} />
        </Routes>
      </BrowserRouter>
    );

    expect(screen.getByText('로딩 중...')).toBeInTheDocument();
  });

  it('한자 정보 표시 테스트', async () => {
    const mockData = {
      traditional: '測試',
      simplified: '测试',
      korean_pronunciation: '측시',
      chinese_pronunciation: 'cè shì',
      radical: '言',
      stroke_count: 13,
      meaning: '테스트하다',
      examples: '測試用例\n테스트 케이스',
      frequency: 1
    };

    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    render(
      <BrowserRouter>
        <Routes>
          <Route path="/hanja/:character" element={<HanjaDetailPage />} />
        </Routes>
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('測試')).toBeInTheDocument();
      expect(screen.getByText('측시')).toBeInTheDocument();
      expect(screen.getByText('cè shì')).toBeInTheDocument();
      expect(screen.getByText('言')).toBeInTheDocument();
      expect(screen.getByText('13')).toBeInTheDocument();
      expect(screen.getByText('테스트하다')).toBeInTheDocument();
      expect(screen.getByText('測試用例')).toBeInTheDocument();
      expect(screen.getByText('테스트 케이스')).toBeInTheDocument();
    });
  });

  it('한자 찾을 수 없음 테스트', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('Not found'));

    render(
      <BrowserRouter>
        <Routes>
          <Route path="/hanja/:character" element={<HanjaDetailPage />} />
        </Routes>
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('한자를 찾을 수 없습니다.')).toBeInTheDocument();
    });
  });
}); 