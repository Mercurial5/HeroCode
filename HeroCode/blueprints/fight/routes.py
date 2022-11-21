from os import getenv

import requests
import json
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
    problem_number = body.get('problem_number', None)

    if None in [code, enemy_id, problem_number]:
        return dict(status=False, reason=strings.missed_data)

    enemy = Enemies.get(id=enemy_id)
    if enemy is None:
        return dict(status=False, reason=strings.missed_data)

    problems = Problems.get(enemy_id=enemy_id)
    if problems is None:
        return dict(status=False, reason=strings.missed_data)
    if (problem_number >= problems.count()) or (problem_number < 0):
        return dict(status=False, reason=strings.wrong_index)

    problem_id = problems[problem_number].id
    tests = Tests.get(problem_id=problem_id)

    if tests.count() == 0:
        return dict(status=False, reason="No tests!")
    inputs = ""
    outputs = ""
    for test in tests:
        inputs += test.input + "\nTestCase\n"
        outputs += test.output + "\nTestCase\n"

    enemy_damage = enemy.damage
    user_damage = 1

    data = {
        'code': code,
        'lang': 'py',
        'input': inputs,
        'output': outputs,
        'io_count': tests.count(),
        'io_tuple_count': 1
    }
    headers = {
        'Content-Length': str(data.__sizeof__()),
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    session = requests.session()
    compiler_response = session.post(getenv('CODEAPI_HOST'), data=data, headers=headers, verify=False)
    compiler_json = json.loads(compiler_response.text)

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
