import requests

from HeroCode.blueprints.fight import fight
from HeroCode.queries import getters


@fight.route('/attack', methods=['POST'])
def attack():
    #Attach this variables within request content
    code = "print('Hello, world!')"
    enemy_id = 1
    enemy_damage = 10#?
    user_damage = 10#?
    #...

    # Getting response from compiler
    params = {
        'code': code
    }
    headers = {
        'Content-type': 'content_type_value'
    }
    compiler_response = requests.post('http://example.com', params=params, headers=headers)
    print(compiler_response.__dict__)
    status = True

    # This values filling from compiler response
    #
    # 10 - value from compiler
    # +1 - time and memory can be (< 1)
    # time and memory dividing user's damage
    time = abs(10) + 1
    memory = 10
    console_message = ""

    damage = user_damage

    # Changing damage for enemy
    if not status:
        time = 1.0 / time
        memory = 1.0 / memory
        user_damage = enemy_damage

    response = {
        'console_message': console_message,
        'status': status,
        'hp_damage': damage / time,
        'armor_damage': damage / memory
    }

    return response



@fight.route('/get_level', methods=['GET'])
def get_level():
    # Attach this variables within request content
    enemy_id = 1
    # ...
    enemy = getters.get_enemy(enemy_id)
    problems = getters.get_problems(enemy_id)

    problem_names = []
    problem_descriptions = []
    for problem in problems:
        problem_names.append(problem.name)
        problem_descriptions.append(problem.description)

    response = {
        'enemy_hp': enemy.hp,
        'stages_count': len(problems),
        'problem_names': problem_names,
        'problem_descriptions': problem_descriptions
    }

    return response
