import argparse
from transformers import AutoTokenizer
import pandas as pd
import torch
import glob
from tqdm.auto import tqdm

model_name = "airesearch/wangchanberta-base-att-spm-uncased"

class WangChanBERTaFinetunerDataset(torch.utils.data.Dataset):
    def __init__(
            self, 
            tokenizer, 
            data_dir,
            text_column_name,
            label_column_name,
            ext='.csv',
            max_length=416,
            input_ids=[],
            attention_masks=[],
            labels=[]
        ):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.fnames = glob.glob(f"{data_dir}/*{ext}")
        print(self.fnames)

        self.text_column_name = text_column_name
        self.label_column_name = label_column_name
        self.input_ids = input_ids
        self.attention_masks = attention_masks
        self.labels = labels

        self._build()
        

    def __getitem__(self, idx):
        item = {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_masks[idx], 'labels': self.labels[idx]}
        return item

    def __len__(self):
        return len(self.labels)

    def _build(self):
        print('fnames', self.fnames)
        for fname in tqdm(self.fnames):
            df = pd.read_csv(fname)
            
            texts = list(df[self.text_column_name].values)
            labels = list(df[self.label_column_name].values)

            # tokenize
            tokenized_inputs = self.tokenizer(
                texts,
                # max_length=self.max_length,
                truncation=True,
                padding=True
            )


            # add to list
            self.input_ids += tokenized_inputs['input_ids']
            self.attention_masks += tokenized_inputs['attention_mask']
            self.labels += labels
    
        self.input_ids = torch.tensor(self.input_ids)
        self.attention_masks = torch.tensor(self.attention_masks)
        self.labels = torch.tensor(self.labels)


class GZipDataset(torch.utils.data.Dataset):
    def __init__(
            self, 
            tokenizer, 
            data_dir,
            text_column_name,
            label_column_name,
            ext='.csv',
            max_length=416,
            input_ids=[],
            attention_masks=[],
            labels=[]
        ):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.fnames = glob.glob(f"{data_dir}/*{ext}")
        print(self.fnames)

        self.text_column_name = text_column_name
        self.label_column_name = label_column_name
        self.input_ids = input_ids
        self.attention_masks = attention_masks
        self.labels = labels

        self._build()
        

    def __getitem__(self, idx):
        item = {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_masks[idx], 'labels': self.labels[idx]}
        return item

    def __len__(self):
        return len(self.labels)

    def _build(self):
        print('fnames', self.fnames)
        for fname in tqdm(self.fnames):
            df = pd.read_csv(fname)
            
            texts = list(df[self.text_column_name].values)
            labels = list(df[self.label_column_name].values)

            # tokenize
            tokenized_inputs = self.tokenizer(
                texts,
                # max_length=self.max_length,
                truncation=True,
                padding=True
            )


            # add to list
            self.input_ids += tokenized_inputs['input_ids']
            self.attention_masks += tokenized_inputs['attention_mask']
            self.labels += labels
    
        self.input_ids = torch.tensor(self.input_ids)
        self.attention_masks = torch.tensor(self.attention_masks)
        self.labels = torch.tensor(self.labels)
        # print(f'input_ids: type: {type(self.input_ids)}, shape: {self.input_ids.shape}')
