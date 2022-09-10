from HeroCode.models import Enemies
from HeroCode.models import Problems
from HeroCode.models import Tests


def get_enemy(enemy_id: int) -> Enemies:
    return Enemies.get(id=enemy_id)


def get_problems(enemy_id: int) -> list[Problems]:
    return Problems.get(enemy_id=enemy_id)


def get_tests(problem_id: int) -> list[Tests]:
    return Tests.get(problem_id=problem_id)
