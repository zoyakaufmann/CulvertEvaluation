# Sorter.py
# David Gold
# November 6, 2015

# Last updated by Lisa Watkins 9/15/2016

# This script will sort the ws data exported from GIS by ID number

import csv
import sys
import operator
import numpy

def sort(ws_data, ID, field_data, output_filename):

    # First write the unsorted ws data to a list and truncate the ID so it
    # is only numbers
   
    try:
        with open(ws_data, 'r') as i:
            input_table = csv.reader(i)
            next(i) # skip header
            id_name=len(ID)
            #i=0
            unsorted=[]
            for row in input_table:
                id_full=row[2]
                id_len=len(id_full)
                id_num=id_full[:id_len-(id_name+2)]
                id_num=int(id_num)
                Area=row[3]
                Tc=row[4]
                CN=row[5]

            
                irow=[id_num,Area,Tc,CN]
                unsorted.append(irow)
        i.close()
    except IOError:
        print "ERROR: Could not find culvert watershed file '" + ws_data + "'. Bailing out."
        sys.exit(0)

    
    # Sort the newly created list by ID number
    ws_sorted=sorted(unsorted, key=operator.itemgetter(0),reverse=False)
    
    # Add the WS ID letters back in
    for i in range(0,len(ws_sorted)):
        ws_sorted[i][0]=str(ws_sorted[i][0])+ID

    F=[] #Empty array for flags
    # Import field data to get flags
    with open(field_data, 'r') as j:
        input_table=csv.reader(j)
        next(j)
        for row in input_table:
            F.append(row[17])
        
    j.close
    

    # Write the sorted data to a new csv file
    f_out= open(output_filename, 'wb')
    w=csv.writer(f_out)
    w.writerow(['Barrier_ID','Area_sqkm','Tc_hr','CN','Flags'])
    
    for i in range(0,len(ws_sorted)):
        Name=ws_sorted[i][0]
        Area=ws_sorted[i][1]
        Tc=ws_sorted[i][2]
        CN=ws_sorted[i][3]
        Flags=F[i]
        
        w.writerow([Name,Area,Tc,CN,Flags])
        
    f_out.close()
