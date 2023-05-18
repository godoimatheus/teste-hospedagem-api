from pymongo import MongoClient
import pandas as pd
from flask import Flask

# conectar ao mongo
client = MongoClient('localhost', 27017)
db = client['workana']
collection = db['vagas']

# converter para dataframe
cursor = collection.find()
df = pd.DataFrame(list(cursor))

filter = {}
sort = list({
                'consulta': -1
            }.items())

result = client['workana']['vagas'].find_one(
    filter=filter,
    sort=sort
)

df['_id'] = df['_id'].apply(lambda x: str(x))

app = Flask(__name__)


@app.route('/')
def all_jobs():
    df_all_jobs = df.to_dict(orient='records')
    return df_all_jobs


@app.route('/recents')
def recents():
    recent = df.tail(1000).to_dict(orient='records')
    return recent


@app.route('/fixed')
def fixed():
    jobs = df.loc[df['forma_pag'] == 'Fixed']
    return jobs.to_dict(orient='records')


@app.route('/hourly')
def hourly():
    jobs = df.loc[df['forma_pag'] == 'Hourly']
    return jobs.to_dict(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
