import os
import random
import string
from sqlalchemy import create_engine, MetaData, Table, select, null


DATABASE_URI = os.getenv("DATABASE_URI")

engine = create_engine(DATABASE_URI)

metadata = MetaData()

# metadata.reflect(bind=engine)
# print(metadata.tables.keys())


def fetch_one_asc(table):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).filter_by(organization_id=7).order_by(
        table1.c.created_at.asc()
        ).limit(1)
    with engine.connect() as conn:
        result = conn.execute(query)
        first = result.fetchone()

    if first:
        return dict(first._mapping)
    else:
        return None


def fetch_one_move(table, location):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).where(
                    table1.c.organization_id == 7,
                    table1.c.location_id != location,
                    table1.c.updated_at != null()
                ).order_by(
        table1.c.created_at.asc()
        ).limit(1)
    with engine.connect() as conn:
        result = conn.execute(query)
        first = result.fetchone()

    if first:
        return dict(first._mapping)
    else:
        return None


def fetch_one(table):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).filter_by(organization_id=7).order_by(
        table1.c.created_at.desc()
        ).limit(1)
    with engine.connect() as conn:
        result = conn.execute(query)
        first = result.fetchone()

    if first:
        return dict(first._mapping)
    else:
        return None


def fetch_one_org(table):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).order_by(
        table1.c.created_at.desc()
        ).limit(1)
    with engine.connect() as conn:
        result = conn.execute(query)
        first = result.fetchone()

    if first:
        return dict(first._mapping)
    else:
        return None    
    

def fetch_one_stack(table):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).filter_by(
        org_id=7, status="OPEN"
        ).order_by(
        table1.c.created_at.desc()
        ).limit(1)
    with engine.connect() as conn:
        result = conn.execute(query)
        first = result.fetchone()

    if first:
        return dict(first._mapping)
    else:
        return None 


def fetch_many_lp(table):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).filter_by(organization_id=7).limit(5)
    with engine.connect() as conn:
        result = conn.execute(query)
        fetchmany = result.fetchmany()

    if fetchmany:
        return [dict(i._mapping)['lp_id'] for i in fetchmany]
    else:
        return None


def fetch_all(table):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).filter_by(organization_id=7).order_by(
        table1.c.created_at.desc()
        )
    with engine.connect() as conn:
        result = conn.execute(query)
        rows = result.fetchall()

    if rows:
        return [dict(row._mapping) for row in rows]
    else:
        return None


def fetch_many_sl(table):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).filter_by(organization_id=7).limit(5)
    with engine.connect() as conn:
        result = conn.execute(query)
        fetchall = result.fetchall()

    if fetchall:
        return [i['lp_id'] for i in dict(fetchall._mapping)]
    else:
        return None
   

def fetch_stack_lp(table, product_id, location_id):
    table1 = Table(table, metadata, autoload_with=engine)
    query = select(table1).filter_by(
        organization_id=7, product_id=product_id, location_id=location_id
        )
    with engine.connect() as conn:
        result = conn.execute(query)
        fetchmany = result.fetchmany()

    if fetchmany:
        return [i['id'] for i in dict(fetchmany._mapping)]
    else:
        return None


def generate_text(length=10):
    return ''.join(random.choices(
        string.ascii_letters, k=length
        ))


def generate_digit(length=6):
    return ''.join(random.choices(
        string.digits, k=length
        ))


def generate_lp_id(qty):
    length = 25
    if qty > 1:
        lps = [''.join(
            random.choices(string.ascii_letters + string.digits, k=length)
            ) for i in range(qty)]
        return lps
    else:
        return ''.join(random.choices(
            string.ascii_letters + string.digits, k=length
            ))