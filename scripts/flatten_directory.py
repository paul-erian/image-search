import argparse
import shutil
from pathlib import Path

from tqdm import tqdm


def flatten_dataset(input_dir, output_dir):
    """Copie tous les fichiers d'une arborescence dans un répertoire unique."""   
    # Chemins
    output_dir.mkdir(parents=True, exist_ok=True)
    image_paths = [p for p in input_dir.rglob("*") if p.is_file()]

    # Copie des fichiers
    for image_path in tqdm(image_paths, desc="Flattening dataset"):
        output_path = output_dir / image_path.name
        shutil.copy2(image_path, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aplatir l'arborescence d'un dataset d'images")
    parser.add_argument('--input-dir', type=Path, required=True, help='Répertoire source')
    parser.add_argument('--output-dir', type=Path, required=True, help='Répertoire de destination')
    args = parser.parse_args()

    flatten_dataset(args.input_dir, args.output_dir)
