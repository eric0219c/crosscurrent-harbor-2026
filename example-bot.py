#!/usr/bin/env python3
"""Play one actual game through the public API. No accounts or money."""
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

origin = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://127.0.0.1:8792'
def call(path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(origin + path, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)
created = call('/api/games', {'name': 'Harbor API Skiff', 'seats': 3, 'kind': 'agent'})
code, token, player_id = created['state']['code'], created['token'], created['playerId']
state_file = Path('.harbor-bot-state.json')
fd = os.open(state_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as f:
    json.dump({'origin': origin, 'room': code, 'playerId': player_id, 'token': token}, f)
call('/api/games/' + code + '/bots', {'token': token})
state = call('/api/games/' + code + '/start', {'token': token})['state']
print('Room:', code, '— keep your local token file private.')
def distance(a, b):
    return abs(a % 5 - b % 5) + abs(a // 5 - b // 5)
while state['status'] == 'playing':
    if state['currentPlayerId'] != player_id:
        time.sleep(1)
        state = call('/api/games/' + code)['state']
        continue
    me = state['players'][player_id]
    legal = state['legalActions']
    bank = next((a for a in legal if a['type'] == 'bank' and me['cargo']), None)
    haul = next((a for a in legal if a['type'] == 'salvage' and me['cargo'] < 3), None)
    if bank or haul:
        action = bank or haul
    else:
        targets = [0, 4, 20, 24] if me['cargo'] >= 2 else [int(k) for k, v in state['stock'].items() if v]
        targets = targets or [0, 4, 20, 24]
        moves = [a for a in legal if 'to' in a]
        action = min(moves, key=lambda a: (min(distance(a['to'], t) for t in targets), a['type'] == 'dash', a['to'])) if moves else {'type': 'rest'}
    try:
        state = call('/api/games/' + code + '/actions', {'token': token, 'action': action})['state']
    except urllib.error.HTTPError as error:
        if error.code != 409:
            raise
        state = call('/api/games/' + code)['state']
    time.sleep(.15)
print('Finished:', [(p['name'], p['points']) for p in state['players']])
print('Match log:', origin + '/api/games/' + code + '/replay')
