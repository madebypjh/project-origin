"""
Project Origin - CLI Entry Point
"""

from .application import ProjectOriginApplication


def main():
    app = ProjectOriginApplication()
    app.run()


if __name__ == "__main__":
    main()