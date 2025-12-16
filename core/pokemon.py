# core/pokemon.py
# 포켓몬 객체 정의 (레벨업, 공격, 진화 처리)

import random
from core.data import get_type_multiplier, EVOLUTIONS


class Pokemon:
    def __init__(self, name, ptype, hp, atk, level=1, exp=0):
        self.name = name
        self.type = ptype
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.level = level
        self.exp = exp

    # ───── 생성 헬퍼 ─────
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            ptype=data["type"],
            hp=data["hp"],
            atk=data["attack"],
            level=data.get("level", 1),
            exp=data.get("exp", 0)
        )

    # ───── 기본 상태 ─────
    def is_alive(self):
        return self.hp > 0

    def heal_full(self):
        self.hp = self.max_hp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    # ───── 공격 로직 ─────
    # 1️⃣ 안정 공격 (100%)
    def attack_safe(self, target):
        multiplier = get_type_multiplier(self.type, target.type)
        damage = int(self.atk * multiplier)
        if damage <= 0:
            damage = 1
        target.take_damage(damage)
        return damage, multiplier

    # 2️⃣ 강력 공격 (확률)
    # 10% : 매우 강함 (x2.0)
    # 50% : 강함 (x1.5)
    # 40% : 실패
    def attack_risky(self, target):
        roll = random.random()
        multiplier = get_type_multiplier(self.type, target.type)

        if roll < 0.10:
            damage = int(self.atk * 2.0 * multiplier)
            kind = "critical"
        elif roll < 0.60:
            damage = int(self.atk * 1.5 * multiplier)
            kind = "strong"
        else:
            return 0, 0, "fail"

        if damage <= 0:
            damage = 1

        target.take_damage(damage)
        return damage, multiplier, kind

    # ───── 경험치 / 레벨 ─────
    def gain_exp(self, amount):
        self.exp += amount
        leveled_up = False

        while self.exp >= self.exp_to_next_level():
            self.exp -= self.exp_to_next_level()
            self.level_up()
            leveled_up = True

        return leveled_up

    def exp_to_next_level(self):
        return 20 + (self.level - 1) * 10

    def level_up(self):
        self.level += 1
        self.max_hp += 3
        self.atk += 1
        self.hp = self.max_hp
        self.check_evolution()

    # ───── 진화 ─────
    def check_evolution(self):
        if self.name in EVOLUTIONS:
            evo = EVOLUTIONS[self.name]
            if self.level >= evo["level"]:
                self.evolve(evo)

    def evolve(self, evo_data):
        self.name = evo_data["evolve_to"]
        self.max_hp += evo_data["bonus_hp"]
        self.atk += evo_data["bonus_atk"]
        self.hp = self.max_hp

    # ───── 정보 출력용 ─────
    def info(self):
        return {
            "name": self.name,
            "type": self.type,
            "level": self.level,
            "hp": f"{self.hp}/{self.max_hp}",
            "atk": self.atk,
            "exp": self.exp
        }
