from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)


def get_data_values():
    def chromosome_key(chromosome: str) -> int:
        chrtype = chromosome[3:]
        match chrtype:
            case 'X':
                return 98
            case 'Y':
                return 89
            case _:
                return int(chrtype)


    with sqlite3.connect('genes.db') as connection:
        cur = connection.cursor()

        values = {}

        cur.execute('SELECT DISTINCT strand FROM genes')
        values['strand'] = [x[0] for x in cur.fetchall()]

        cur.execute('SELECT DISTINCT chromosome FROM genes')
        values['chromosome'] = [x[0] for x in cur.fetchall()]

        cur.execute('SELECT DISTINCT protein_name FROM genes')
        values['protein_name'] = [x[0] for x in cur.fetchall()]

    values['strand'].sort()
    values['protein_name'].sort()
    values['chromosome'].sort(key=chromosome_key)

    values['strand'].insert(0, '')
    values['protein_name'].insert(0, '')
    values['chromosome'].insert(0, '')

    return values


data_values = get_data_values()


@app.route('/get_results')
def get_results():
    strand = request.args['strand']
    protein_name = request.args['protein_name']
    chromosome = request.args['chromosome']
    start_min = request.args['start_min']
    start_max = request.args['start_max']
    end_min = request.args['end_min']
    end_max = request.args['end_max']
    pvalue_min = request.args['pvalue_min']
    pvalue_max = request.args['pvalue_max']

    conditions = []
    params = []

    if strand:
        conditions.append('strand = ?')
        params.append(strand)

    if protein_name:
        conditions.append('protein_name = ?')
        params.append(protein_name)

    if chromosome:
        conditions.append('chromosome = ?')
        params.append(chromosome)

    if start_min:
        conditions.append('start >= ?')
        params.append(start_min)

    if start_max:
        conditions.append('start <= ?')
        params.append(start_max)

    if end_min:
        conditions.append('end >= ?')
        params.append(end_min)

    if end_max:
        conditions.append('end <= ?')
        params.append(end_max)

    if pvalue_min:
        conditions.append('pValue >= ?')
        params.append(pvalue_min)

    if pvalue_max:
        conditions.append('pValue <= ?')
        params.append(pvalue_max)

    cond = ' AND '.join(conditions)
    where = 'WHERE' if cond else ''
    sql_statement = f'SELECT * FROM genes {where} {cond} LIMIT 10000'

    with sqlite3.connect('genes.db') as connection:
        cur = connection.cursor()
        cur.execute(sql_statement, params)
        data = cur.fetchall()
        return jsonify({'data': [list(item) for item in data]})


@app.route('/')
def search():
    return render_template('search.html', values=data_values)


@app.route('/download_all')
def download_all():
    return send_from_directory('static', 'rbp_encode_eclip.csv.gz', as_attachment=True)


if __name__ == '__main__':
    app.run()
