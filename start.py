"""
Main function
"""

from schedule import (
    Akb, Team8, Ske, Nmb, Hkt, Ngt, Stu
)


def run():
    group = [
        Akb, Team8, Ske, Nmb, Hkt, Ngt, Stu
    ]

    test_date = "2018/10/20"
    for g in group:
        result = g(test_date).get_schedule()
        print(result)
        print("-" * 20)


if __name__ == "__main__":
    run()
