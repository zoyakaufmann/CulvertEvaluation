# Runoff calculation model
# David Gold
# August 2015
#
# Last updated by Lisa Watkins 9/15/2016
#
# Based off of the runoff model created by Rebecca Marjerson in 2013
#
# Determine the runoff peak flow using the SCS curve number method, available in NRCS TR-55
# 
# Inputs:   culvert_Q_input.csv: culvertID, watershed area (sq km), average curve number, time of concentration (hr)
#           ws_precip: csv file exported from the Cornell NRCC of 24 hour storms with return periods 1 to 500 years
#           rainfall_adjustment: scalar, with 1 as current rainfall.
#           output_filename: where to save the results of the runoff calculation.
#
# Outputs:  table of runoff (q_peak) in cubic meters per second for each return periods under current precipitation conditions
#           table of runoff (q_peak) in cubic meters per second for each return periods under future precipitation conditions

import numpy, os, re, csv, sys

def calculate(ws_data, ws_precip, rainfall_adjustment, output_filename):
    # Precipitation values (cm) are average for the overall watershed, for 24 hour storm, from NRCC
    # 1yr,2yr,5yr,10yr,25 yr,50 yr,100yr,200 yr,500 yr storm
    # Rainfall values are read directly from the standard NRCC output format and converted into cm.

    Precips = []

    # Open the precipitation data csv and read all the precipitations out.
    try:
        with open(ws_precip) as g:
            input_precip= csv.reader(g)
            
	    # Skip the first 10 rows of the csv, which are assorted header information.
            for j in range (1, 11): 
                next(g)

            k=1    
            for row in input_precip:
                P=float(row[10]) # Grab data from column containing 24-hour estimate
                Precips.append(P*2.54*rainfall_adjustment) # convert to cm and adjust for future rainfall conditions (if rainfall_adjustment is > 1)
                if k>8:
                    break
                else:
                    k=k+1
        g.close()
    except IOError:
        print "ERROR: Could not find watershed precipitation data file '" + ws_precip + "'. Bailing out."
        sys.exit(0)

    # Set up to save results to new file.
    f_out = open(output_filename, 'wb')
    csv_writer = csv.writer(f_out) #output file
    csv_writer.writerow(['Barrier_ID','WS_Area','Tc','CN','Y1','Y2','Y5','Y10','Y25','Y50','Y100','Y200','Y500']) #header row

    # Open the culvert watershed file (which has been sorted and saved to a new file).
    with open(ws_data, 'rb') as f: 
        input_table = csv.reader(f) 

        next(f) #skip header
        Qp=[]
        Barrier_ID=[]
        flags=[]
        skipped_culverts=[]
        TC=[]
        cn=[]
        WS_area=[]
        for row in input_table: #each culvert
        
            cID = row[0]
            ws_area = float(row[1]) #sq km, calculated with ArcGIS tools 
            WS_area.append(ws_area)
            tc = float(row[2]) #time of concentration in hours, calculated by ArcGIS script
            TC.append(tc)
            CN = float(row[3]) #area-weighted average curve number
            cn.append(CN)
            fl = int(row[4]) #number of culverts at crossing (0=1 culvert, 2=2 culverts, 3=3 culverts, etc)
            flags.append(fl)
            
            # Skip over culverts where curve number or time of concentration are 0, since this indicates invalid data.
            # Note that this results in output files with potentially fewer culverts in them than the input file.
            #if CN == 0 or tc == 0:
               # skipped_culverts.append(cID) ##THIS IS COMMENTED OUT BECAUSE IT CURRENTLY SCREWS UP MECHANISM THAT COMBINES MULTICULVERT CROSSINGS
                #continue

            Barrier_ID.append(cID)
            
            #calculate storage, S in cm
            Storage = 0.1*((25400.0/CN)-254.0)
            Ia = 0.2*Storage #inital abstraction, amount of precip that never has a chance to become runoff

            #setup precip list for the correct watershed from dictionary
        
            P = numpy.array(Precips)
        
            #calculate depth of runoff from each storm
            #if P < Ia NO runoff is produced
            Pe = (P - Ia)
            Pe = numpy.array([0 if i < 0 else i for i in Pe]) # get rid of negative Pe's
            Q = (Pe**2)/(P+(Storage-Ia))

            
            #calculate q_peak, cubic meters per second
            # q_u is an adjustment because these watersheds are very small. It is a function of tc,
            #  and constants Const0, Const1, and Const2 which are in turn functions of Ia/P (rain_ratio) and rainfall type
            #  We are using rainfall Type II because that is applicable to most of New York State
            #  rain_ratio is a vector with one element per input return period
            rain_ratio = Ia/P
            rain_ratio = numpy.array([.1 if i < .1 else .5 if i > .5 else i for i in rain_ratio])
            # keep rain ratio within limits set by TR55
        
            Const0 = (rain_ratio ** 2) * -2.2349 + (rain_ratio * 0.4759) + 2.5273
            Const1 = (rain_ratio ** 2) * 1.5555 - (rain_ratio * 0.7081) - 0.5584
            Const2 = (rain_ratio ** 2)* 0.6041 + (rain_ratio * 0.0437) - 0.1761

            qu = 10 ** (Const0+Const1*numpy.log10(tc)+Const2*(numpy.log10(tc))**2-2.366)
            q_peak = Q*qu*ws_area #qu has weird units which take care of the difference between Q in cm and area in km2
            Qp.append(q_peak)
    
                    
    L=len(Qp)
    i=0
    while i < L:
        #csv_writer.writerow([Barrier_ID[i],Qp[i][0],Qp[i][1],Qp[i][2],Qp[i][3],Qp[i][4],Qp[i][5],Qp[i][6],Qp[i][7],Qp[i][8]])
        #i=i+1          Lisa commented this out 9/15/16 to add the lines below (copied in from Model_2-29 in order to make sure it's skipping duplicate watersheds to properly match skipped cells from capacity script
        if flags[i]>1:
            csv_writer.writerow([Barrier_ID[i],WS_area[i],TC[i],cn[i],Qp[i][0],Qp[i][1],Qp[i][2],Qp[i][3],Qp[i][4],Qp[i][5],Qp[i][6],Qp[i][7],Qp[i][8]])
            i=i+flags[i]
        else:
            csv_writer.writerow([Barrier_ID[i],WS_area[i],TC[i],cn[i],Qp[i][0],Qp[i][1],Qp[i][2],Qp[i][3],Qp[i][4],Qp[i][5],Qp[i][6],Qp[i][7],Qp[i][8]])
            i=i+1           
    f.close()
    f_out.close()

    if (len(skipped_culverts) > 0):
        print "   ! The following culverts had invalid curve number or time of concentration and were skipped:\n" + ", ".join(skipped_culverts)

    return f_out


