import time  
import numpy as np  

class DataProcessor:  
    def __init__(self, data):  
        self.data = data  
        self.results = []  
  
    def optimize_processing(self):  
        start_time = time.time()  
        # Using numpy for vectorized operations  
        self.results = np.sqrt(self.data)  
        end_time = time.time()  
        print(f"Processing time: {end_time - start_time} seconds")  
  
    def filter_results(self, threshold):  
        # Using numpy for boolean indexing  
        return self.results[self.results > threshold]  

if __name__ == '__main__':  
    data = np.random.rand(1000000)  
    processor = DataProcessor(data)  
    processor.optimize_processing()  
    filtered = processor.filter_results(0.5)  
    print(filtered[:10])  
