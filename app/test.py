from clip import search_images

if __name__ == "__main__":
    query = "a photo of a dog"
    results = search_images(query, 10, 0.0)
    for path, score in results:
        print(f"{path}:{score}")
