from googleapiclient.discovery import build
from numpy import random
import requests
from bs4 import BeautifulSoup
import re
import sys
import string
from pyvi import ViTokenizer
import os
# from utils import create_token
from dotenv import load_dotenv
load_dotenv()

class PreProcess:
    def __init__(self):
        self.vowel = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
                ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
                ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
                ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
                ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
                ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
                ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
                ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
                ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
                ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
                ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
                ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]

        self.vowel_to_idx = {}

        for i in range(len(self.vowel)):
            for j in range(len(self.vowel[i]) - 1):
                self.vowel_to_idx[self.vowel[i][j]] = (i, j)
        # self.abc = 1
    def is_valid_vietnam_word(self,word):
        chars = list(word)
        vowel_index = -1
        # print(self.vowel_to_idx)
        for index, char in enumerate(chars):
            x, y = self.vowel_to_idx.get(char, (-1, -1))
            if x != -1:
                if vowel_index == -1:
                    vowel_index = index
                else:
                    if index - vowel_index != 1:
                        return False
                    vowel_index = index
        return True 
    
    def normalize_word_diacritic(self,word):
        """
        diacritic: á, à, ạ, ả, ã
        params:
            raw word
        return:
            word normalize
        """
        if not self.is_valid_vietnam_word(word):
            return word

        chars = list(word)
        diacritic = 0
        vowel_index = []
        qu_or_gi = False
        for index, char in enumerate(chars):
            x, y = self.vowel_to_idx.get(char, (-1, -1))
            if x == -1:
                continue
            elif x == 9:  # check qu
                if index != 0 and chars[index - 1] == 'q':
                    chars[index] = 'u'
                    qu_or_gi = True
            elif x == 5:  # check gi
                if index != 0 and chars[index - 1] == 'g':
                    chars[index] = 'i'
                    qu_or_gi = True
            if y != 0:
                diacritic = y
                chars[index] = self.vowel[x][0]
            if not qu_or_gi or index != 1:
                vowel_index.append(index)
        if len(vowel_index) < 2:
            if qu_or_gi:
                if len(chars) == 2:
                    x, y = self.vowel_to_idx.get(chars[1])
                    chars[1] = self.vowel[x][diacritic]
                else:
                    x, y = self.vowel_to_idx.get(chars[2], (-1, -1))
                    if x != -1:
                        chars[2] = self.vowel[x][diacritic]
                    else:
                        chars[1] = self.vowel[5][diacritic] if chars[1] == 'i' else self.vowel[9][diacritic]
                return ''.join(chars)
            return word

        for index in vowel_index:
            x, y = self.vowel_to_idx[chars[index]]
            if x == 4 or x == 8:  # ê, ơ
                chars[index] = self.vowel[x][diacritic]
                # for index2 in vowel_index:
                #     if index2 != index:
                #         x, y = vowel_to_idx[chars[index]]
                #         chars[index2] = vowel[x][0]
                return ''.join(chars)

        if len(vowel_index) == 2:
            if vowel_index[-1] == len(chars) - 1:
                x, y = self.vowel_to_idx[chars[vowel_index[0]]]
                chars[vowel_index[0]] = self.vowel[x][diacritic]
                # x, y = vowel_to_idx[chars[vowel_index[1]]]
                # chars[vowel_index[1]] = vowel[x][0]
            else:
                # x, y = vowel_to_idx[chars[vowel_index[0]]]
                # chars[vowel_index[0]] = vowel[x][0]
                x, y = self.vowel_to_idx[chars[vowel_index[1]]]
                chars[vowel_index[1]] = self.vowel[x][diacritic]
        else:
            # x, y = vowel_to_idx[chars[vowel_index[0]]]
            # chars[vowel_index[0]] = vowel[x][0]
            x, y = self.vowel_to_idx[chars[vowel_index[1]]]
            chars[vowel_index[1]] = self.vowel[x][diacritic]
            # x, y = vowel_to_idx[chars[vowel_index[2]]]
            # chars[vowel_index[2]] = vowel[x][0]
        return ''.join(chars)

    def normalize_diacritic(self,text):
        """
        normalize diacritic
        params:
            crawl text
        return:
            text normalize
        """
        sentence = text.lower()
        words = sentence.split()
        for index, word in enumerate(words):
            cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
            # print(cw)
            if len(cw) == 3:
                cw[1] = self.normalize_word_diacritic(cw[1])
            words[index] = ''.join(cw)
        return ' '.join(words)

    def normalize_encode(self,text):
        """
        normalize unicode encoding
        params:
            raw text
        return:
            normalization text 
        """
        dicchar = self._load_dict_char()
        return re.sub(
            r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
            lambda x: dicchar[x.group()], text)
    def _load_dict_char(self):
        dic = {}
        char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
            '|')
        charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
            '|')
        for i in range(len(char1252)):
            dic[char1252[i]] = charutf8[i]
        return dic

    def process(self,text):
        """
        pipeline normalize encoding + normalize diacritic
        params:
            raw text
        return:
            normalization text
        """
        norm_enc = self.normalize_encode(text)
        # norm_diac = self.normalize_diacritic(norm_enc)
        # return norm_diac
        return norm_enc
    
    def remove_accent(self,text):
        """
        clean accent for edit distance
        params:
            text has accent
        return:
            text non accent
        """
        list_a = ["à","á","ạ","ả","ã","â","ầ","ấ","ậ","ẩ","ẫ","ă","ằ","ắ","ặ","ẳ","ẵ"]
        list_e = ["è","é","ẹ","ẻ","ẽ","ê","ề","ế","ệ","ể","ễ"]
        list_i = ["ì","í","ị","ỉ","ĩ"]
        list_o = ["ò","ó","ọ","ỏ","õ","ô","ồ","ố","ộ","ổ","ỗ","ơ","ờ","ớ","ợ","ở","ỡ"]
        list_u = ["ù","ú","ụ","ủ","ũ","ư","ừ","ứ","ự","ử","ữ"]
        list_y = ["ỳ","ý","ỵ","ỷ","ỹ"]
        list_d = ["đ"]
        
        text_lower = text.lower()

        for item in list_a:
            text_lower = text_lower.replace(item,'a')
        for item in list_e:
            text_lower = text_lower.replace(item,'e')
        for item in list_i:
            text_lower = text_lower.replace(item,'i')
        for item in list_o:
            text_lower = text_lower.replace(item,'o')
        for item in list_u:
            text_lower = text_lower.replace(item,'u')
        for item in list_y:
            text_lower = text_lower.replace(item,'y')
        for item in list_d:
            text_lower = text_lower.replace(item,'d')

        return text_lower

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def get_content_from_url(url):
    html = requests.get(url)
    tree = BeautifulSoup(html.text,'lxml')
    for invisible_elem in tree.find_all(['script', 'style']):
            invisible_elem.extract()

    paragraphs = [p.get_text() for p in tree.find_all("p")]

    for para in tree.find_all('p'):
        para.extract()

    for href in tree.find_all(['a','strong']):
        href.unwrap()

    tree = BeautifulSoup(str(tree.html),'lxml')

    text = tree.get_text(separator='\n\n')
    text = re.sub('\n +\n','\n\n',text)

    paragraphs += text.split('\n\n')
    paragraphs = [re.sub(' +',' ',p.strip()) for p in paragraphs]
    paragraphs = [p for p in paragraphs if len(p.split()) > 10]

    return ' '.join(paragraphs)

