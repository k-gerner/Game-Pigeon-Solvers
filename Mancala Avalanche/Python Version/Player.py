# class that represents the Player (of which, there are 2)
class Player(object):
    score = 0
    def __init__(self):
        pass
    def incrementScore(self):
        self.score += 1
    def copyPlayer(self):
        p = Player()
        p.score = self.score
        return p
