import torch
import pandas as pd
import re
from transformers import BertModel, BertTokenizer
from torch.utils.data import Dataset
from torch import nn
import numpy as np
from collections import Counter
from kobert_tokenizer import KoBERTTokenizer
# GPU든 CPU 사용
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# BERT 모델을 불러오기.
model = BertModel.from_pretrained('skt/kobert-base-v1')
# BERT 모델을 위한 토크나이저를 불러오기
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')

# 미리 학습된 감정 분류기 모델을 불러오기
class BERTClassifier(nn.Module):
    def __init__(self, bert, num_classes=6):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.classifier = nn.Linear(bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = output.pooler_output
        logits = self.classifier(pooled_output)
        return logits

# 모델 불러오기
model_path = './.model/model_state_dict.pt'
classifier_model = BERTClassifier(model).to(device)
classifier_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
classifier_model.eval()

#classifier_model = joblib.load('./model_spotify.pkl')

# 평가 함수
def testModel(ly, top_k=2):
    cate = ['기쁨', '분노', '상처', '슬픔', '불안', '당황']
    ly = re.sub('[a-zA-z]', '', ly) # 영문 제거
    ly = re.sub("\n", ' ', ly) #빈칸 제거
    ly = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', ly) #특수문자 제거

    # 토큰화
    encoding = tokenizer.encode_plus(
        ly,
        add_special_tokens=True,
        max_length = 512,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

    with torch.no_grad():
        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)
        logits = classifier_model(input_ids=input_ids, attention_mask=attention_mask)
        probabilities = nn.functional.softmax(logits, dim=1)[0]
        top_k_prob, top_k_idx = torch.topk(probabilities, k=top_k)
        
        # 감정 카운트
        emotion_counts = Counter([cate[idx.item()] for idx in top_k_idx])

        return emotion_counts

# 평가 모델 parameter
def predict_emotion(lyrics_list):
    #lyrics_list = []
    # 모든 노래의 감정을 합산하여 가장 많이 등장한 감정 2개 선택
    all_emotion_counts = Counter()
    for lyric in lyrics_list:
        emotion_counts = testModel(lyric, top_k=2)
        all_emotion_counts += emotion_counts

    # 가장 많이 등장한 감정 2개 선택
    most_common_emotions = all_emotion_counts.most_common(2)
    most_common_emotions_str = ', '.join([emotion for emotion, _ in most_common_emotions])

    return(most_common_emotions_str)
