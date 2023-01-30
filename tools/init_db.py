import argparse
import sqlite3
import csv


def init_db(datafile: str):
    connection = sqlite3.connect('../genes.db')

    print('Creating DB')
    with open('schema.sql') as f:
        connection.executescript(f.read())

    connection.commit()

    print('Loading data')
    with open(datafile) as f:
        csv_reader = csv.reader(f)
        # Skip header
        next(csv_reader, None)
        data = [tuple(row) for row in csv_reader]

    cur = connection.cursor()

    print('Inserting data')
    cur.executemany(
        'INSERT INTO genes(chromosome, start, end, strand, protein_name, sequence) VALUES (?, ?, ?, ?, ?, ?)',
        data)

    connection.commit()

    print('Creating indices')
    with open('indices.sql') as f:
        connection.executescript(f.read())

    connection.commit()

    print('Done')
    connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=str, help='CSV file with data to fit into the SQLite DB')
    args = parser.parse_args()
    init_db(args.data)
