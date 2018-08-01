# import sqlite3
# from kerberusIO.application import app
# from kerberusIO.utils.db.connection import get_db
# from typing import Union
#
# with app.app_context():
#     conn = get_db()
#
#
# def get_result_set(query: str, args: Union[tuple, str]=None):
#     """ executes a query with a return value """
#     with conn.cursor() as cur:
#         if args:
#             if isinstance(args, str):
#                 args = args,
#             try:
#                 cur.execute(query, args)
#                 rs = cur.fetchall()
#                 conn.commit()
#                 return rs
#             except sqlite3.Error as err:
#                 conn.rollback()
#                 print(err)
#         else:
#             try:
#                 cur.execute(query)
#                 rs = cur.fetchall()
#                 conn.commit()
#                 return rs
#             except sqlite3.Error as err:
#                 conn.rollback()
#                 print(err)
#
#
# def execute_query(query: str, args: Union[tuple, str]=None):
#     """ executes a query with no return value """
#     if 'RETURNING' in query:
#         returning = True
#     else:
#         returning = False
#
#     with conn.cursor() as cur:
#         if args:
#             if isinstance(args, str):
#                 args = args,
#             try:
#                 cur.execute(query, args)
#                 conn.commit()
#                 if returning:
#                     return cur.fetchone()[0]
#             except sqlite3.Error as err:
#                 conn.rollback()
#                 print("err in ex_qr")
#                 print(err)
#                 raise err
#         else:
#             try:
#                 cur.execute(query)
#                 conn.commit()
#                 if returning:
#                     return cur.fetchone()[0]
#             except sqlite3.Error as err:
#                 conn.rollback()
#                 print("err in ex_qr")
#                 print(err)
