from sklearn.base import BaseEstimator, TransformerMixin
from langdetect import detect
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)
import spacy
nlp = spacy.load("es_core_news_sm")
import re, string, unicodedata
import inflect
import pandas as pd

class Traductor(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos=[]
        for i in range(len(X)): 
            if detect(X.iloc[i]['review_text']) != "es":
                textos.append(GoogleTranslator(source='auto', target='es').translate(text=X.iloc[i]['review_text']))
            else:
                textos.append(X.iloc[i]['review_text'])
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X
    
class Lematizador(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos=[]
        for i in range(len(X)):
            new_words = []
            tokens = nlp(X.iloc[i]['review_text'])
            for token in tokens:
                if not token.is_stop:
                    new_words.append(token.lemma_)
            textos.append(new_words)
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X
    
class NoASCII(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos=[]
        for i in range(len(X)):
            new_words = []
            words = X.iloc[i]['review_text']
            for word in words:
                new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
                new_words.append(new_word)
            textos.append(new_words)
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X
    
class Minusculas(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos=[]
        for i in range(len(X)):
            new_words = []
            words = X.iloc[i]['review_text']
            for word in words:
                new_word = word.lower()
                new_words.append(new_word)
            textos.append(new_words)
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X
    
class SinPuntuacion(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos=[]
        for i in range(len(X)):
            new_words = []
            words = X.iloc[i]['review_text']
            for word in words:
                new_word = re.sub(r'[^\w\s]', '', word)
                if new_word != '':
                    new_words.append(new_word)
            textos.append(new_words)
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X

class ReemplazadorNumeros(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos=[]
        for i in range(len(X)):
            p = inflect.engine()
            new_words = []
            words = X.iloc[i]['review_text']
            for word in words:
                if word.isdigit():
                    new_word = p.number_to_words(word)
                    new_words.append(new_word)
                else:
                    new_words.append(word)
            textos.append(new_words)
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X
    
class SinVacios(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos=[]
        for i in range(len(X)):
            new_words = []
            words = X.iloc[i]['review_text']
            for word in words:
                if word!=" ":
                    new_words.append(word)
            textos.append(new_words)
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X
    
class ArrayToString(BaseEstimator, TransformerMixin):
    def __init__(self, by=1, columns=None):        
        self.by = by        
        self.columns = columns
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        textos = []
        for i in range(len(X)):
            words = X.iloc[i]['review_text']
            textos.append(' '.join(map(str, words)))
        X=X.drop(['review_text'], axis=1)
        X["review_text"]=textos
        return X["review_text"]