# Final output script
# David Gold
# August 5, 2015

# Last updated by Lisa Watkins 9/15/2016

# This script will combine the data outputs from prior model steps into one csv


def combine(return_periods,capacity,field_data,current_runoff_filename,cap_in, output_filename):

    import numpy, os, re, csv

    #Create arrays for storing the relevant data
    BarrierID=[]
    NAACC_ID=[]
    Current_RP=[]
    Future_RP=[]
    Cap_inlet=[]
    Lat=[]
    Long=[]
    Comments=[]
    WS_AREA=[]
    TC=[]
    CN=[]
    Cross_Sec_Area=[]

    #Extract relevant data from the return periods csv file
    with open(return_periods, 'r') as f:
        input_table = csv.reader(f)
        next(f) # skip header

        k=0
        for row in input_table: #each culvert
            BarrierID.append(row[0])
            Current_RP.append(float(row[1]))
            Future_RP.append(float(row[2]))
            k=k+1

    f.close()

    #Extract relevant data from the capacity csv file
    with open(capacity, 'r') as g:
        input_table = csv.reader(g)
        next(g) # skip header

        for row in input_table: #each culvert
            Cap_inlet.append(float(row[1]))
            Cross_Sec_Area.append(float(row[7]))
            NAACC_ID.append(row[3])
            Lat.append(float(row[4]))
            Long.append(float(row[5]))
            Comments.append(row[6])
    g.close()

    #Extract relevant data from the field data csv file
    #with open(field_data, 'r') as h:
       # input_table = csv.reader(h)
       # next(h) # skip header

      #  for row in input_table: #each culvert


    #h.close()

    #Extract relevant data from the current_runoff csv file
    with open(current_runoff_filename, 'r') as i:
        input_table = csv.reader(i)
        next(i) # skip header

        for row in input_table: #each culvert
            WS_AREA.append(float(row[1]))
            TC.append(float(row[2]))
            CN.append(float(row[3]))

    i.close()

    #Extract relevant data from the culvert geometry csv file
    #with open(cap_in, 'r') as j:
     #   input_table = csv.reader(j)
      #  next(j) # skip header

     #   for row in input_table: #each culvert

            
    #j.close()

    #Write all data to a new csv file
    
    f_out = open(output_filename, 'wb')
    csv_writer = csv.writer(f_out) #output file
    csv_writer.writerow(['CULVERT_ID','NAACC_ID','Latitude','Longitude','Current Max Return Period (yr)','Future Max Return Period (yr)','Capacity (m^3/s)','Cross sectional Area (m^2)','WS Area (sq km)','Tc (hr)','CN','Comments']) #header row

    t=0
    while t<k:
        csv_writer.writerow([BarrierID[t],NAACC_ID[t],Lat[t],Long[t],Current_RP[t],Future_RP[t],Cap_inlet[t],Cross_Sec_Area[t],WS_AREA[t],TC[t],CN[t],Comments[t]])
        t=t+1
    
            
