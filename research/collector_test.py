from research.collector import BrandCollector


def main():
    print("Categories:")
    print(BrandCollector.get_categories())

    print("\nCybersecurity Brands:")
    print(BrandCollector.get_brands("cybersecurity"))

    print("\nTotal Brands:")
    print(len(BrandCollector.get_all_brands()))


if __name__ == "__main__":
    main()