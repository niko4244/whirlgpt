from pdf2image import convert_from_path
import os

def pdf_to_png(pdf_path, output_dir, dpi=300):
    """
    Convert each page of a PDF to a separate PNG image.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the PNG images.
        dpi (int): Resolution in dots per inch.

    Returns:
        List[str]: List of saved PNG image paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi)
    image_paths = []

    for i, page in enumerate(pages):
        image_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{i+1}.png")
        page.save(image_path, "PNG")
        image_paths.append(image_path)

    return image_paths

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert PDF to PNG images")
    parser.add_argument("pdf_path", type=str, help="Path to input PDF file")
    parser.add_argument("output_dir", type=str, help="Directory to save output PNGs")
    parser.add_argument("--dpi", type=int, default=300, help="Resolution in DPI")
    args = parser.parse_args()

    converted_images = pdf_to_png(args.pdf_path, args.output_dir, args.dpi)
    print(f"Converted {len(converted_images)} pages to PNG images:")
    for img_path in converted_images:
        print(f" - {img_path}")
