import reviews

__author__ = 'Damon Hayhurst'

class Tag(object):

    def __init__(self, name, rank):
        self.name = name.lower()
        self.rank = rank

    def __repr__(self):
        return self.name


class Adj(Tag):

    def __init__(self, top_sim=5):
        super(Tag, self).__init__()
        self.similar = self.most_similar(topn=top_sim)


    def most_similar(self, more_words=None, minimum=0.7, topn=5):
        model = reviews.model
        sim_adjs = []
        try:
            if more_words != None:
                similar = model.most_similar(positive=[self.name, more_words], topn=topn)
            else:
                similar = model.most_similar(positive=[self.name])
            rank = 1
            for sim in similar:
                if sim[1] >= minimum:
                    sim_adjs.append(SimAdj(sim[0], rank))
                    rank += 1
                else:
                    break
        finally:
            return sim_adjs



class SimAdj(Adj):

    def __init__(self, similarity):
        super(Adj, self).__init__()
        self.similarity = similarity

class Ent(Tag):

    def __init__(self, type):
        super(Tag, self).__init__()
        self.type = type

def word_to_tag(word, rank, type, ent_type=None):
    if type == "ENT":
        return Ent(word, ent_type)
    elif type == "ADJ":
        return Adj(word)
    else:
        return None
