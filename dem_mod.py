#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gen_tech.py
#  
#  Copyright 2018  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import pandas as pd
import numpy as np
import sqlalchemy as sa

"""
1 basic build for each region    
    1.1 load the demand - store in a sorted list (np)
    1.2 loop through bid stacks (min and max) in order of cost (pd dataframe has to work the best here)
    1.3 modify cost for gen that's already on (-1000 for min)
    1.4 is there unmet demand and no suppy left? Add to list for interconnector demand
2 repeat for unmet demand for interconnector
    
"""

"""
do I keep the data in table format or I do convert it to 
classes? Table format
Pros:
 - simple to load from db
 - simple to sort
 
Cons:
 - referencing individual data more complex, have to use pandas
 - 
"""

"""
let's mock up the data as a pd df and see how we go
"""
eng = sa.create_engine('postgresql:///dem_model')
gen_data = pd.read_sql_table('gen_data', eng)
print(gen_data)

#create the unique list of regions - change to demand table later
regions = pd.read_sql_query(
'SELECT DISTINCT region FROM gen_data;', eng)
print()
print(regions)

for state in regions:
    for hour_iter in range(24):
        #replace later when reading the demand table
        demand = 150
        
        #set up the masks to extract gen data
        gen_mask = (gen_data['region'] == state and 
        gen_data['hour'] == hour_iter)
        gen_filt = gen_data[gen_mask]
        
        #store the filtered & sorted gen_data for that hour
        hour_gen = gen_filt.sort(['cost'])
        
        #initiate the loop variables for gen tech loop
        filled_demand = 0
        unchecked_gen = True
        gen_list = list(hour_gen['gen_name']) #there shouldn't be multiple entries - data check 1
        gen_iter = 0
        while filled_demand < demand and not(unchecked_gen):
            if ((demand - filled_demand) > 
            hour_gen['gen_name' == gen_list[gen_iter]]):
                filled_demand += (
                hour_gen['gen_name' == gen_list[gen_iter]])
                #add the full generation amount for fully dispatched gen
                
            else:
                filled_demand = demand
                unchecked_gen = false
            
            if 


