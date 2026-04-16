# -*- coding: utf-8 -*-
"""
PDF 转 Markdown 脚本
支持提取文本、表格、图片，输出为 Markdown 格式。

用法：
  单个文件:    python pdf_to_markdown.py -i document.pdf
  整个文件夹:  python pdf_to_markdown.py -d ./pdfs
  指定输出目录: python pdf_to_markdown.py -i document.pdf -o ./output
  指定页码范围: python pdf_to_markdown.py -i document.pdf --pages 0-5
  不提取图片:  python pdf_to_markdown.py -i document.pdf --no-images

输出结构:
  output/
  ├── document.md          # Markdown 文件
  └── document_images/     # 提取的图片目录
      ├── page0_img0.png
      ├── page1_img0.png
      └── ...
"""

import argparse
import os
import re
import sys
import pathlib

import pymupdf
import pymupdf4llm


PDF_EXTENSIONS = {'.pdf'}


def parse_page_range(page_str: str, total_pages: int) -> list:
    """
    解析页码范围字符串，支持格式:
      "0-5"   -> [0,1,2,3,4,5]
      "1,3,5" -> [1,3,5]
      "2-"    -> [2, 3, ..., last]
      "-3"    -> [0, 1, 2, 3]
    """
    pages = set()
    for part in page_str.split(','):
        part = part.strip()
        if '-' in part:
            bounds = part.split('-', 1)
            start = int(bounds[0]) if bounds[0].strip() else 0
            end = int(bounds[1]) if bounds[1].strip() else total_pages - 1
            start = max(0, min(start, total_pages - 1))
            end = max(0, min(end, total_pages - 1))
            pages.update(range(start, end + 1))
        else:
            p = int(part)
            if 0 <= p < total_pages:
                pages.add(p)
    return sorted(pages)


def extract_and_save_images(pdf_path: str, output_dir: str, page_numbers: list = None) -> dict:
    """
    从 PDF 提取图片并保存到磁盘。
    返回 {xref: 相对路径} 映射，用于在 Markdown 中替换图片引用。
    """
    doc = pymupdf.open(pdf_path)
    image_map = {}
    os.makedirs(output_dir, exist_ok=True)

    pages_to_process = page_numbers if page_numbers else range(len(doc))

    for page_idx in pages_to_process:
        if page_idx >= len(doc):
            continue
        page = doc[page_idx]
        image_list = page.get_images(full=True)

        for img_idx, img_info in enumerate(image_list):
            xref = img_info[0]
            if xref in image_map:
                continue

            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue

                img_ext = base_image.get("ext", "png")
                img_bytes = base_image["image"]

                filename = f"page{page_idx}_img{img_idx}.{img_ext}"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "wb") as f:
                    f.write(img_bytes)

                image_map[xref] = filename
            except Exception as e:
                print(f"  [警告] 提取图片失败 (page={page_idx}, xref={xref}): {e}")

    doc.close()
    return image_map


def replace_image_refs(md_text: str, images_dir_name: str) -> str:
    """
    将 pymupdf4llm 生成的 base64 内嵌图片替换为本地文件引用。
    匹配模式: ![...](data:image/...;base64,...)
    """
    base64_pattern = re.compile(
        r'!\[([^\]]*)\]\(data:image/[^;]+;base64,[A-Za-z0-9+/=\s]+\)'
    )

    img_counter = [0]

    def _replace(match):
        alt_text = match.group(1) or f"image_{img_counter[0]}"
        ref = f"![{alt_text}]({images_dir_name}/image_{img_counter[0]}.png)"
        img_counter[0] += 1
        return ref

    return base64_pattern.sub(_replace, md_text)


def save_base64_images(md_text: str, output_dir: str) -> str:
    """
    从 Markdown 中提取 base64 图片数据，保存为文件，并替换为本地路径引用。
    """
    import base64 as b64module

    base64_pattern = re.compile(
        r'!\[([^\]]*)\]\(data:image/([^;]+);base64,([A-Za-z0-9+/=\s]+)\)'
    )

    os.makedirs(output_dir, exist_ok=True)
    img_counter = [0]
    images_dir_name = os.path.basename(output_dir)

    def _replace(match):
        alt_text = match.group(1) or f"image_{img_counter[0]}"
        img_ext = match.group(2).split('+')[0]
        img_data = match.group(3).replace('\n', '').replace(' ', '')

        filename = f"image_{img_counter[0]}.{img_ext}"
        filepath = os.path.join(output_dir, filename)

        try:
            with open(filepath, "wb") as f:
                f.write(b64module.b64decode(img_data))
        except Exception as e:
            print(f"  [警告] 保存内嵌图片失败: {e}")

        img_counter[0] += 1
        return f"![{alt_text}]({images_dir_name}/{filename})"

    return base64_pattern.sub(_replace, md_text)


