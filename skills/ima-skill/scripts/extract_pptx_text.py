#!/usr/bin/env python3
"""
PPTX 文字内容提取器
支持 .pptx 文件，纯标准库实现（zipfile + xml.etree），无需安装任何第三方库

用法：
  python3 extract_pptx_text.py 文件.pptx
  python3 extract_pptx_text.py 文件.pptx --output output.txt
"""

import sys
import zipfile
import xml.etree.ElementTree as ET
import argparse
import re
from pathlib import Path


def extract_text_from_pptx(pptx_path: str) -> dict:
    """提取 PPTX 文件中的所有文字内容"""
    
    slides_content = []
    slide_titles = []
    
    # 命名空间映射
    namespaces = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }
    
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # 获取所有幻灯片文件
        slide_files = sorted([
            name for name in zf.namelist() 
            if re.match(r'ppt/slides/slide\d+\.xml', name)
        ])
        
        for slide_path in slide_files:
            with zf.open(slide_path) as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                # 提取所有文字
                texts = []
                for elem in root.iter():
                    if elem.tag.endswith('}t'):
                        if elem.text and elem.text.strip():
                            texts.append(elem.text.strip())
                
                # 提取标题（第一个加粗大字体的文本）
                title = texts[0] if texts else ""
                slide_titles.append(title)
                
                # 合并所有文字
                combined = ' '.join(texts)
                slides_content.append({
                    'slide_num': len(slides_content) + 1,
                    'title': title,
                    'text': combined,
                    'raw_texts': texts
                })
    
    return {
        'slides': slides_content,
        'total_slides': len(slides_content),
        'slide_titles': slide_titles
    }


def format_output(result: dict, include_raw: bool = False) -> str:
    """格式化输出"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"📊 PPT 内容提取结果（共 {result['total_slides']} 页）")
    lines.append("=" * 60)
    lines.append("")
    
    for slide in result['slides']:
        lines.append(f"{'─' * 40}")
        lines.append(f"📄 第 {slide['slide_num']} 页")
        if slide['title']:
            lines.append(f"   标题：{slide['title']}")
        lines.append("")
        lines.append(slide['text'])
        lines.append("")
        
        if include_raw and slide['raw_texts']:
            lines.append("   [原始文本片段]")
            for i, t in enumerate(slide['raw_texts'], 1):
                lines.append(f"     {i}. {t}")
            lines.append("")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='提取 PPTX 文件中的文字内容')
    parser.add_argument('file', help='PPTX 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径（不指定则输出到终端）')
    parser.add_argument('--raw', '-r', action='store_true', help='显示原始文本片段')
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"❌ 文件不存在：{args.file}")
        sys.exit(1)
    
    if not args.file.lower().endswith('.pptx'):
        print("❌ 请提供 .pptx 文件")
        sys.exit(1)
    
    print(f"🔍 正在解析：{args.file}")
    
    try:
        result = extract_text_from_pptx(args.file)
        output = format_output(result, include_raw=args.raw)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ 已保存到：{args.output}")
        else:
            print(output)
            
    except zipfile.BadZipFile:
        print("❌ 不是有效的 PPTX 文件（损坏或不是 ZIP 格式）")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 解析出错：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
