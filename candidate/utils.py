import hashlib
import os

def generate_file_path(instance, filename):
    """
    Return a unique filename using SHA-256 for better security.
    """

    hash_object = hashlib.sha256(filename.encode())
    hash_filename = hash_object.hexdigest()
    extension = os.path.splitext(filename)[1]

    return f"candidates_photos/{hash_filename}{extension}"