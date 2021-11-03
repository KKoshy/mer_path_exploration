import os

DATA_DIR = "data"
MASTER_SVF = os.path.join(DATA_DIR, 'mer2_master.svf')
REFERENCE_FRAME = ['name', 'index1']
OFFSET = ['x', 'y', 'z']
ORIENTATION = ['s', 'v1', 'v2', 'v3']
DERIVATION = ['solution_id']
NUMERIC_FIELDS = ['x', 'y', 'z', 's', 'v1', 'v2', 'v3']
SOLUTION_FIELDS = ['solution_id', 'name', 'add_date', 'index1']
SVF_SHEET = "svf_data"
