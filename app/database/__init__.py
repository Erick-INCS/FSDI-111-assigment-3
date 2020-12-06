#!/usr/bin/env python3
# -*- coding: utf8 -*-
""" module """

from flask import g
import sqlite3

DATABASE = "database"
PROPS = ['id', 'name', 'price', 'description', 'category', 'quantity', 'unique_tag', 'active']

def get_db():
    db = getattr(g, "_database", None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def output_formatter(results: tuple):
    out = {"body":[]}
    for result in results:
        res_dict = {}
        for i, p in enumerate(PROPS):
            res_dict[p] = result[i]
        out['body'].append(res_dict)
    return out

def scan(deleted=False):
    global PROPS
    cursor = get_db().execute(f"select {','.join(PROPS)} from product where active = {not deleted}", ())
    result = cursor.fetchall()
    cursor.close()
    return output_formatter(result)

def read(p_id):
    query = f"""
        select {','.join(PROPS)}
        from product
        where id = ? and active = true
    """
    cursor = get_db().execute(query, (p_id,))
    result = cursor.fetchall()
    cursor.close()
    return output_formatter(result)

def update(p_id, fields: dict):
    field_string = ", ".join(
        "%s=\"%s\"" % (key, val)
            for key, val
            in fields.items())
    query = """
            update product
            set %s
            where id = ?
            """ % field_string

    cursor = get_db()
    cursor.execute(query, (p_id,))
    cursor.commit()
    return True

def create(name, price, quantity, unique_tag, description='', category='None', active='true'):
    value_tuple = (name, price, description, category, quantity, unique_tag, active)
    query = """
        INSERT INTO product (
            name, price, description, category, quantity, unique_tag, active)
        VALUES  (?, ?, ?, ?, ?, ?, ?)
    """
    cursor = get_db()
    print(value_tuple)
    last_row_id = cursor.execute(query, value_tuple).lastrowid
    cursor.commit()
    return last_row_id


def delete(p_id):
    query = "update product set active=false where id = ?"
    cursor = get_db()
    cursor.execute(query, (int(p_id),))
    cursor.commit()
    return True

def reactivate(p_id):
    query = "update product set active=true where id = ?"
    cursor = get_db()
    cursor.execute(query, (int(p_id),))
    print(p_id, query)
    cursor.commit()
    return {'ok':True, 'message':'Updated'}
