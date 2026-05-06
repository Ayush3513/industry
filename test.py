"""A module to add two numbers provided via command line."""

import argparse


def add_numbers(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


def main() -> None:
    """Prints the sum of two variables passed via command line."""
    parser = argparse.ArgumentParser(description="Add two numbers.")
    parser.add_argument("a", type=int, help="First number")
    parser.add_argument("b", type=int, help="Second number")

    args = parser.parse_args()

    print(add_numbers(args.a, args.b))


if __name__ == "__main__":
    main()
