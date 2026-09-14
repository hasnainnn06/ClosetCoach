import json
import pickle
from pathlib import Path
import shutil


class UserWardrobeManager:
    """
    Handles persistent storage of a user's wardrobe.
    Phase-1: single local user.
    """

    def __init__(self, base_dir="data/user_wardrobes", user_id="default_user"):
        self.base_dir = Path(base_dir)
        self.user_id = user_id
        self.user_dir = self.base_dir / self.user_id

        self.images_dir = self.user_dir / "images"
        self.metadata_path = self.user_dir / "metadata.json"
        self.embedding_index_path = self.user_dir / "embedding_index.pkl"

        self._ensure_directories()
        self._ensure_files()

    def _ensure_directories(self):
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_files(self):
        if not self.metadata_path.exists():
            self._save_metadata({})
        if not self.embedding_index_path.exists():
            self._save_embedding_index({})

    # ---------- Metadata ----------
    def _load_metadata(self):
        with open(self.metadata_path, "r") as f:
            return json.load(f)

    def _save_metadata(self, data):
        with open(self.metadata_path, "w") as f:
            json.dump(data, f, indent=2)

    # ---------- Embeddings ----------
    def _load_embedding_index(self):
        with open(self.embedding_index_path, "rb") as f:
            return pickle.load(f)

    def _save_embedding_index(self, data):
        with open(self.embedding_index_path, "wb") as f:
            pickle.dump(data, f)

    # ---------- Public API ----------
    def add_item(self, source_image_path, item_name, category, colors, embedding):
        """
        Persist a user clothing item.
        """

        # 1️⃣ Save image
        dest_path = self.images_dir / item_name
        shutil.copy(source_image_path, dest_path)

        # 2️⃣ Update metadata
        metadata = self._load_metadata()
        metadata[item_name] = {
            "category": category,
            "colors": colors.tolist() if hasattr(colors, "tolist") else colors
        }
        self._save_metadata(metadata)

        # 3️⃣ Update embedding index
        index = self._load_embedding_index()
        index[item_name] = embedding
        self._save_embedding_index(index)

    def load_wardrobe(self):
        return {
            "metadata": self._load_metadata(),
            "embeddings": self._load_embedding_index()
        }
