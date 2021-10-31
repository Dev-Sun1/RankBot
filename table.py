async def createTable(vals, headers):
    String = ""
    counter = 1
    String += ("%s:\t%s\t\t\t%s" % (headers[0], headers[2], headers[1])) + "\n"
    for i in vals:
        String += ("%s:\t\t\t\t\t\t%s\t\t\t%s" % (counter, i[1], i[0])) + "\n"
        counter += 1
        
    return String
        
        
    
    
    
    
        
    