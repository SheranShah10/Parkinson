import torch
import json
import os

class Trainer:
    def __init__(self, model, optimizer, scheduler, criterion, device, checkpoint_dir):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        self.device = device
        self.scaler = torch.amp.GradScaler('cuda') if torch.cuda.is_available() else None
        self.checkpoint_dir = checkpoint_dir
        self.best_val_loss = float('inf')

    def train_epoch(self, dataloader):
        self.model.train()
        total_loss = 0
        batch_losses = []
        for X, y in dataloader:
            X, y = X.to(self.device), y.to(self.device)
            self.optimizer.zero_grad()
            if self.scaler:
                with torch.amp.autocast('cuda'):
                    outputs = self.model(X)
                    loss = self.criterion(outputs, y)
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                outputs = self.model(X)
                loss = self.criterion(outputs, y)
                loss.backward()
                self.optimizer.step()
            total_loss += loss.item()
            batch_losses.append(loss.item())
        return total_loss / len(dataloader), batch_losses

    def validate_epoch(self, dataloader):
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for X, y in dataloader:
                X, y = X.to(self.device), y.to(self.device)
                outputs = self.model(X)
                loss = self.criterion(outputs, y)
                total_loss += loss.item()
        val_loss = total_loss / len(dataloader)
        if self.scheduler: self.scheduler.step(val_loss)
        return val_loss

    def save_checkpoint(self, epoch, val_loss, is_best=False):
        state = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
            'val_loss': val_loss
        }
        torch.save(state, os.path.join(self.checkpoint_dir, 'last_model.pt'))
        if is_best: torch.save(state, os.path.join(self.checkpoint_dir, 'best_model.pt'))
