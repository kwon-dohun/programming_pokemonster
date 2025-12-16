# core/battle.py
import random

MAX_HEAL_COUNT = 3
HEAL_RATIO = 0.3
RUN_SUCCESS_RATE = 0.6


def battle(player, enemy):
    print(f"\n야생의 {enemy.name} 이(가) 나타났다!")
    print_status(player, enemy)

    heal_used = 0
    turn = 0  # 0: player, 1: enemy

    while player.is_alive() and enemy.is_alive():
        if turn == 0:
            action = choose_action(heal_used)

            # 1️⃣ 안정 공격 (100%)
            if action == "1":
                damage, mult = player.attack_safe(enemy)
                print_attack(player, enemy, damage, mult)
                turn = 1

            # 2️⃣ 강력 공격 (확률)
            elif action == "2":
                result = player.attack_risky(enemy)

                if result[0] == 0:
                    print("공격을 실패했다!")
                else:
                    damage, mult, kind = result
                    if kind == "critical":
                        print("치명적인 일격!")
                    elif kind == "strong":
                        print("강력한 공격!")
                    print_attack(player, enemy, damage, mult)

                turn = 1

            # 3️⃣ 회복
            elif action == "3":
                if heal_used >= MAX_HEAL_COUNT:
                    print("더 이상 회복할 수 없다!")
                else:
                    heal_amount = int(player.max_hp * HEAL_RATIO)
                    player.hp = min(player.max_hp, player.hp + heal_amount)
                    heal_used += 1
                    print(f"체력을 {heal_amount} 회복했다! ({heal_used}/{MAX_HEAL_COUNT})")
                    turn = 1

            # 4️⃣ 도망
            elif action == "4":
                if random.random() < RUN_SUCCESS_RATE:
                    print("무사히 도망쳤다!")
                    return "run", 0
                else:
                    print("도망에 실패했다!")
                    turn = 1

        else:
            damage, mult = enemy.attack_safe(player)
            print_attack(enemy, player, damage, mult)
            turn = 0

        print_status(player, enemy)

    # ───── 전투 종료 처리 ─────
    if player.is_alive():
        exp = calculate_exp(enemy)
        print(f"\n{enemy.name}을(를) 쓰러뜨렸다!")
        print(f"경험치 {exp} 획득!")
        player.gain_exp(exp)
        return "win", exp
    else:
        print(f"\n{player.name}이(가) 쓰러졌다...")
        return "lose", 0


def choose_action(heal_used):
    print("\n행동을 선택해")
    print("1. 안정 공격 (100%)")
    print("2. 강력 공격 (확률)")
    print(f"3. 회복 ({heal_used}/{MAX_HEAL_COUNT})")
    print("4. 도망")
    return input("선택: ").strip()


def calculate_exp(enemy):
    return 15 + enemy.level * 5


def print_attack(attacker, defender, damage, multiplier):
    msg = f"{attacker.name}의 공격! {defender.name}에게 {damage} 데미지!"
    if multiplier > 1:
        msg += " 효과가 굉장했다!"
    elif multiplier < 1:
        msg += " 효과가 별로였다..."
    print(msg)


def print_status(player, enemy):
    print("\n-------------------------")
    print(f"{player.name} Lv.{player.level}")
    print(f"HP: {player.hp}/{player.max_hp}")
    print("-------------------------")
    print(f"{enemy.name} Lv.{enemy.level}")
    print(f"HP: {enemy.hp}/{enemy.max_hp}")
    print("-------------------------")
