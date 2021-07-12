
# example dataset here: https://www.kaggle.com/openaddresses/openaddresses-us-west?select=az.csv
import re

def bag_of_ngrams(string, n=3):

  #adapted from:
  #  https://towardsdatascience.com/fuzzy-matching-at-scale-84f2bfd0c536
  #vergvca.github.io/2017/10/14/super-fast-string-matching.html

  string = clean_address_string(string)
  string = ' ' + string + ' '
  ngrams = zip(*[string[i:] for i in range(n)])

  return [''.join(ngram) for ngram in ngrams]


def clean_address_string(string):

  string = str(string)

  chars_to_remove = ["(", ")", ".", "|", "[", "]", "{", "}", "`", "'", "?", ",", "#", "NO.", "No.", "no"]
  rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
  try:
    string = re.sub(rx, '', string)
  except:
    pass

  string = string.replace('&', 'and')
  string = string.replace('?', ' ')

  # , _ - :

  return string