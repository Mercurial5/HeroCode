from os import getenv

import requests
from flask import request

from HeroCode.blueprints.fight import fight
from HeroCode.models import Enemies
from HeroCode.queries import getters
from utils import strings


@fight.route('/attack', methods=['POST'])
def attack():
    body = request.json
    code = body['code']
    enemy_id = body['enemy_id']
    enemy_damage = Enemies.get(id=enemy_id)['damage']
    user_damage = 1

    params = {
        'code': code
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }
    compiler_response = requests.post(getenv('CODEAPI_HOST'), params=params, headers=headers)
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

    # Changing damage for enemy
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
    enemy_id = body['enemy_id']

    enemy = getters.get_enemy(enemy_id)
    if enemy is None:
        return dict(status=False, reason=strings.missed_data)

    problems = getters.get_problems(enemy_id)
    if problems.count() == 0:
        return dict(status=False, reason=strings.problems_is_missing)

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
