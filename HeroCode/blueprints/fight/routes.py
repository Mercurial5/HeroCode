from os import getenv

import requests
from flask import request

from HeroCode.blueprints.fight import fight
from HeroCode.models import Enemies
from HeroCode.models import Problems
from HeroCode.models import Tests
from utils import strings


@fight.route('/attack', methods=['POST'])
def attack():
    body = request.json
    code = body.get('code', None)
    enemy_id = body.get('enemy_id', None)

    if None in [code, enemy_id]:
        return dict(status=False, reason=strings.missed_data)

    enemy = Enemies.get(id=enemy_id)
    if enemy is None:
        return dict(status=False, reason=strings.missed_data)

    problem = Problems.get(enemy_id=enemy_id)
    if problem is None:
        return dict(status=False, reason=strings.missed_data)

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

    response = requests.post(getenv('CODEAPI_HOST'), data=data, headers=headers, verify=False)
    compiler_json = response.json()

    return compiler_json

    status = compiler_json['status']
    reason = compiler_json['reason']
    description = compiler_json['description']
    case = compiler_json['case']

    print(compiler_json)

    time = 1
    memory = 1

    damage = user_damage
    if not status:
        time = 1.0 / time
        memory = 1.0 / memory
        damage = enemy_damage

    response = {
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
    problems = Problems.get(enemy_id=enemy_id)
    if None in [enemy, problems]:
        return dict(status=False, reason=strings.not_found)

    problem_names = []
    problem_descriptions = []
    for problem in problems:
        problem_names.append(problem.name)
        problem_descriptions.append(problem.description)

    response = {
        'enemy_hp': enemy.hp,
        'stages_count': problems.count(),
        'problem_names': problem_names,
        'problem_descriptions': problem_descriptions
    }

    return response
