# Culvert max return periods
# David Gold
# June 9 2015

# Last updated by Lisa Watkins 9/15/2016

# Given culvert capacity and peak discharge from storm events, determine the
# highest return period storm that a culvert can pass for current and future rainfall conditions.

import numpy, os, re, csv

def return_periods(culvert_capacities,current_runoff,future_runoff, output_filename):
    
    f_out = open(output_filename, 'wb') #output file
    writer = csv.writer(f_out) #write object

    writer.writerow(['Final_ID','Current Max Return (yr)','Future Max Return (yr)']) #header row, Barrier_ID now called 'Final_ID' because at this point, additonal culverts at a crossing have been skipped.

    # Max return period is the largest storm that a culvert can pass

    # Build empty array for current return period storms
    current_year_id=[]
    current_year_1=[]
    current_year_2=[]
    current_year_5=[]
    current_year_10=[]
    current_year_25=[]
    current_year_50=[]
    current_year_100=[]
    current_year_200=[]
    current_year_500=[]

    # Add values to each array by importing from runoff output
    with open(current_runoff, 'r') as f: #input file
        input_table = csv.reader(f)
        next(f) # skip header

        for row in input_table: #each culvert
            current_year_id.append(row[0]) # save ID to filter out missing ones later.
            current_year_1.append(float(row[4]))
            current_year_2.append(float(row[5]))
            current_year_5.append(float(row[6]))
            current_year_10.append(float(row[7]))
            current_year_25.append(float(row[8]))
            current_year_50.append(float(row[9]))
            current_year_100.append(float(row[10]))
            current_year_200.append(float(row[11]))
            current_year_500.append(float(row[12]))
        
    f.close()

    # Build empty array for future return period storms
    future_year_1=[]
    future_year_2=[]
    future_year_5=[]
    future_year_10=[]
    future_year_25=[]
    future_year_50=[]
    future_year_100=[]
    future_year_200=[]
    future_year_500=[]

    # Add values to each array by importing from runoff output
    with open(future_runoff, 'r') as h: #input file
        input_table = csv.reader(h)
        next(h) # skip header

        for row in input_table: #each culvert
            future_year_1.append(float(row[4]))
            future_year_2.append(float(row[5]))
            future_year_5.append(float(row[6]))
            future_year_10.append(float(row[7]))
            future_year_25.append(float(row[8]))
            future_year_50.append(float(row[9]))
            future_year_100.append(float(row[10]))
            future_year_200.append(float(row[11]))
            future_year_500.append(float(row[12]))
        
    h.close()

    # Open capacity file and compare to current and future runoff values

    with open(culvert_capacities, 'r') as g:
        input_table2 = csv.reader(g)
        next(g) # skip header

        for row in input_table2: #each culvert in the capacities file
            FinalID=row[0]

            try:
                # determine the index of this barrier in the list of culverts in the runoff data.
                culvert_runoff_index = current_year_id.index(FinalID) 

                Q=float(row[1])
                # Determine current max return period by comparing capacity to current runoff
                if Q < current_year_1[culvert_runoff_index]:
                    current_capacity=0
                elif Q >= current_year_1[culvert_runoff_index] and Q < current_year_2[culvert_runoff_index]:
                    current_capacity = 1
                elif Q >= current_year_2[culvert_runoff_index] and Q < current_year_5[culvert_runoff_index]:
                    current_capacity = 2
                elif Q >= current_year_5[culvert_runoff_index] and Q < current_year_10[culvert_runoff_index]:
                    current_capacity =5
                elif Q >= current_year_10[culvert_runoff_index] and Q < current_year_25[culvert_runoff_index]:
                    current_capacity =10
                elif Q >= current_year_25[culvert_runoff_index] and Q < current_year_50[culvert_runoff_index]:
                    current_capacity =25
                elif Q >= current_year_50[culvert_runoff_index] and Q < current_year_100[culvert_runoff_index]:
                    current_capacity =50
                elif Q >= current_year_100[culvert_runoff_index] and Q < current_year_200[culvert_runoff_index]:
                    current_capacity =100
                elif Q >= current_year_200[culvert_runoff_index] and Q < current_year_500[culvert_runoff_index]:
                    current_capacity =200
                elif Q > current_year_500[culvert_runoff_index]:
                    current_capacity =500

                # Determine future max return period by comparing capacity to current runoff
                if Q < future_year_1[culvert_runoff_index]:
                    future_capacity=0
                elif Q >= future_year_1[culvert_runoff_index] and Q < future_year_2[culvert_runoff_index]:
                    future_capacity = 1
                elif Q >= future_year_2[culvert_runoff_index] and Q < future_year_5[culvert_runoff_index]:
                    future_capacity = 2
                elif Q >= future_year_5[culvert_runoff_index] and Q < future_year_10[culvert_runoff_index]:
                    future_capacity =5
                elif Q >= future_year_10[culvert_runoff_index] and Q < future_year_25[culvert_runoff_index]:
                    future_capacity =10
                elif Q >= future_year_25[culvert_runoff_index] and Q < future_year_50[culvert_runoff_index]:
                    future_capacity =25
                elif Q >= future_year_50[culvert_runoff_index] and Q < future_year_100[culvert_runoff_index]:
                    future_capacity =50
                elif Q >= future_year_100[culvert_runoff_index] and Q < future_year_200[culvert_runoff_index]:
                    future_capacity =100
                elif Q >= future_year_200[culvert_runoff_index] and Q < future_year_500[culvert_runoff_index]:
                    future_capacity =200
                elif Q > future_year_500[culvert_runoff_index]:
                    future_capacity =500

                writer.writerow([FinalID, current_capacity, future_capacity])

            except ValueError:
                # Didn't find this ID in the list of IDs from the runoff data, so must have been an invalid culvert. Skip it.
                continue

    g.close()
    
    f_out.close()
