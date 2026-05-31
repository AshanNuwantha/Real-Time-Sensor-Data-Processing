import random
import threading
import time
import statistics

calculation_handler_bool = False
temp_number_array = []
missing_data = []


def randomNumberHandler():
    global temp_number_array, missing_data, calculation_handler_bool
    index = 0
    temp_number_array = [0] * 101 # Initilizing array
    while True:
      val = random.randint(0, 100)
      if calculation_handler_bool == False:
        temp_number_array[index] = val
        index = index +1
        if index == 101:
            index = 0
            calculation_handler_bool = True
      else:
        missing_data.append(val) 
      time.sleep(0.01) 




if __name__ == "__main__":
    print(" real-time data processing system")
    thread = threading.Thread(target=randomNumberHandler, daemon=True)
    thread.start()

    try:
        while True:
          if calculation_handler_bool:
            block_data = temp_number_array.copy()
            max_val = max(block_data)
            min_val = min(block_data)
            avg_val = sum(block_data) / len(block_data)
            std_val = statistics.stdev(block_data)

            print(f"\n{'='*100}")
            print("Sensor data set             : ", temp_number_array[:100])
            print("\n")
            print(f"  Count                     :  {len(block_data)-1}")
            print(f"  Maximum Value             :  {max_val}")
            print(f"  Minimum Value             :  {min_val}")
            print(f"  Average (mean)            :  {avg_val:.2f}")
            print(f"  Standard deviation        :  {std_val:.2f}")
            print(f"  Number of missing samples :  {len(missing_data)}")
            print(f"  Invalid samples           :  {missing_data}")
            print(f"\n{'-'*100}")
            calculation_handler_bool = False
            missing_data.clear()
          time.sleep(0.04)
    except KeyboardInterrupt:
       print("\n Stopped ...")