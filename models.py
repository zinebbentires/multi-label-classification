import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm

class AudioNet1(nn.Module):
    def __init__(self):
        super(AudioNet1,self).__init__()
        self.fc1 = nn.Linear(256, 22) # linear layer (256 -> 22)

        
    def forward(self,x):
        x = self.fc1(x)
        return x
    
class UsageNet1(nn.Module):
    def __init__(self):
        super(UsageNet1,self).__init__()
        self.fc1 = nn.Linear(128, 22) # linear layer (128 -> 22)

        
    def forward(self,x):
        x = self.fc1(x)
        return x
    
# training function
def train(model, dataloader, optimizer, criterion, train_data, device, audio_bool):
    print('Training')
    model.train()
    counter = 0
    train_running_loss = 0.0
    for i, data in tqdm(enumerate(dataloader), total=int(len(train_data)/dataloader.batch_size)):
        counter += 1
        if audio_bool:
            data, target = data['audio_feature'].to(device), data['label'].to(device)
        else:
            data, target = data['usage_feature'].to(device), data['label'].to(device)
        optimizer.zero_grad()
        outputs = model(data)
        # apply sigmoid activation to get all the outputs between 0 and 1
        outputs = torch.sigmoid(outputs)
        loss = criterion(outputs, target)
        train_running_loss += loss.item()
        # backpropagation
        loss.backward()
        # update optimizer parameters
        optimizer.step()
        
    train_loss = train_running_loss / counter
    return train_loss

# validation function
def validate(model, dataloader, criterion, val_data, device, audio_bool):
    print('Validating')
    model.eval()
    counter = 0
    val_running_loss = 0.0
    with torch.no_grad():
        for i, data in tqdm(enumerate(dataloader), total=int(len(val_data)/dataloader.batch_size)):
            counter += 1
            if audio_bool:
                data, target = data['audio_features'].to(device), data['label'].to(device)
            else:
                data, target = data['usage_feature'].to(device), data['label'].to(device)
            outputs = model(data)
            # apply sigmoid activation to get all the outputs between 0 and 1
            outputs = torch.sigmoid(outputs)
            loss = criterion(outputs, target)
            val_running_loss += loss.item()
        
        val_loss = val_running_loss / counter
        return val_loss