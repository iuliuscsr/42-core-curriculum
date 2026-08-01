#!/usr/bin/env python3
import sys


def store_scores() -> list[int]:
    """Stores scores in a list."""

    scores: list[int] = []
    for argc in sys.argv[1:]:
        try:
            score: list[int] = [int(argc)]
            scores = scores + score
        except ValueError:
            print(f"Invalid parameter: '{argc}'")
    return scores


def display_statistics(scores: list[int]) -> None:
    """Displays statistics within the list"""
    if len(scores) == 0:
        print("No scores provided. Usage: python3"
              " ft_score_analytics.py <score1> <score2> ...")
    else:
        print(f"Scores processed: {scores}")
        print(f"Total players: {len(scores)}")
        print(f"Total score: {sum(scores)}")
        print(f"Average score: {sum(scores) / len(scores):.1f}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}\n")


def main() -> None:
    """Checks user input and shows statistics"""
    print("=== Player Score Analytics ===")
    display_statistics(store_scores())


if __name__ == "__main__":
    main()
