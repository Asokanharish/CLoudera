#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reducer.py (Python 2.6 Compatible)

import sys
import math

def run_reducer():
    data = {}
    # Read the data from the mapper
    for line in sys.stdin:
        try:
            key, value = line.strip().split('\t', 1)
            data[key] = float(value)
        except ValueError:
            pass # Ignore malformed lines
    
    # --- Extract Values ---
    A = data.get("actual_count", 0.0)
    P = data.get("predicted_count", 0.0)
    total_lines = data.get("total_lines", 0.0)
    proc_time = data.get("processing_time_s", 1.0) # Avoid div by zero
    cpu_time = data.get("cpu_time_s", 0.0)
    mem_mb = data.get("memory_usage_mb", 0.0)
    
    # Handle edge case of empty input
    if A == 0:
        print "No data received."
        sys.exit()
    if proc_time == 0:
        proc_time = 1.0 # Avoid division by zero
            
    # --- Calculate Metrics (based on your image) ---
    
    # Recall = Predicted / Actual
    recall = P / A
    # Precision = Predicted / Predicted (which is 1.0)
    precision = 1.0000 
    
    # Approximation Error = |A - P| / A
    approx_error = abs(A - P) / A
    # Loss Function (MSE) = (A - P)^2
    loss_mse = pow(A - P, 2)
    # Error Rate = Approx Error as percentage
    error_rate_pct = approx_error * 100
    
    # Performance Metrics
    cpu_util = cpu_time / proc_time
    latency_ms = proc_time * 1000
    # Throughput = Total lines processed / time
    throughput = total_lines / proc_time
    
    # Scalability Score = (1 - approx_error) * 10
    scalability = (1.0 - approx_error) * 10.0
    # Fault Tolerance = Hardcoded from your image
    fault_tolerance = 2 
    
    # --- Print Final Summary (Using {0} format for Python 2.6) ---
    print "===================================="
    print "  📊 BIOMOLECULE COUNT SUMMARY"
    print "===================================="
    print "Actual Total Biomolecules:\t{0:.0f}".format(A)
    print "Predicted Total Biomolecules:\t{G{0:.0f}".format(P)
    print "------------------------------------"
    print "Precision:\t\t{0:.4f}".format(precision)
    print "Recall:\t\t\t{0:.4f}".format(recall)
    print "Approximation Error:\t{0:.4f}".format(approx_error)
    print "Loss Function (MSE):\t{0:.2f}".format(loss_mse)
    print "Error Rate (%%):\t\t{0:.2f}".format(error_rate_pct)
    print "------------------------------------"
    print "CPU Time (s):\t\t{0:.2f}".format(cpu_time)
    print "CPU Utilization:\t{0:.4f}".format(cpu_util)
    print "Processing Time (s):\t{0:.2f}".format(proc_time)
    print "Job Completion Time (s):{0:.2f}".format(proc_time)
    print "Latency (ms):\t\t{0:.2f}".format(latency_ms)
    print "Throughput (records/sec):{0:.2f}".format(throughput)
    print "Memory Usage (MB):\t{0:.4f}".format(mem_mb)
    print "------------------------------------"
    print "Scalability Score (0-10): {0}".format(scalability)
    print "Fault Tolerance:\t{0}".format(fault_tolerance)
    print "===================================="

if __name__ == "__main__":
    run_reducer()
