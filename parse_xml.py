import os
import xml.etree.ElementTree as ET
from pathlib import Path

def analyze_xml_structure(xml_file):
    try:
        # XML 파일 파싱
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        print(f"\n파일: {xml_file}")
        print(f"루트 요소: {root.tag}")
        
        # 첫 번째 item 요소만 자세히 분석
        for item in root.findall('item')[:1]:  # 첫 번째 item만 분석
            print("\n=== 항목 상세 분석 ===")
            
            # target_code 출력
            target_code = item.find('target_code')
            if target_code is not None and target_code.text:
                print(f"target_code: {target_code.text}")
            
            # word_info 분석
            word_info = item.find('word_info')
            if word_info is not None:
                print("\nword_info 내용:")
                for element in word_info:
                    print(f"\n- {element.tag}:")
                    if element.text and element.text.strip():
                        print(f"  {element.text[:200]}")
                    # 하위 요소가 있는 경우
                    for subelement in element:
                        print(f"  * {subelement.tag}:")
                        if subelement.text and subelement.text.strip():
                            print(f"    {subelement.text[:200]}")
    
    except Exception as e:
        print(f"파일 {xml_file} 파싱 중 오류 발생: {str(e)}")

def main():
    # raw 폴더의 XML 파일들 찾기
    raw_dir = Path("data/raw")
    xml_files = list(raw_dir.glob("*.xml"))
    
    if not xml_files:
        print("XML 파일을 찾을 수 없습니다.")
        return
    
    # 첫 번째 XML 파일 분석
    analyze_xml_structure(xml_files[0])

if __name__ == "__main__":
    main() 