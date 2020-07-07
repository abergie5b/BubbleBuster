import json
import os
import hashlib
import time
import requests

class HighScores:
    instance = None
    def __init__(self, dir_='data/'):
        self.dir_ = dir_
        self.path = os.path.join(self.dir_, 'bank.bub')
        if not os.path.exists(self.path):
            self.safe_touch(self.path)
            print('created bank file %s' % self.path)
        HighScores.instance = self

    def safe_touch(self, filepath, mode='w'):
        try:
            with open(filepath, mode) as f:
                json.dump({}, f)
        except Exception as e:
            print('failed to create bank file: %s' % e)

    def get_playername(self):
        url = 'http://names.drycodes.com/1?nameOptions=all'
        js = requests.get(url).json()
        return js.get(0)

    def load_all(self):
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                for k,v in data.items():
                    playerjson = data.get(k)
                    if not self.check(k, playerjson):
                        print('failed to pass check opening bank file %s' % f)
                        return
                print('loaded bank file with %d profiles from %s' % (len(data), self.path))
                return data
        except Exception as e:
            print('failed to open bank file for load: %s' % e)

    def load(self, player):
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                playerjson = data.get(player)
                if self.check(player.playername, playerjson):
                    return playerjson
                else:
                    print('failed to pass check opening bank file %s' % f)
        except Exception as e:
            print('failed to open bank file for player: %s' % e)

    def check(self, playername, playerjson):
        a = playerjson.get('check')
        playerjson['check'] = None
        b = self.secretsauce(playerjson)
        return a == b

    def write(self, player):
        playerjson = {
            'score': player.score,
            'bubbles': player.stats_bubbles,
            'explosions': player.stats_explosions,
            'maxmultiplier': player.stats_maxmultiplier
        }
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                playerdata = data.get(player)

            if playerdata:
                for k,v in playerdata.items():
                    if playerjson[k] < playerdata[k]:
                        playerjson[k] = playerdata[k]
            # extra stuff
            playerjson['rank'] = 1
            playerjson['updated'] = time.time()
            playerjson['check'] = None
            # fun
            if not player.playername:
                player.playername = self.get_playername()
            # top secret
            sauce = self.secretsauce(player.playername, playerjson)
            playerjson['check'] = sauce
            data[player] = playerjson
            with open(self.path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print('failed to open bank file for write: %s' % e)

    def secretsauce(self, playername, playerjson):
        check = hashlib.blake2b(bytes(str(playerjson), encoding='utf=8'), salt=playername)
        check = hashlib.md5(check)
        return check

