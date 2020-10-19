from aitime.data import DataPool
from aitime.train import KFoldTrainer

"""
    Complete the logical process of training and evaluation
"""

# 1. Create a DataPool - an object to hold all the data I have
dp = DataPool()

# 2. Extract Sequences from raw data
dp.extract_sequences()

# 3. Extract Windows from Sequences
dp.extract_windows()

# 4. Split Data Pool into K datasets
dp.split_pool(10)

# 5. Augment Data
dp.augment_pool()

# 6. Extract Features
dp.extract_features()

# 7. Create a trainer and train / evaluate K datasets
trainer = KFoldTrainer(dp)
print(trainer.train_and_evaluate())
