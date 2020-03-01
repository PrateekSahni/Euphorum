from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in


def get_summary(text):

    # file = "plain_text.txt" #name of the plain-text file
    # parser = PlaintextParser.from_file(file, Tokenizer("english"))

    parser=PlaintextParser.from_string(text,Tokenizer("English"))
    summarizer = LexRankSummarizer()

    summary = summarizer(parser.document, 5) #Summarize the document with 5 sentences

    # for sentence in summary:
    #     print(sentence)

    return summary
