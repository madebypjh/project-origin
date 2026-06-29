"""
Project Origin - CLI Entry Point
"""

from project_origin.brand.application import BrandApplication


def main():
    app = BrandApplication()
    app.run()


if __name__ == "__main__":
    main()
