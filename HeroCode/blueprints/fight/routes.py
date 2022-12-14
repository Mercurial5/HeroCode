from urllib.parse import unquote
from os import getenv

import requests
import json
from flask import request

from HeroCode import db
from HeroCode.blueprints.login import login
from HeroCode.blueprints.fight import fight
from HeroCode.models import Enemies, Users
from HeroCode.models import Problems
from HeroCode.models import Tests
from HeroCode.models import Action
from utils import strings


@fight.route('/attack', methods=['POST'])
def attack():
    code: str = request.json.get('code', None)
    enemy_id = request.json.get('enemy_id', None)
    username = request.json.get('username', None)

    if None in [code, enemy_id, username]:
        return dict(status=False, reason=strings.missed_data)

    code = unquote(code)

    enemy = Enemies.get(id=enemy_id)
    if enemy is None:
        return dict(status=False, reason=f'Enemy with id {enemy_id} does not exists')

    problem = Problems.get(enemy_id=enemy_id)
    if problem is None:
        return dict(status=False, reason=f'Problem with enemy_id {enemy_id} does not exists')

    tests = Tests.get(problem_id=problem.id)

    if len(tests) == 0:
        return dict(status=False, reason="No tests!")

    inputs = [test.input for test in tests]
    outputs = [test.output for test in tests]

    weak_inputs, weak_outputs = inputs[:2], outputs[:2]
    strong_inputs, strong_outputs = inputs[2:], outputs[2:]

    enemy_damage = enemy.damage
    user_damage = 50

    data = {
        'code': code,
        'lang': 'python',
        'weak_inputs': weak_inputs,
        'weak_outputs': weak_outputs,
        'strong_inputs': strong_inputs,
        'strong_outputs': strong_outputs,
        'case_time': 2
    }
    headers = {
        'Content-Length': str(data.__sizeof__()),
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    response = requests.post(getenv('CODEAPI_HOST'), data=data, headers=headers, verify=False).json()
    response['hp_damage'] = enemy.hp if response['status'] else enemy.damage

    body = request.json
    user = Users.get(username=username)
    action = Action(type='fight', text=str(response) + str(body), user_id=user.id)
    db.session.add(action)
    db.session.commit()

    return response

    status = response['status']
    reason = response['reason']
    description = response['description']
    case = response['case']

    print(response)

    time = 1
    memory = 1

    damage = user_damage
    if not status:
        time = 1.0 / time
        memory = 1.0 / memory
        damage = enemy_damage

    response = {
        'status': True,
        'reason': reason,
        'console_message': description,
        'status': status,
        'hp_damage': damage / time,
        'armor_damage': damage / memory
    }

    return dict(response)


@fight.route('/get_level', methods=['POST'])
def get_level():
    body = request.json
    enemy_id = body.get('enemy_id', None)
    if enemy_id is None:
        return dict(status=False, reason=strings.missed_data)

    enemy = Enemies.get(id=enemy_id)
    problem = Problems.get(enemy_id=enemy_id)
    if None in [enemy, problem]:
        return dict(status=False, reason=strings.not_found)

    response = {
        'status': True,
        'enemy_hp': enemy.hp,
        'stages_count': 1,
        'problem_names': [problem.name],
        'problem_descriptions': [problem.description],
        'problem_solutions': [problem.solution]
    }

    return response
