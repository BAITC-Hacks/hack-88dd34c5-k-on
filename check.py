"""
Есть дефект или нет.

Правило: если в кадре много красного — DEFECT, иначе OK.

Запуск:
    python check.py defect.png
    python check.py ok.png --threshold 15 --verbose
"""

import argparse
import sys

import numpy as np
from PIL import Image

THRESHOLD = 10.0  # процент красных пикселей, с которого считаем брак


def red_ratio(path: str) -> float:
    """Доля красных пикселей в кадре, в процентах."""
    img = Image.open(path).convert("RGB")
    img.thumbnail((800, 800))  # ускоряет, на результат почти не влияет

    arr = np.asarray(img, dtype=np.int16)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # красный канал заметно преобладает над остальными и пиксель не тёмный
    mask = (r > 90) & (r - g > 40) & (r - b > 40)
    return float(mask.mean() * 100)


def main() -> int:
    parser = argparse.ArgumentParser(description="Брак или норма по одной картинке")
    parser.add_argument("image", help="путь к файлу изображения")
    parser.add_argument("--threshold", type=float, default=THRESHOLD,
                        help=f"порог в процентах (по умолчанию {THRESHOLD})")
    parser.add_argument("--verbose", action="store_true",
                        help="дополнительно показать процент красного")
    args = parser.parse_args()

    try:
        ratio = red_ratio(args.image)
    except FileNotFoundError:
        print(f"Файл не найден: {args.image}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Не удалось открыть изображение: {exc}", file=sys.stderr)
        return 1

    verdict = "DEFECT" if ratio >= args.threshold else "OK"

    if args.verbose:
        print(f"{verdict} (красного {ratio:.1f}%, порог {args.threshold:.1f}%)")
    else:
        print(verdict)

    return 0


if __name__ == "__main__":
    sys.exit(main())