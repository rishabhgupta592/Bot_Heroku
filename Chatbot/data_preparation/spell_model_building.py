import re
import collections
import dill
import os, sys
if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as cfg


def words(data): return re.findall('[a-z]+', data.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model


# file_path = cfg.ROOT + '/DataPreparation/Data_prep/Big.txt'
vocab_file_name = "DataPrepCorpus.txt"
vocab_file_short_path = cfg.ROOT + '/data_preparation/vocab/'
spell_model_short_path = cfg.ROOT + '/data_preparation/vocab/'
spell_model_file_name = "spell_model"

def build_spell_model(company_name):
    vocab_file_path = vocab_file_short_path + company_name + "/" + vocab_file_name
    with open(vocab_file_path, 'rb') as f:
        big_file = f.read()

    NWORDS = train(words(big_file))
    spell_model_path = spell_model_short_path + company_name + "/" + spell_model_file_name
    with open(spell_model_path, 'wb') as out:
        dill.dump(NWORDS, out)


if __name__ == "__main__":
    build_spell_model()