import random
import threading
import time
import statistics

buffer_full = False         
data_buffer = []             
missing_count = 0           
corrupted_samples = []


def sensor_simulator():

    global buffer_full, data_buffer, missing_count, corrupted_samples
    
    while True:
        current_block = []
        samples_collected = 0
        expected_samples = 100

        while samples_collected < expected_samples:
            #  missing sample 5% chance of dropout
            if random.random() < 0.05:
                missing_count += 1
                time.sleep(0.01)
                continue
            
            # Generate sample
            if random.random() < 0.03:
                sample = random.choice([-999, -1, 101, 999, 255])
                corrupted_samples.append(sample)
                #add invalid
            else:
                #valid sample data
                sample = random.randint(0, 100)
            
            current_block.append(sample)
            samples_collected += 1
            time.sleep(0.01)
        
        while buffer_full:
            time.sleep(0.01)
        data_buffer = current_block
        buffer_full = True


def separate_valid_invalid(block_data):
    valid = []
    invalid = []
    for s in block_data:
        if 0 <= s <= 100:
            valid.append(s)
        else:
            invalid.append(s)
    return valid, invalid


def calculate_stats(block_data):

    if not block_data:
        return None, None, None, None
    
    data_size = len(block_data)
    max_val = max(block_data)
    min_val = min(block_data)
    mean = sum(block_data) / data_size
    std_dev = statistics.stdev(block_data)

    
    return data_size,max_val, min_val, mean, std_dev


if __name__ == "__main__":

    sensor_thread = threading.Thread(target=sensor_simulator, daemon=True)
    sensor_thread.start()
    
    block_number = 0
    total_missing = 0
    total_corrupted = 0
    
    try:
        while True:
            if buffer_full:
                block_number += 1
                current_samples = data_buffer.copy()
                block_missing = missing_count
                block_corrupted = corrupted_samples.copy()

                buffer_full = False
                missing_count = 0
                corrupted_samples.clear()

                valid_samples, invalid_samples = separate_valid_invalid(current_samples)
                total_missing += block_missing
                total_corrupted += len(block_corrupted) + len(invalid_samples)
                data_size,max_val, min_val, avg, std = calculate_stats(valid_samples)
                print(f"\n{'='*50}")
                print(f"  BLOCK #{block_number}")
                print(f"{'='*50}")
                print(f"  Raw block data : {current_samples[:100]}")
                print(f"  --- ({data_size}")
                print()
                print(f"------------------------------STATISTICAL ANALYSIS--------------------------------")
                print(f"  Maximum Value             : {max_val}")
                print(f"  Minimum Value             : {min_val}")
                print(f"  Average (Mean)            : {avg:.2f}")
                print(f"  Standard Deviation        : {std:.2f}")
                print()
                print(f"  Number of missing samples : {block_missing}")
                print(f"  Invalid samples size      : {len(invalid_samples)}")
                print(f"  Invalid samples           : {invalid_samples if invalid_samples else 'None'}")
                print(f"  Total missing samples     : {total_missing}")
                print(f"  Total corrupted samples   : {total_corrupted}")
                print(f"{'-'*100}")
            
            time.sleep(0.04)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*50}")
        print(f"  Shutdown complete.")