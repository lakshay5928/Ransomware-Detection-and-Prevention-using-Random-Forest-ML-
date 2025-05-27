import os
import math

def get_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in set(data):
        p_x = data.count(x) / len(data)
        entropy -= p_x * math.log2(p_x)
    return entropy

def extract_features(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        if not content:
            return None

        size = len(content)
        entropy = get_entropy(content.decode('latin1'))

        txt_ratio = content.count(b'.txt') / size
        exe_ratio = content.count(b'.exe') / size
        encrypted_ratio = content.count(b'encrypted') / size
        locky_ratio = content.count(b'.locky') / size

        return {
            'event_count': 1,
            'unique_file': 1,
            'total_size_change': size,
            'avg_file_size': size,
            'entropy': entropy,
            'txt_ratio': txt_ratio,
            'exe_ratio': exe_ratio,
            'encrypted_ratio': encrypted_ratio,
            'locky_ratio': locky_ratio,
            'created_ratio': 1,
            'modified_ratio': 0,
            'deleted_ratio': 0
        }
    except Exception as e:
        print(f"Feature extraction error: {e}")
        return None
