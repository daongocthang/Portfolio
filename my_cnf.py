import argparse
import os
import secrets
import string

tmpl = r"SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pwd}@{host}/{db}'"
basedir = os.path.dirname(os.path.abspath(__file__))
alphabet = string.ascii_letters + string.digits


def gen_secret_key(num=8):
    return ''.join(secrets.choice(alphabet) for _ in range(num))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', default='root')
    parser.add_argument('-p', '--password', default='')
    parser.add_argument('--host', default='localhost:3306')
    parser.add_argument('--secret-key', default=gen_secret_key(20))
    parser.add_argument('database')

    args = parser.parse_args()

    path = os.path.join(basedir, 'instance')

    # Create directory if not exists
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'config.py'), 'w+') as f:
        f.write("SECRET_KEY = '{}'".format(args.secret_key))
        f.write('\n')
        cnf = tmpl.format(user=args.user, pwd=args.password, host=args.host, db=args.database)
        f.write(cnf)
