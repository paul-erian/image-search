from clip import search_images

if __name__ == "__main__":
    query = "a thing that launch water everywhere"
    results = search_images(query)
    for path, score in results:
        print(f"{path}:{score}")
