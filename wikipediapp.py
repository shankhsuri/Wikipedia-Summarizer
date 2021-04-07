import streamlit as st
import bs4 as bs
import urllib.request
import re
import heapq
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
PAGE_CONFIG = {"page_title":"StColab.io","page_icon":":smiley:","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

def main():
    menu = ["Tool","More"]
    choice = st.sidebar.selectbox('Menu',menu)
    if choice == 'Tool':
        st.header("Wikipedia Summarizer")
        st.write("A machine learning tool which can summarize wikipedia articles")
        topic_input = st.text_input('Enter topic to be summarized')
        topic_input = topic_input.replace(" ", "_")
        number_input=st.number_input('Enter the number of sentences in summary', min_value=1, max_value=50)
        if st.button('Generate Result'):
            try:
                scraped_data = urllib.request.urlopen(f'https://en.wikipedia.org/wiki/{topic_input}')
                article = scraped_data.read()
                parsed_article = bs.BeautifulSoup(article,'lxml')
                paragraphs = parsed_article.find_all('p')
                article_text = ""
                for p in paragraphs:
                    article_text += p.text
                article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
                article_text = re.sub(r'\s+', ' ', article_text)
                formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
                formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
                sentence_list = sent_tokenize(article_text)
                stopword = stopwords.words('english')
                word_frequencies = {}
                for word in word_tokenize(formatted_article_text):
                    if word not in stopword:
                        if word not in word_frequencies.keys():
                            word_frequencies[word] = 1
                        else:
                            word_frequencies[word] += 1
                maximum_frequncy = max(word_frequencies.values())

                for word in word_frequencies.keys():
                    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
                sentence_scores = {}
                for sent in sentence_list:
                    for word in word_tokenize(sent.lower()):
                        if word in word_frequencies.keys():
                            if len(sent.split(' ')) < 30:
                                if sent not in sentence_scores.keys():
                                    sentence_scores[sent] = word_frequencies[word]
                                else:
                                    sentence_scores[sent] += word_frequencies[word]
                summary_sentences = heapq.nlargest(number_input, sentence_scores, key=sentence_scores.get)
                summary = ' '.join(summary_sentences)
                st.write(summary)
            except:
                st.error('Page does not exist')
if __name__=='__main__':main()
