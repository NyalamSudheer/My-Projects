#from dbconfig import *
import pymysql
import cgi
import cgitb
cgitb.enable()

#	Establish a cursor for MySQL connection.
'''
db = get_mysql_param()
cnx = pymysql.connect(user=db['user'], 
                      password=db['password'],
                      host=db['host'],
                      # port needed only if it is not the default number, 3306.
                      port = int(db['port']), 
                      database=db['database'])
'''
cnx = pymysql.connect(user='munisifb', 
                      password='Sce1927351!!',
                      host='localhost',
                      # port needed only if it is not the default number, 3306.
                      port = 3306, 
                      database='SWIM')                             
cursor = cnx.cursor()

#	Create HTTP response header
print("Content-Type: text/html;charset=utf-8")
print()

#	Create a primitive HTML starter
print ('''<html>
<head></head>
<body>
''')

#	Get HTTP parameter, swimmer_id (swimmer id)
form = cgi.FieldStorage()
swimmer_id = form.getfirst('swimmer_id')
event_id = form.getfirst('event_id')

if swimmer_id is None and event_id is None:
    #	No HTTP parameter: show all meets
    print('<h2>Please select from following meets:</h2>')
    #All meets
    query = '''
SELECT mi.meetid,mi.title AS title,vn.name AS name,vn.address AS address
FROM meet mi, venue vn
WHERE mi.venueid=vn.venueid;
'''
    cursor.execute(query)
    for (swimmer_id, title, name, address) in cursor:
        print('<ul>')
        print(" <li><a href=?swimmer_id=" + str(swimmer_id) +">"+"("+str(swimmer_id)+")" +title+ "</a>:"+ " at " +name 
        +" (adresses:"+str(address)+")"+'</li>')         
        print('</ul>') 
    print('</body></html>')
    cursor.close()
    cnx.close()		
    quit() 
   
   
form = cgi.FieldStorage()
event_id = form.getfirst('event_id')
if event_id is None:	
    #	Show  events.

    query = '''
    SELECT mt.meetid,mt.title,mt.date,mt.starttime,mt.endtime,et.eventid,et.title,et.starttime,et.endtime, COUNT(pt.eventid),ve.name 
    FROM meet mt, venue ve, event et, participation pt
    WHERE mt.venueid=ve.venueid
    AND mt.meetid=et.meetid
    AND et.eventid=pt.eventid 
    AND mt.meetid = %s
    GROUP BY pt.eventid;
'''
   
    print ("<ol>")
    
    cursor.execute(query,(int(swimmer_id),))
    eve = 0
    
    for (meetid,meettitle,date,stime,etime,event_id,etitle,sttime,ettime,count,name) in cursor:
        if (eve != meetid):
            if (eve != 0):
                print('</ol>') 
            eve = meetid
            print("<h2>Meet #" + str(meetid) + ": " + meettitle +"</h2>")
            print ("Venue: "+name)
            print("<p>Date/time: "+str(date)+": "+str(stime)+" to "+str(etime)+"</p>")
            print("<p>Events:</p>")
            
            print('<ol>')
        print("    <li><a href =?event_id=" + str(event_id) + ">" + str(etitle) + "</a>: " +str(sttime)+
        " to "+str(ettime)+"; with "+ str(count) +" participants.</li>")
    print ("</ol>")
    cursor.close()
    cnx.close()		
    quit()
    

else :	
   
    #	Show all participants

    query = '''
    SELECT CONCAT(swi.fname,' ',swi.lname) AS name,pat.eventid
    FROM swimmer swi, participation pat
    WHERE swi.swimmerid = pat.swimmerid 
    AND pat.eventid = %s;
'''
    cursor.execute(query,(int(event_id),))
    print("<h2> Participants # " + str(event_id) + "</h2>")
    for (name,event_id) in cursor:
        print('<ul>')
        print(" <li>"+name+'</li>')         
        print('</ul>') 
        
    cursor.close()
    cnx.close()	
				  
print ('''</body>
</html>''')