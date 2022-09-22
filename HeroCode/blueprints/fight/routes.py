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

    enemy_damage = enemy.damage
    user_damage = 1

    params = {
        'code': code
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }
    #compiler_response = requests.post(getenv('CODEAPI_HOST'), params=params, headers=headers)
    status = True

    # This values filling from compiler response
    #
    # 10 - value from compiler
    # +1 - time and memory can be (< 1)
    # time and memory dividing user's damage
    time = abs(10) + 1
    memory = abs(10) + 1
    console_message = ""

    damage = user_damage
    if not status:
        time = 1.0 / time
        memory = 1.0 / memory
        damage = enemy_damage

    response = {
        'console_message': console_message,
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
