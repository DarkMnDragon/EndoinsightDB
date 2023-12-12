from configparser import ConfigParser
import argparse
import time
from dbms.postgres import PgDBMS
from hint_recommender.hint_space import HintSpace

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-seed", type=int, default=1)
    args = parser.parse_args()
    print(args.seed)
    print(f'Input arguments: {args}')
    time.sleep(2)
    config = ConfigParser()


    config_path = "./configs/postgres.ini"
    config.read(config_path)
    dbms = PgDBMS.from_file(config)


    hint_space = HintSpace(
        dbms=dbms, 
        sql_path="./sql/1.sql",
        seed = int(args.seed)
    )

    hint_space.optimize(
        name = f"../BO_test", 
        trials_number=30, 
        initial_config_number=10)
