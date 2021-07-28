# -*- coding: utf-8 -*-
import sqlite3


class HistoryDatabase:

	insertSync = """INSERT INTO syncs(
								startTime,
								finishTime,
								size,
								user
							)
							VALUES (
								:startTime,
								:finishTime,
								:size,
								:user
							)"""

	insertTransaction = """INSERT INTO transactions(
								elementId,
								transactions,
								syncId
							)
							VALUES (
								:elementId,
								:transactions,
								:syncId
							)"""

	createSyncs = """CREATE TABLE IF NOT EXISTS syncs(
								syncId integer PRIMARY KEY AUTOINCREMENT,
								startTime text,
								finishTime text,
								size real,
								user text
							)"""

	createTransactions = """CREATE TABLE IF NOT EXISTS transactions(
								elementId integer,
								transactions text,
								syncId integer
							)"""

	pragmaJournal = "PRAGMA journal_mode=OFF"

	pragmaFK = "PRAGMA foreign_keys = ON"

	syncLimit = 1750

	def __init__(self, db):
		self.db = db
		conn = sqlite3.connect(self.db)
		conn.execute(self.pragmaJournal)
		conn.execute(self.pragmaFK)
		conn.execute(self.createSyncs)
		conn.execute(self.createTransactions)
		# Index elements.
		conn.execute("CREATE INDEX IF NOT EXISTS elementIndex ON transactions(elementId)")
		# Limit rows.
		conn.execute(
		    "DELETE FROM syncs WHERE syncId < ((SELECT MAX(syncId) FROM syncs) - {})".
		    format(str(self.syncLimit))
		)
		conn.execute(
		    "DELETE FROM transactions WHERE syncId < ((SELECT MAX(syncId) FROM transactions) - {})"
		    .format(str(self.syncLimit))
		)
		conn.commit()
		conn.close()

	def sync(self, row):
		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()
		cursor.execute(self.pragmaJournal)
		cursor.execute(self.insertSync, row)
		rowId = cursor.lastrowid
		cursor.close()
		conn.commit()
		conn.close()
		return rowId

	def transactions(self, data, syncId):
		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()
		cursor.execute(self.pragmaJournal)
		cursor.execute('SELECT syncId FROM syncs WHERE syncId = :id', {'id': syncId})
		result = cursor.fetchall()
		syncRowId = result[0][0]

		for row in data:
			row['syncId'] = syncRowId
			cursor.execute(self.insertTransaction, row)

		cursor.close()
		conn.commit()
		conn.close()
