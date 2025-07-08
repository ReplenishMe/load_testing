#CLI COMMAND FOR LOAD TESTING
python cli.py --test main --report                          #cli command for LoadTesting locally for all resources at once and run on default parameters
python cli.py --test location --report                      #cli command for LoadTesting locally for single resources and run on default parameters
python cli.py --r 10 --u 100 --t 10m --test main --report   #cli command for LoadTesting locally for all resources at once and run on custom parameters 


list of ordertrack api resources:
'vendors', 
'users', 
'super_admin', 
'shopping_list', 
'report', 
'bin_family', 
'bin', 
'product', 
'location', 
'licenseplates', 
'production_order', 
'stack', 
'printer', 
'learning_video_map', 
'pick_lineitem', 
'pick'
