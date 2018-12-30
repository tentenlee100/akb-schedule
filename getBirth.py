from birthday import GetBirthMember
import datetime


if __name__ == '__main__':
    query_date = datetime.datetime.today().strftime("/%m/%d")
    members = GetBirthMember().get_birth_member(query_date)
    print(members)
