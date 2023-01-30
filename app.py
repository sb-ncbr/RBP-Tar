from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def get_data_values():
    connection = sqlite3.connect('genes.db')
    cur = connection.cursor()

    values = {
        'strand': [''],
        'chromosome': [''],
        'protein_name': ['']
    }

    cur.execute('SELECT DISTINCT strand FROM genes')
    values['strand'].extend(x[0] for x in cur.fetchall())

    cur.execute('SELECT DISTINCT chromosome FROM genes')
    values['chromosome'].extend(x[0] for x in cur.fetchall())

    cur.execute('SELECT DISTINCT protein_name FROM genes')
    values['protein_name'].extend(x[0] for x in cur.fetchall())

    for v in values.values():
        v.sort()

    return values


data_values = get_data_values()


@app.route('/get_results')
def get_results():
    parameters = request.args
    connection = sqlite3.connect('genes.db')
    cur = connection.cursor()

    conditions = []
    strand = parameters['strand']
    if strand:
        conditions.append(f'strand = "{strand}"')
    protein_name = parameters['protein_name']
    if protein_name:
        conditions.append(f'protein_name = "{protein_name}"')
    chromosome = parameters['chromosome']
    if chromosome:
        conditions.append(f'chromosome = "{chromosome}"')
    start_min = parameters['start_min']
    start_max = parameters['start_max']
    end_min = parameters['end_min']
    end_max = parameters['end_max']

    if start_min:
        conditions.append(f'start >= {start_min}')
    if start_max:
        conditions.append(f'start <= {start_max}')
    if end_min:
        conditions.append(f'end >= {end_min}')
    if end_max:
        conditions.append(f'end <= {end_max}')

    cond = ' AND '.join(conditions)

    where = 'WHERE' if cond else ''

    sql_statement = f'SELECT * FROM genes {where} {cond} LIMIT 10000'
    cur.execute(sql_statement)

    data = cur.fetchall()
    return jsonify({'data': [list(item) for item in data]})


@app.route('/')
def search():
    return render_template('search.html', values=data_values)


if __name__ == '__main__':
    app.run()
