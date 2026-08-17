from pathlib import Path

from src.ocr import (
    download_image,
    extract_text_from_image
)


IMAGE_URL = (
    "https://cdn.grofers.com/da/cms-assets/cms/product/"
    "3c63ccbb-6f20-444c-808b-311bcf06cfd9.jpg"
)


output_dir = Path(
    "output",
    "ocr_test"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)


image_path = (
    output_dir /
    "product.jpg"
)


print("Downloading product image...")

download_image(
    IMAGE_URL,
    image_path
)

print(
    f"Image downloaded: {image_path}"
)


print("\nRunning OCR...")

text = extract_text_from_image(
    image_path
)


print("\n" + "=" * 70)
print("OCR RESULT")
print("=" * 70)

print(text)


ocr_file = (
    output_dir /
    "ocr_result.txt"
)

ocr_file.write_text(
    text,
    encoding="utf-8"
)


print("\nOCR saved to:")
print(ocr_file)