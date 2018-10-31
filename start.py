"""
Main function
"""
import argparse
from datetime import datetime

from schedule import (
    Akb, Team8, Ske, Nmb, Hkt, Ngt, Stu
)


def main(query_date, group_name):
    group_class = (Akb, Team8, Ske, Nmb, Hkt, Ngt, Stu)

    group_name = group_name.lower()
    if group_name in ['all', '']:
        for g in group_class:
            result = g(query_date).get_schedule()
            print(g.__name__)
            print(result)
            print("-" * 20)
    elif group_name in ['akb', 'akb48']:
        result = Akb(query_date).get_schedule()
        print(result)
    elif group_name in ['team8', 't8']:
        result = Team8(query_date).get_schedule()
        print(result)
    elif group_name in ['ske', 'ske48']:
        result = Ske(query_date).get_schedule()
        print(result)
    elif group_name in ['nmb', 'nmb48']:
        result = Nmb(query_date).get_schedule()
        print(result)
    elif group_name in ['hkt', 'hkt48']:
        result = Hkt(query_date).get_schedule()
        print(result)
    elif group_name in ['ngt', 'ngt48']:
        result = Ngt(query_date).get_schedule()
        print(result)
    elif group_name in ['stu', 'stu48']:
        result = Stu(query_date).get_schedule()
        print(result)
    else:
        print('Please check group name string.')

    print(f"Your query is: {query_date}, {group_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The AKB48 group schedule script.')

    parser.add_argument('name', type=str, nargs='?', default='all',
                        help='Group name: ex. team8')
    parser.add_argument('query_date', type=str, nargs='?',
                        default=datetime.today().strftime("%Y/%m/%d"),
                        help='ex. 2018/10/30')

    args = parser.parse_args()
    main(query_date=args.query_date, group_name=args.name)
