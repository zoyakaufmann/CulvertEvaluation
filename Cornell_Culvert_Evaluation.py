# Culvert Evaluation Model
# David Gold
# August 4, 2015
#
# This script is based on the culvert evaluation model developed by Rebecca Marjerison in 2013
#
# This script will:
# 1. Determine the runoff peak discharge of given culvert's watershed using the SCS graphical curve number method.
# 2. Calculate the cross sectional area of each culvert and assign c and Y coefficients based on culvert characteristics
# 3. Determine the maximum capacity of a culvert using inlet control
# 4. Determine the maximum return period storm that the culvert can safely pass before overtopping for both current and
#    future rainfall conditions.
#
# Inputs:
# 1. Culvert Watershed data input: A CSV file containing data on culvert watershed characteristics including 
#    Culvert IDs, WS_area in sq km, Tc in hrs and CN

# 2. NRCC export CSV file of precipitation data (in) for the 1, 2, 5, 10, 25, 50, 100, 200 and 500 yr 24-hr storm events
#    Check that the precipitation from the 1-yr, 24 hr storm event is in cell K-11
#
# 3. Field data collection input: A CSV file containing culvert data gathered in the field using either then NAACC
#    data colleciton format or Tompkins county Fulcrum app
#
# Outputs:
# 1. Culvert geometry file: A CSV file containing culvert dimensions and assigned c and Y coefficients
#
# 2. Capacity output: A CSV file containing the maximum capacity of each culvert under inlet control
#
# 3. Current Runoff output: A CSV file containing the peak discharge for each culvert's watershed for
#    the analyzed return period storms under current rainfall conditions
#
# 4. Future Runoff output: A CSV file containing the peak discharge for each culvert's watershed for
#    the analyzed return period storms under 2050 projected rainfall conditions
#
# 5. Return periods output: A CSV file containing the maximum return period that each culvert can
#    safely pass under current rainfall conditions and 2050 projections.
#
# 6. Final Model ouptut: A CSV file that summarizes the above model outputs in one table

print('Cornell Culvert Evaluation Model')
print('--------------------------------\n')

import numpy, os, re, csv, runoff, capacity_prep, capacity, return_periods, time, final_output, sys, sorter

#add note about making sure that the same culverts are in both sheets?

# 0. LOAD LIST OF WATERSHED FILES

# Input watershed file name.
counties_filename = raw_input('\nEnter counties csv file name: ')
if counties_filename[len(counties_filename) - 4:] != '.csv':
    counties_filename = counties_filename + '.csv'   

# Open watershed file and load all the lists of files from it.
try:
    with open(counties_filename, 'r') as list_file:
        input_table = csv.reader(list_file)

        # Skip descriptive header.
        next(list_file) 
        counties = []
        # Load each row in the csv as a list of the abbreviation and files for a given watershed.
        for row in input_table:
            watershed_abbreviation = row[0]

            # Note each of the files in the watershed list csv *must* have the .csv after it already.
            culvert_watershed_file = row[1]
            watershed_precipitation_file = row[2]
            field_data_collection_file = row[3]
    
            county_row = [watershed_abbreviation, culvert_watershed_file, watershed_precipitation_file, field_data_collection_file]
            counties.append(county_row)
    list_file.close()
except IOError:
    print "ERROR: Could not find counties csv file '" + counties_filename + "'. Bailing out."
    sys.exit(0)

# For each watershed listed in the watersheds csv, perform all the computations:
for county in counties:
    # Grab the abbreviation and filenames from the watershed row.
    ws_name = county[0]
    ws_data = ws_name + '/data/' + county[1]
    ws_precip = ws_name + '/data/' + county[2]
    field_data = ws_name + '/data/' + county[3]

    # Create filenames for all of the output files.
    output_prefix = ws_name + "/output/" + ws_name + "_"
    current_runoff_filename     = output_prefix + "current_runoff.csv"
    future_runoff_filename      = output_prefix + "future_runoff.csv"
    sorted_filename             = output_prefix + "sorted_ws.csv"
    culvert_geometry_filename   = output_prefix + "culv_geom.csv"
    capacity_filename           = output_prefix + "capacity_output.csv"
    return_period_filename      = output_prefix + 'return_periods.csv'
    final_output_filename       = output_prefix + 'model_output.csv'

    print "\nRunning calculations for culverts in county " + ws_name + ":"

    # 1. WATERSHED PEAK DISCHARGE
    
    # Sort watersheds so they match original numbering (GIS changes numbering)
    sorter.sort(ws_data, ws_name, field_data, sorted_filename)

    # Culvert Peak Discharge function calculates the peak discharge for each culvert for current and future precip
    print " * Calculating current runoff and saving it to " + current_runoff_filename + "."
    runoff.calculate(sorted_filename, ws_precip, 1.0, current_runoff_filename)
    print " * Calculating future runoff and saving it to " + current_runoff_filename + "."
    runoff.calculate(sorted_filename, ws_precip, 1.15, future_runoff_filename) # 15% increase in rainfall predicted for future conditions

    # 2. CULVERT GEOMETRY
    print " * Calculating culvert geometry and saving it to " + culvert_geometry_filename + "."
    # Culvert Capacity Prep function calculates the cross sectional area and assigns c and Y coeffs to each culvert
    capacity_prep.geometry(field_data, culvert_geometry_filename)

    # 3. CULVERT CAPACITY
    print " * Calculating culvert capacity and saving it to " + capacity_filename + "."
    # Culvert_Capacities function calculates the capacity of each culvert (m^3/s) based on inlet control
    capacity.inlet_control(culvert_geometry_filename, capacity_filename)

    # 4. RETURN PERIODS
    print " * Calculating return periods and saving them to " + return_period_filename + "."
    # Run return period script
    return_periods.return_periods(capacity_filename, current_runoff_filename, future_runoff_filename, return_period_filename)

    # 5. FINAL OUTPUT
    print " * Calculating final output and saving it to " + final_output_filename + "."
    #Run final output script to aggregate all model outputs
    final_output.combine(return_period_filename, capacity_filename, field_data, current_runoff_filename, culvert_geometry_filename, final_output_filename)

print "\nDone! All output files can be found within the folder " + os.getcwd()

