# main.py

from core.data import STARTER_POKEMONS, get_random_enemy, TYPE_POKEDEX
from core.battle import battle
from core.pokemon import Pokemon
from core.player import PlayerState


def choose_starter():
    print("=== 스타터 포켓몬 선택 ===")
    for i, p in enumerate(STARTER_POKEMONS, start=1):
        print(f"{i}. {p['name']} ({p['type']})")
        print(f"   {p['desc']}")
    print()

    while True:
        choice = input("번호 선택: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(STARTER_POKEMONS):
                return Pokemon.from_dict(STARTER_POKEMONS[idx])
        print("잘못된 입력이야.")


def main_menu():
    print("\n=== 메뉴 ===")
    print("1. 야생 포켓몬과 배틀")
    print("2. 내 포켓몬 상태")
    print("3. 도감")
    print("4. 종료")
    return input("선택: ").strip()


def show_pokedex():
    print("\n=== 포켓몬 타입 도감 ===")
    for t, info in TYPE_POKEDEX.items():
        print(f"\n[{t.upper()} 타입]")
        print(info["desc"])

        if info["strong"]:
            print(" - 강함:", ", ".join(info["strong"]))
        if info["weak"]:
            print(" - 약함:", ", ".join(info["weak"]))
        if info["neutral"]:
            print(" - 보통:", ", ".join(info["neutral"]))

    input("\n엔터를 누르면 메뉴로 돌아간다.")


def main():
    print("포켓몬 미니 배틀 게임")
    player = choose_starter()
    state = PlayerState()

    print(f"\n{player.name}을(를) 선택했다!")

    while True:
        choice = main_menu()

        # 1️⃣ 배틀
        if choice == "1":
            if not state.can_battle():
                print(state.empty_life_message())
                continue

            enemy = get_random_enemy(player.level)
            result, _ = battle(player, enemy)

            if result == "lose":
                state.lose_life(1)
                player.heal_full()
                print(f"\n패배했다. 남은 목숨: {state.lives}/5")

            elif result == "run":
                state.lose_life(0.5)
                print(f"\n도망쳤다. 남은 목숨: {state.lives}/5")

        # 2️⃣ 상태 확인 + 회복
        elif choice == "2":
            print("\n=== 내 상태 ===")
            print(f"이름: {player.name}")
            print(f"타입: {player.type}")
            print(f"레벨: {player.level}")
            print(f"HP: {player.hp}/{player.max_hp}")
            print(f"EXP: {player.exp}/{player.exp_to_next_level()}")
            print(f"목숨: {state.lives}/5")
            print(f"알약: {state.pills}/10")

            if state.can_use_pill():
                use = input("알약을 사용해 회복할까? (y/n): ").strip().lower()
                if use == "y":
                    player.heal_full()
                    print("체력이 완전히 회복됐다!")
            else:
                print("오늘 사용할 수 있는 알약을 모두 사용했다.")

        # 3️⃣ 도감
        elif choice == "3":
            show_pokedex()

        # 4️⃣ 종료
        elif choice == "4":
            print("게임 종료")
            break

        else:
            print("잘못된 선택이야.")


if __name__ == "__main__":
    main()
