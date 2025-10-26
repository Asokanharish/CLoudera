#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mapper.py (Python 2.6 Compatible)

import sys
import time
import resource # For memory and CPU time

# --- Flajolet-Martin (FM) Algorithm ---

def get_trailing_zeros(n):
    """Gets the number of trailing zeros in the binary representation of n."""
    if n == 0:
        return 32 # Assume 32-bit hash
    
    # Use bin() for binary string and strip 0s
    try:
        s = bin(n)
        return len(s) - len(s.rstrip('0'))
    except:
        return 0

class FMEstimator:
    """Implements the basic Flajolet-Martin algorithm."""
    def __init__(self):
        # Our bitmap is just a single integer
        self.bitmap = 0
    
    def add(self, item):
        # Use Python 2's built-in hash().
        # We need a non-negative hash.
        h = abs(hash(item))
        
        # Find the position of the least-significant 1-bit
        # (which is the same as the number of trailing 0s)
        z = get_trailing_zeros(h)
        
        # Set the z-th bit in our bitmap to 1
        self.bitmap = self.bitmap | (1 << z)
        
    def estimate(self):
        if self.bitmap == 0:
            return 0
        
        # Find R, the position of the first 0-bit
        r = 0
        temp_bitmap = self.bitmap
        while (temp_bitmap & 1) == 1:
            temp_bitmap = temp_bitmap >> 1
            r += 1
        
        # The FM estimator is 2^R / phi
        phi = 0.77351
        return int(pow(2, r) / phi)

# --- Main Mapper Logic ---

def run_mapper():
    fm = FMEstimator()
    exact_set = set()
    total_lines = 0
    
    # --- Start Tracking Performance ---
    start_time = time.time()
    start_cpu = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    
    # Read from standard input
    for line in sys.stdin:
        total_lines += 1
        try:
            parts = line.strip().split('\t')
            
            # Skip header or malformed lines
            if len(parts) < 2 or parts[0] == 'gene_id':
                continue
            
            # We will count the unique 'gene_id' from the first column
            key = parts[0] 
            
            # 1. Add to exact set
            exact_set.add(key)
            
            # 2. Add to FM estimator
            fm.add(key)
            
        except Exception as e:
            # Ignore any errors in the stream
            pass 
    
    # --- Stop Tracking Performance ---
    end_time = time.time()
    end_cpu = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    
    # Get memory in MB (this is platform-dependent, ru_maxrss is good for Linux)
    mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024.0) # KB
    mem_usage_mb = mem_usage / 1024.0 # MB
    
    # Get counts
    actual_count = len(exact_set)
    predicted_count = fm.estimate()
    
    # --- Pass all data to the reducer ---
    # We use key-value pairs separated by a tab
    # (Using {0} format for Python 2.6)
    print "{0}\t{1}".format("actual_count", actual_count)
    print "{0}\t{1}".format("predicted_count", predicted_count)
    print "{0}\t{1}".format("total_lines", total_lines)
    print "{0}\t{1}".format("processing_time_s", end_time - start_time)
    print "{0}\t{1}".format("cpu_time_s", end_cpu - start_cpu)
    print "{0}\t{1}".format("memory_usage_mb", mem_usage_mb)

if __name__ == "__main__":
    run_mapper()
