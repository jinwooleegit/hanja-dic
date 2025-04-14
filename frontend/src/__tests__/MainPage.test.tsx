import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import MainPage from '../pages/MainPage';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('MainPage', () => {
  beforeEach(() => {
    mockedAxios.get.mockReset();
  });

  it('렌더링 테스트', () => {
    render(
      <BrowserRouter>
        <MainPage />
      </BrowserRouter>
    );
    
    expect(screen.getByText('한자 사전')).toBeInTheDocument();
    expect(screen.getByLabelText('한자 또는 발음 검색')).toBeInTheDocument();
  });

  it('검색 기능 테스트', async () => {
    const mockData = [
      {
        traditional: '測試',
        simplified: '测试',
        korean_pronunciation: '측시',
        chinese_pronunciation: 'cè shì',
        meaning: '테스트하다',
      }
    ];

    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    render(
      <BrowserRouter>
        <MainPage />
      </BrowserRouter>
    );

    const searchInput = screen.getByLabelText('한자 또는 발음 검색');
    fireEvent.change(searchInput, { target: { value: '測試' } });
    fireEvent.keyPress(searchInput, { key: 'Enter', code: 'Enter' });

    await waitFor(() => {
      expect(screen.getByText('測試')).toBeInTheDocument();
      expect(screen.getByText('측시')).toBeInTheDocument();
      expect(screen.getByText('테스트하다')).toBeInTheDocument();
    });
  });

  it('검색 결과 클릭 테스트', async () => {
    const mockData = [
      {
        traditional: '測試',
        simplified: '测试',
        korean_pronunciation: '측시',
        chinese_pronunciation: 'cè shì',
        meaning: '테스트하다',
      }
    ];

    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    render(
      <BrowserRouter>
        <MainPage />
      </BrowserRouter>
    );

    const searchInput = screen.getByLabelText('한자 또는 발음 검색');
    fireEvent.change(searchInput, { target: { value: '測試' } });
    fireEvent.keyPress(searchInput, { key: 'Enter', code: 'Enter' });

    await waitFor(() => {
      const resultItem = screen.getByText('測試');
      fireEvent.click(resultItem);
    });

    expect(window.location.pathname).toBe('/hanja/測試');
  });
}); 