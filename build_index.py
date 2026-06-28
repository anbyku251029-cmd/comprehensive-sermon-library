"""
build_index.py - 설교 인덱스 빌더

Volume 디렉토리에서 _ko_free.md 파일을 스캔하고,
메타데이터를 파싱하여 index.json을 생성하고,
MD 파일을 sermons/spurgeon/ 디렉토리로 복사합니다.

사용법:
    python build_index.py
"""

import os
import sys
import json
import shutil
import glob
from datetime import datetime

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import parse_sermon_md, get_sermon_no_from_filename


def find_source_volumes(base_dir):
    """Volume_XX_XXXX_XXXX 디렉토리 목록을 찾습니다."""
    volumes = []
    for item in os.listdir(base_dir):
        if item.startswith("Volume_") and os.path.isdir(os.path.join(base_dir, item)):
            volumes.append(os.path.join(base_dir, item))
    return sorted(volumes)


def find_md_files(volume_dirs):
    """Volume 디렉토리에서 _ko_free.md 파일을 찾습니다."""
    md_files = []
    for vol_dir in volume_dirs:
        pattern = os.path.join(vol_dir, "*_ko_free.md")
        files = glob.glob(pattern)
        md_files.extend(files)
    
    # _ko.md 파일도 포함 (고품질 번역)
    for vol_dir in volume_dirs:
        pattern = os.path.join(vol_dir, "*_ko.md")
        for f in glob.glob(pattern):
            # _ko_free.md 가 이미 있으면 스킵
            free_version = f.replace("_ko.md", "_ko_free.md")
            if free_version not in md_files:
                md_files.append(f)
    
    return sorted(md_files, key=lambda x: get_sermon_no_from_filename(os.path.basename(x)) or 0)


def build_index(source_base_dir, project_dir):
    """
    인덱스를 빌드합니다.
    
    Args:
        source_base_dir: Volume 디렉토리가 있는 상위 폴더
        project_dir: sermon-library 프로젝트 폴더
    """
    sermons_dir = os.path.join(project_dir, "sermons", "spurgeon")
    os.makedirs(sermons_dir, exist_ok=True)
    
    print("=" * 60)
    print("📖 한글 설교 도서관 - 인덱스 빌더")
    print("=" * 60)
    
    # 1. Volume 디렉토리 탐색
    print("\n[1/4] Volume 디렉토리 탐색 중...")
    volume_dirs = find_source_volumes(source_base_dir)
    print(f"  → {len(volume_dirs)}개 Volume 디렉토리 발견")
    
    # 2. MD 파일 탐색
    print("\n[2/4] 마크다운 파일 탐색 중...")
    md_files = find_md_files(volume_dirs)
    print(f"  → {len(md_files)}개 설교 파일 발견")
    
    # 3. 파싱 및 복사
    print("\n[3/4] 설교 파싱 및 복사 중...")
    sermons = []
    errors = []
    
    for i, filepath in enumerate(md_files):
        filename = os.path.basename(filepath)
        
        # 진행 상황 표시
        if (i + 1) % 100 == 0 or i == 0:
            print(f"  → 진행: {i + 1}/{len(md_files)} ({filename})")
        
        try:
            # 메타데이터 파싱
            metadata = parse_sermon_md(filepath)
            
            # 파일 이름 통일 (chs{N}_ko_free.md)
            sermon_no = metadata.get("sermon_no")
            if sermon_no:
                target_filename = f"chs{sermon_no}_ko_free.md"
            else:
                target_filename = filename
            
            metadata["file_name"] = target_filename
            
            # 파일 복사
            target_path = os.path.join(sermons_dir, target_filename)
            if not os.path.exists(target_path) or os.path.getmtime(filepath) > os.path.getmtime(target_path):
                shutil.copy2(filepath, target_path)
            
            sermons.append(metadata)
            
        except Exception as e:
            errors.append((filename, str(e)))
            print(f"  ⚠️  에러: {filename} - {e}")
    
    # 설교 번호 순 정렬
    sermons.sort(key=lambda s: s.get("sermon_no") or 0)
    
    # 중복 제거 (같은 sermon_no)
    seen = set()
    unique_sermons = []
    for s in sermons:
        sno = s.get("sermon_no")
        if sno and sno in seen:
            continue
        if sno:
            seen.add(sno)
        unique_sermons.append(s)
    sermons = unique_sermons
    
    # 4. index.json 생성
    print("\n[4/4] index.json 생성 중...")
    
    # 볼륨별 통계
    volume_stats = {}
    for s in sermons:
        v = s.get("volume", 0)
        volume_stats[v] = volume_stats.get(v, 0) + 1
    
    index_data = {
        "metadata": {
            "total_sermons": len(sermons),
            "pastors": [
                {
                    "id": "spurgeon",
                    "name_ko": "C. H. 스펄전",
                    "name_en": "C. H. Spurgeon",
                    "full_name": "C. H. 스펄전 (C. H. Spurgeon)",
                    "sermon_count": len(sermons),
                    "description": "영국의 '설교 왕자'로 불리는 침례교 목사 (1834-1892)"
                }
            ],
            "volumes": len(volume_stats),
            "volume_stats": volume_stats,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
        },
        "sermons": sermons,
    }
    
    index_path = os.path.join(project_dir, "sermons", "index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("✅ 인덱스 빌드 완료!")
    print(f"  • 총 설교 수: {len(sermons)}")
    print(f"  • 볼륨 수: {len(volume_stats)}")
    print(f"  • 에러 수: {len(errors)}")
    print(f"  • 인덱스 파일: {index_path}")
    print(f"  • 설교 디렉토리: {sermons_dir}")
    
    if errors:
        print(f"\n⚠️  에러가 발생한 파일 ({len(errors)}개):")
        for fname, err in errors[:10]:
            print(f"    - {fname}: {err}")
        if len(errors) > 10:
            print(f"    ... 외 {len(errors) - 10}개")
    
    print("=" * 60)
    return index_data


if __name__ == "__main__":
    # 프로젝트 디렉토리 (이 스크립트가 있는 곳)
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Volume 디렉토리가 있는 상위 폴더
    source_base_dir = os.path.dirname(project_dir)
    
    print(f"소스 디렉토리: {source_base_dir}")
    print(f"프로젝트 디렉토리: {project_dir}")
    
    build_index(source_base_dir, project_dir)
