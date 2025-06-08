from app.clip_utils import search_images, dowload_images_from_r2

if __name__ == "__main__":
    query = "a photo of a boat"
    results = search_images(query, 10, 0.0)
    image_paths_cloud = [path for path, _ in results]
    dowload_images_from_r2(image_paths_cloud)
    for path, score in results:
        print(f"{path}:{score}")