def convert_single_pdf(pdf_path: str, output_dir: str,
                       extract_images: bool = True,
                       page_numbers: list = None) -> str:
    """
    转换单个 PDF 文件为 Markdown。
    返回输出的 .md 文件路径。
    """
    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    md_filename = f"{basename}.md"
    md_filepath = os.path.join(output_dir, md_filename)
    images_dir = os.path.join(output_dir, f"{basename}_images")

    os.makedirs(output_dir, exist_ok=True)

    print(f"  转换中: {pdf_path}")

    kwargs = {
        "write_images": extract_images,
        "image_path": images_dir,
        "show_progress": False,
    }
    if page_numbers is not None:
        kwargs["pages"] = page_numbers

    try:
        md_text = pymupdf4llm.to_markdown(pdf_path, **kwargs)
    except TypeError:
        kwargs.pop("show_progress", None)
        if "image_path" in kwargs:
            kwargs.pop("image_path")
        md_text = pymupdf4llm.to_markdown(pdf_path, **kwargs)

    if extract_images:
        md_text = save_base64_images(md_text, images_dir)

        doc = pymupdf.open(pdf_path)
        pages_to_process = page_numbers if page_numbers else list(range(len(doc)))
        page_count = len(doc)
        doc.close()

        extra_images = extract_and_save_images(pdf_path, images_dir, pages_to_process)
        if extra_images:
            images_dir_name = os.path.basename(images_dir)
            md_text += "\n\n---\n\n## 附录：提取的图片\n\n"
            for xref, filename in extra_images.items():
                md_text += f"![{filename}]({images_dir_name}/{filename})\n\n"

        if os.path.isdir(images_dir) and not os.listdir(images_dir):
            os.rmdir(images_dir)

    pathlib.Path(md_filepath).write_text(md_text, encoding="utf-8")
    return md_filepath


def collect_pdfs_from_dir(directory: str) -> list:
    """收集文件夹下所有 PDF 文件路径，按文件名排序"""
    pdfs = []
    for filename in sorted(os.listdir(directory)):
        ext = os.path.splitext(filename)[1].lower()
        if ext in PDF_EXTENSIONS:
            pdfs.append(os.path.join(directory, filename))
    return pdfs


def main():
    parser = argparse.ArgumentParser(
        description="PDF 转 Markdown 脚本 - 支持表格、图片提取",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -i report.pdf
  %(prog)s -i report.pdf -o ./output --pages 0-5
  %(prog)s -d ./pdfs -o ./markdown_output
  %(prog)s -i report.pdf --no-images
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input', help="单个 PDF 文件路径")
    group.add_argument('-d', '--dir', help="PDF 文件夹路径（批量转换）")

    parser.add_argument('-o', '--output', default=None,
                        help="输出目录 (默认: 与输入文件同目录)")
    parser.add_argument('--pages', default=None,
                        help="页码范围，从0开始 (如: 0-5, 1,3,5, 2-)")
    parser.add_argument('--no-images', action='store_true',
                        help="不提取图片")

    args = parser.parse_args()

    if args.input:
        if not os.path.isfile(args.input):
            print(f"错误: 文件不存在 -> {args.input}")
            sys.exit(1)

        output_dir = args.output or os.path.dirname(os.path.abspath(args.input))

        page_numbers = None
        if args.pages:
            doc = pymupdf.open(args.input)
            page_numbers = parse_page_range(args.pages, len(doc))
            doc.close()
            print(f"指定页码: {page_numbers}")

        md_path = convert_single_pdf(
            args.input, output_dir,
            extract_images=not args.no_images,
            page_numbers=page_numbers,
        )
        print(f"\n完成! Markdown 文件: {md_path}")

    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"错误: 目录不存在 -> {args.dir}")
            sys.exit(1)

        pdfs = collect_pdfs_from_dir(args.dir)
        if not pdfs:
            print(f"错误: 目录中未找到 PDF 文件 -> {args.dir}")
            sys.exit(1)

        output_dir = args.output or args.dir
        print(f"找到 {len(pdfs)} 个 PDF 文件\n")

        success, fail = 0, 0
        for idx, pdf_path in enumerate(pdfs, 1):
            print(f"[{idx}/{len(pdfs)}] {os.path.basename(pdf_path)}")
            try:
                md_path = convert_single_pdf(
                    pdf_path, output_dir,
                    extract_images=not args.no_images,
                )
                print(f"  -> 输出: {md_path}")
                success += 1
            except Exception as e:
                print(f"  -> 失败: {e}")
                fail += 1

        print(f"\n完成! 成功: {success}, 失败: {fail}")


if __name__ == '__main__':
    main()
