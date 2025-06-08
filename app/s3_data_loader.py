import os

class S3DataLoader():
    def __init__(self, s3, bucket):
        self.s3 = s3
        self.bucket = bucket
        
    def download(self, s3_paths, save_dir):
        save_paths = []
        for s3_path in s3_paths:
            save_path = os.path.join(save_dir, os.path.basename(s3_path))
            if os.path.exists(save_path):
                print(f"le fichier {save_path} existe deja")
            else:
                self.s3.download_file(self.bucket, s3_path, save_path)
                print(f"telechargement de {s3_path} vers {save_path}")
            save_paths.append(save_path)
        return save_paths