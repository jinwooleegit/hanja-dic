from typing import Dict, List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .national_scraper import NationalScraper
from .naver_scraper import NaverScraper
from .daum_scraper import DaumScraper
from app.utils.validator import HanjaValidator
from app.utils.cleaner import HanjaCleaner
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class ScraperManager:
    def __init__(self):
        self.scrapers = [
            NaverScraper(),
            DaumScraper(),
            NationalScraper()
        ]
        self.executor = ThreadPoolExecutor(max_workers=3)
        
    async def search_hanja(self, query: str) -> Dict:
        """여러 스크레이퍼를 병렬로 실행하여 한자 검색 결과를 수집합니다."""
        try:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(self.executor, scraper.search, query)
                for scraper in self.scrapers
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 유효한 결과만 필터링
            valid_results = []
            for result in results:
                if isinstance(result, dict) and 'traditional' in result:
                    valid_results.append(result)
                elif isinstance(result, Exception):
                    logger.error(f"스크레이퍼 실행 중 오류: {str(result)}")
            
            if not valid_results:
                logger.warning(f"'{query}'에 대한 유효한 검색 결과 없음")
                return {}
                
            # 결과 병합 및 정제
            merged_data = HanjaCleaner.merge_hanja_data(valid_results)
            
            # 데이터 검증
            validation_errors = HanjaValidator.validate_hanja_data(merged_data)
            if validation_errors:
                logger.error(f"데이터 검증 실패: {validation_errors}")
                return {}
                
            logger.info(f"'{query}'에 대한 검색 결과 병합 완료: {merged_data.get('traditional')}")
            return merged_data
            
        except Exception as e:
            logger.error(f"한자 검색 중 오류 발생: {str(e)}")
            return {}
    
    async def search_hanja_async(self, query: str) -> Dict:
        """여러 스크레이퍼를 비동기적으로 실행하여 한자 검색 결과를 수집합니다."""
        try:
            tasks = [scraper.search_hanja_async(query) for scraper in self.scrapers]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 유효한 결과만 필터링
            valid_results = []
            for result in results:
                if isinstance(result, dict) and 'traditional' in result:
                    valid_results.append(result)
                elif isinstance(result, Exception):
                    logger.error(f"비동기 스크레이퍼 실행 중 오류: {str(result)}")
            
            if not valid_results:
                logger.warning(f"'{query}'에 대한 유효한 비동기 검색 결과 없음")
                return {}
                
            # 결과 병합 및 정제
            merged_data = HanjaCleaner.merge_hanja_data(valid_results)
            
            # 데이터 검증
            validation_errors = HanjaValidator.validate_hanja_data(merged_data)
            if validation_errors:
                logger.error(f"비동기 데이터 검증 실패: {validation_errors}")
                return {}
                
            logger.info(f"'{query}'에 대한 비동기 검색 결과 병합 완료: {merged_data.get('traditional')}")
            return merged_data
            
        except Exception as e:
            logger.error(f"비동기 한자 검색 중 오류 발생: {str(e)}")
            return {}
            
    def _run_scraper(self, scraper, query: str) -> Dict:
        """개별 스크레이퍼를 실행하고 결과를 반환합니다."""
        try:
            return scraper.search(query)
        except Exception as e:
            logger.error(f"{scraper.__class__.__name__} 실행 중 오류: {str(e)}")
            return {}
            
    def merge_results(self, results: List[Dict]) -> List[Dict]:
        """여러 스크레이퍼의 결과를 병합합니다."""
        try:
            # 데이터 정제
            cleaned_results = [HanjaCleaner.clean_hanja_data(result) for result in results]
            
            # 중복 제거
            unique_results = HanjaCleaner.remove_duplicates(cleaned_results)
            
            # 데이터 검증
            validated_results = []
            for result in unique_results:
                validation_errors = HanjaValidator.validate_hanja_data(result)
                if not validation_errors:
                    validated_results.append(result)
                else:
                    logger.warning(f"데이터 검증 실패: {validation_errors}")
                    
            return validated_results
            
        except Exception as e:
            logger.error(f"결과 병합 중 오류 발생: {str(e)}")
            return []

# 싱글톤 인스턴스 생성
scraper_manager = ScraperManager() 