def create_token(mess):
    # input: câu nhập vào của người dùng
    # return: token(_) loại bỏ những special token
    mess_rmspectoken = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9]+\b', mess)
    mess_norm = ' '.join(mess_rmspectoken)
    mess_token = ViTokenizer.tokenize(mess_norm)
    mess_lower = mess_token.lower()
    tokens = mess_lower.split()
    table = str.maketrans('', '', string.punctuation.replace("_", ""))
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    return tokens

def print_50_tokens(para):
    tokens = create_token(para)
    if len(tokens) < 50:
        rs =  tokens
    else:
        rs =  tokens[:50]

    token_space = [item.replace('_',' ') for item in rs]

    return ' '.join(token_space)

def norm_text(mess):
    pp = PreProcess()
    norm_mess = pp.process(mess)
    return norm_mess
def major_vote(tit_tokens,list_phrase):
    mask = [0]*len(list_phrase)
    for i in range(len(list_phrase)):
        for token in tit_tokens:
            if token in list_phrase[i]:
                mask[i] +=1
    for i in range(len(mask)):
        if mask[i] == max(mask):
            vote = list_phrase[i]
            break
    return vote

def pipeline_gg_search(mess,api_key,cse_id):
    mess = norm_text(mess)
    results = google_search(mess, api_key, cse_id, num=10)
    ## get first result
    result = results[0]
    doc = get_content_from_url(result['link']).lower()

    dict_search = {}
    dict_search['link'] = result['link']
    # dict_search['content'] = print_50_tokens(doc)
    dict_search['title'] = result['title']
    tit_tokens = create_token(dict_search['title'])
    list_phrase = doc.split('\n')
    content_vote = major_vote(tit_tokens,list_phrase)
    dict_search['content']  = print_50_tokens(content_vote)
    # return content_vote
    return dict_search

if __name__ == '__main__':
    api_key = os.getenv('GG_API')
    cse_id = os.getenv('CUSTOM_SEARCH_ID')
    
    mess = 'quán cà phê gần bách khoa hcm'

    print(pipeline_gg_search(mess,api_key,cse_id))