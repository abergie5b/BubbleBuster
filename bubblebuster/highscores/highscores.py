import bubblebuster.settings as st

import json
import os
import hashlib as hl
import time
import urllib.request

class HighScores:
    instance = None
    def __init__(self, dir_='data/'):
        self.dir_ = dir_
        self.path = os.path.join(self.dir_, 'bank.bub')
        if not os.path.exists(self.path):
            self.safe_touch(self.path)
        HighScores.instance = self

    def safe_touch(self, filepath, mode='w'):
        try:
            with open(filepath, mode) as f:
                json.dump({}, f)
                if st.DEBUG:
                    print('created bank file %s' % self.path)
        except Exception as e:
            print('failed to create bank file: %s' % e)

    def get_playername(self):
        url = 'http://names.drycodes.com/1?nameOptions=all'
        weburl = urllib.request.urlopen(url)
        data = weburl.read()
        encoding = weburl.info().get_content_charset('utf-8')
        js = json.loads(data.decode(encoding))
        return js[0] if js else ''

    def load_all(self):
        result = {}
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                for k,v in data.items():
                    playerjson = data.get(k)
                    if not self.check(k, playerjson):
                        if st.DEBUG:
                            print('failed to pass check opening bank file for %s' % k)
                        result[k] = {'score': -69, 'bubbles': 'cheater', 'explosions': 'hacker', 'maxmultiplier': 'weasel'}
                    else:
                        result[k] = playerjson
                if st.DEBUG:
                    print('loaded bank file with %d profiles from %s' % (len(data), self.path))
                return result
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
                    if st.DEBUG:
                        print('failed to pass check opening bank file %s' % f)
        except Exception as e:
            print('failed to open bank file for player: %s' % e)

    def check(self, playername, playerjson):
        a = playerjson.get('check')
        playerjson['check'] = None
        b = self.ash(playername, playerjson)
        return a == b

    def write(self, player):
        # fun
        if not player.playername:
            player.playername = self.get_playername()

        playerjson = {
            'score': player.score,
            'bubbles': player.stats_bubbles,
            'explosions': player.stats_explosions,
            'maxmultiplier': player.stats_maxmultiplier
        }

        with open(self.path, 'r') as f:
            data = json.load(f)

        # update
        playerdata = data.get(player.playername)
        if not playerdata:
            playerdata = playerjson
        else:
            playerdata['score'] += playerjson['score']
            playerdata['bubbles'] += playerjson['bubbles']
            playerdata['explosions'] += playerjson['explosions']
            playerdata['maxmultiplier'] = max(playerjson['maxmultiplier'], playerdata['maxmultiplier'])

        # extra stuff
        playerdata['rank'] = 1
        playerdata['updated'] = time.time()
        playerdata['check'] = None

        # top secret
        sauce = self.ash(player.playername, playerdata)
        playerdata['check'] = sauce

        # write me
        data[player.playername] = playerdata
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def ash(self, n, p):
        e = 'utf-8'
        s = bytes(n, e)[:15]
        c = hl.blake2b(bytes(str(p), e), salt=s)
        return hl.md5(c.digest()).hexdigest()

