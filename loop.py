import os

mta_run = 4
arcade_run = 1
prefill_run = 4
bus_pinball_run = 2

#fill up table with 100 bus stops
print("fill up table with 100 bus stops")
for i in range(mta_run):
    os.system('python main.py')

#fill up aracde table and update mta arcade_id
print("#fill up aracde table and update mta arcade_id (give it 30 seconds)")
for i in range(arcade_run):
    os.system('python main.py')

#prefill with 100 pinball
print("prefilling with 100 pinball")
for i in range(prefill_run):
    os.system('python main.py')

#add more pinball near bus stop
print("add more pinball near bus stop")
for i in range(bus_pinball_run):
    os.system('python main.py')
