import xml.etree.ElementTree as ET
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def check_xml_structure():
    xml_file = Path('data/raw/1435291_5000.xml')
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # 루트 태그 확인
        print(f"\n루트 태그: {root.tag}")
        
        # 첫 번째 항목의 자세한 구조 확인
        first_item = root.find('.//item')
        if first_item is not None:
            print("\n첫 번째 항목의 상세 구조:")
            word_info = first_item.find('word_info')
            if word_info is not None:
                print("\nword_info 태그의 모든 자식 태그:")
                for child in word_info:
                    print(f"태그: {child.tag}")
                    print(f"값: {child.text}")
                    print("---")
                
                # 의미 정보 확인
                print("\n의미 정보 태그:")
                sense_info = word_info.find('sense_info')
                if sense_info is not None:
                    for child in sense_info:
                        print(f"태그: {child.tag}")
                        print(f"값: {child.text}")
                        print("---")
            
            # 단어 정보 요약
            target_code = first_item.find('target_code').text if first_item.find('target_code') is not None else 'N/A'
            word = word_info.find('word').text if word_info.find('word') is not None else 'N/A'
            print(f"\n단어 정보 요약:")
            print(f"대상 코드: {target_code}")
            print(f"단어: {word}")
        
        # 전체 항목 수 확인
        items = root.findall('.//item')
        print(f"\n전체 항목 수: {len(items)}")
        
        # 실제 단어 수 확인
        words = root.findall('.//word_info/word')
        print(f"실제 단어 수: {len(words)}")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == '__main__':
    check_xml_structure() 