import xml.etree.ElementTree as ET
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def check_xml_structure():
    data_dir = Path('data/raw')
    xml_files = list(data_dir.glob('*.xml'))
    
    if not xml_files:
        print("XML 파일을 찾을 수 없습니다.")
        return
        
    print(f"\n총 XML 파일 수: {len(xml_files)}")
    
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # 루트 태그 확인
            print(f"\n파일: {xml_file.name}")
            print(f"루트 태그: {root.tag}")
            
            # 전체 항목 수 확인
            items = root.findall('.//item')
            print(f"전체 항목 수: {len(items)}")
            
            # 첫 번째 항목의 자세한 구조 확인
            if items:
                first_item = items[0]
                print("\n첫 번째 항목의 상세 구조:")
                
                # target_code 확인
                target_code = first_item.find('target_code')
                if target_code is not None:
                    print(f"대상 코드: {target_code.text}")
                
                # word_info 확인
                word_info = first_item.find('word_info')
                if word_info is not None:
                    print("\nword_info 태그의 모든 자식 태그:")
                    for child in word_info:
                        print(f"태그: {child.tag}")
                        print(f"값: {child.text}")
                        print("---")
            
        except Exception as e:
            print(f"{xml_file.name} 처리 중 오류 발생: {str(e)}")

if __name__ == '__main__':
    check_xml_structure() 