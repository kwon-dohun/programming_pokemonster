# core/player.py
import time
import datetime

MAX_LIVES = 5
LIFE_RECOVER_INTERVAL = 60 * 60      # 1시간
EMPTY_LIFE_WAIT = 30 * 60            # 30분

MAX_PILLS_PER_DAY = 10


class PlayerState:
    def __init__(self):
        # 목숨 (0.5 단위 허용)
        self.lives = float(MAX_LIVES)
        self.last_update = time.time()

        # 알약
        self.pills = MAX_PILLS_PER_DAY
        self.last_pill_day = datetime.date.today()

    # ───── 목숨 관리 ─────
    def update_lives(self):
        now = time.time()
        elapsed = now - self.last_update

        recovered = int(elapsed // LIFE_RECOVER_INTERVAL)
        if recovered > 0:
            self.lives = min(MAX_LIVES, self.lives + recovered)
            self.last_update += recovered * LIFE_RECOVER_INTERVAL

    def lose_life(self, amount):
        self.update_lives()
        self.lives = max(0, self.lives - amount)

    def can_battle(self):
        self.update_lives()
        return self.lives > 0

    def empty_life_message(self):
        now = time.time()
        remain = EMPTY_LIFE_WAIT - (now - self.last_update)
        if remain < 0:
            remain = 0
        m = int(remain // 60)
        s = int(remain % 60)
        return f"회복 중입니다. {m}분 {s}초 후 다시 시도하세요."

    # ───── 알약 관리 ─────
    def update_pills(self):
        today = datetime.date.today()
        if today != self.last_pill_day:
            self.pills = MAX_PILLS_PER_DAY
            self.last_pill_day = today

    def can_use_pill(self):
        self.update_pills()
        return self.pills > 0

    def use_pill(self):
        self.update_pills()
        if self.pills > 0:
            self.pills -= 1
            return True
        return False
