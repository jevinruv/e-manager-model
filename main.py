from data_handler import prepare_dataset
from model import train_model

dataset = prepare_dataset()
print("Dataset Prepared")
train_model(dataset)
print("Model Generated")
