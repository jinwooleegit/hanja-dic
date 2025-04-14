import re
from typing import Dict, Optional, List
from unidecode import unidecode

class HanjaValidator:
    @staticmethod
    def is_valid_hanja(char: str) -> bool:
        """한자가 유효한지 검사합니다."""
        # 한자 범위: 4E00-9FFF (CJK Unified Ideographs)
        return bool(re.match(r'^[\u4e00-\u9fff]$', char))
    
    @staticmethod
    def is_valid_korean_pronunciation(text: str) -> bool:
        """한글 발음이 유효한지 검사합니다."""
        # 한글 범위: 가-힣
        return bool(re.match(r'^[가-힣\s]+$', text))
    
    @staticmethod
    def is_valid_pinyin(text: str) -> bool:
        """병음이 유효한지 검사합니다."""
        # 병음 패턴: 알파벳과 성조(1-4)로 구성
        return bool(re.match(r'^[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+$', text))
    
    @staticmethod
    def is_valid_radical(char: str) -> bool:
        """부수가 유효한지 검사합니다."""
        return HanjaValidator.is_valid_hanja(char)
    
    @staticmethod
    def is_valid_stroke_count(count: int) -> bool:
        """획수가 유효한지 검사합니다."""
        return 1 <= count <= 64  # 일반적인 한자의 최대 획수
    
    @staticmethod
    def normalize_hanja_data(data: Dict) -> Dict:
        """한자 데이터를 정규화합니다."""
        normalized = data.copy()
        
        # 한자 정규화
        if 'traditional' in normalized:
            normalized['traditional'] = normalized['traditional'].strip()
        
        if 'simplified' in normalized:
            normalized['simplified'] = normalized['simplified'].strip()
        
        # 발음 정규화
        if 'korean_pronunciation' in normalized:
            normalized['korean_pronunciation'] = normalized['korean_pronunciation'].strip()
        
        if 'chinese_pronunciation' in normalized:
            normalized['chinese_pronunciation'] = normalized['chinese_pronunciation'].strip()
        
        # 부수 정규화
        if 'radical' in normalized:
            normalized['radical'] = normalized['radical'].strip()
        
        # 획수 정규화
        if 'stroke_count' in normalized:
            try:
                normalized['stroke_count'] = int(normalized['stroke_count'])
            except (ValueError, TypeError):
                normalized['stroke_count'] = None
        
        # 뜻 정규화
        if 'meaning' in normalized:
            normalized['meaning'] = normalized['meaning'].strip()
        
        # 예문 정규화
        if 'examples' in normalized:
            normalized['examples'] = normalized['examples'].strip()
        
        return normalized
    
    @staticmethod
    def validate_hanja_data(data: Dict) -> List[str]:
        """한자 데이터의 유효성을 검사하고 오류 메시지를 반환합니다."""
        errors = []
        
        # 한자 검증
        if 'traditional' not in data or not data['traditional']:
            errors.append("번체자가 필요합니다.")
        elif not HanjaValidator.is_valid_hanja(data['traditional']):
            errors.append("유효하지 않은 번체자입니다.")
        
        # 간체자 검증
        if 'simplified' in data and data['simplified']:
            if not HanjaValidator.is_valid_hanja(data['simplified']):
                errors.append("유효하지 않은 간체자입니다.")
        
        # 한글 발음 검증
        if 'korean_pronunciation' not in data or not data['korean_pronunciation']:
            errors.append("한글 발음이 필요합니다.")
        elif not HanjaValidator.is_valid_korean_pronunciation(data['korean_pronunciation']):
            errors.append("유효하지 않은 한글 발음입니다.")
        
        # 병음 검증
        if 'chinese_pronunciation' in data and data['chinese_pronunciation']:
            if not HanjaValidator.is_valid_pinyin(data['chinese_pronunciation']):
                errors.append("유효하지 않은 병음입니다.")
        
        # 부수 검증
        if 'radical' not in data or not data['radical']:
            errors.append("부수가 필요합니다.")
        elif not HanjaValidator.is_valid_radical(data['radical']):
            errors.append("유효하지 않은 부수입니다.")
        
        # 획수 검증
        if 'stroke_count' not in data or data['stroke_count'] is None:
            errors.append("획수가 필요합니다.")
        elif not HanjaValidator.is_valid_stroke_count(data['stroke_count']):
            errors.append("유효하지 않은 획수입니다.")
        
        return errors 