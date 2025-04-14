import re
from typing import Dict, List, Optional
from .validator import HanjaValidator

class HanjaCleaner:
    @staticmethod
    def clean_pronunciation(text: str) -> str:
        """발음을 정제합니다."""
        # 괄호와 그 안의 내용 제거
        text = re.sub(r'\([^)]*\)', '', text)
        # 쉼표로 구분된 여러 발음 중 첫 번째 것만 사용
        text = text.split(',')[0].strip()
        return text
    
    @staticmethod
    def clean_meaning(text: str) -> str:
        """뜻을 정제합니다."""
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def clean_examples(text: str) -> str:
        """예문을 정제합니다."""
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        # 예문을 줄바꿈으로 구분
        examples = [ex.strip() for ex in text.split('\n') if ex.strip()]
        return '\n'.join(examples)
    
    @staticmethod
    def clean_hanja_data(data: Dict) -> Dict:
        """한자 데이터를 정제합니다."""
        cleaned = data.copy()
        
        # 발음 정제
        if 'korean_pronunciation' in cleaned:
            cleaned['korean_pronunciation'] = HanjaCleaner.clean_pronunciation(
                cleaned['korean_pronunciation']
            )
        
        if 'chinese_pronunciation' in cleaned:
            cleaned['chinese_pronunciation'] = HanjaCleaner.clean_pronunciation(
                cleaned['chinese_pronunciation']
            )
        
        # 뜻 정제
        if 'meaning' in cleaned:
            cleaned['meaning'] = HanjaCleaner.clean_meaning(cleaned['meaning'])
        
        # 예문 정제
        if 'examples' in cleaned:
            cleaned['examples'] = HanjaCleaner.clean_examples(cleaned['examples'])
        
        return cleaned
    
    @staticmethod
    def remove_duplicates(data_list: List[Dict]) -> List[Dict]:
        """중복된 한자 데이터를 제거합니다."""
        seen = set()
        unique_data = []
        
        for data in data_list:
            # 번체자를 기준으로 중복 체크
            key = data.get('traditional')
            if key and key not in seen:
                seen.add(key)
                unique_data.append(data)
        
        return unique_data
    
    @staticmethod
    def merge_hanja_data(data_list: List[Dict]) -> Dict:
        """여러 출처의 한자 데이터를 병합합니다."""
        if not data_list:
            return {}
        
        merged = {}
        sources = []
        
        for data in data_list:
            # 데이터 정제
            cleaned = HanjaCleaner.clean_hanja_data(data)
            
            # 필수 필드가 있는지 확인
            if not cleaned.get('traditional'):
                continue
            
            # 출처 추가
            sources.append(cleaned.get('source', 'unknown'))
            
            # 데이터 병합
            for key, value in cleaned.items():
                if value and (key not in merged or not merged[key]):
                    merged[key] = value
        
        # 출처 정보 추가
        if sources:
            merged['sources'] = list(set(sources))
        
        return merged 