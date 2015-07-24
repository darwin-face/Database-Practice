import json, os, sqlite3
from pprint import pprint
from collections import namedtuple

'''
		try catch to create the database
			create constituents table
		 	create meeting table
		try catch with importing the json file
		try to read chunk by chunk
		create the respective object arrays
		import constituents as objects
		import meetings as objects
		run through meeting array
			if(!mtg.getStatus.equalsIgnoreCase("confirmed"))
				continue
			else put it in the database
'''

conn = sqlite3.connect('example.db')
c = conn.cursor()

#create tables
c.execute("CREATE TABLE constituents (district text, email text, firstName text, ident int, lastName text, mtgID int[])")

c.execute("CREATE TABLE meeting	(adrLine1 text, adrLine2 text, congressPersonId int, congressPersonDistrict text, constituentIds int[], end text, ident int, location text, name text, phoneNo text, status text, start text)")

#import data
with open('advocacy_day.json') as data_file:
	data = json.load(data_file)

#create a tuple list of constituents, and put in the database
constituents = []
for e in data[u'Constituents']:
	constituents.append(namedtuple('constituent', e.keys())(*e.values()))

	district = e[u'District']
	email = e[u'Email']
	firstName = e[u'FirstName']
	ident = e[u'Id']
	lastName = e[u'LastName']
	mtgID = e[u'MeetingIds']
	c.execute("insert into constituents values (?,?,?,?,?,?)", (district, email, firstName, ident, lastName, str(mtgID)))

#create a tuple list of meetings, if it is a Confirmed meeting
#put it in the database
meetings = []
for m in data[u'Meetings']:
	if(m[u'Status'] == "Confirmed"):
		meetings.append(namedtuple('meeting', m.keys())(*m.values()))

		adrLine1 = m[u'AddressLine1']
		adrLine2 = m[u'AddressLine2']
		congressPersonId = m[u'CongressPersonID']
		congressPersonDistrict = m[u'CongressPersonStateDistrict']
		constituentIds = m[u'ConstituentIds']
		end = m[u'End']
		ident = m[u'Id']
		location = m[u'Location']
		name = m[u'Name']
		phoneNo = m[u'PhoneNumber']
		start = m[u'Start']
		status = m[u'Status']

		c.execute("insert into meeting values (?,?,?,?,?,?,?,?,?,?,?,?)", (adrLine1, adrLine2, congressPersonId, congressPersonDistrict, str(constituentIds), end, ident, location, name, phoneNo, status, start))

#print the sql above code
with open('dump.sql', 'w') as c:
    for line in conn.iterdump():
        c.write('%s\n' % line)

conn.commit()
conn.close()