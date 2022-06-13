ONLY_FEE = 0.0025
FEE_AND_TAX = 0.0035


class ListUtils:
    @staticmethod
    def average(ls: list):
        return sum(ls) / len(ls)

    @staticmethod
    def max(ls: list):
        max_value = None
        for i in ls:
            if max_value is None or i > max_value:
                max_value = i
        return max_value


def avg_price(old_p, old_q, new_p, new_q):
    # AP = SUM(Pn*Qn)/SUM(Qn)
    return (old_p * old_q + new_p * new_q) / (old_q + new_q)


def net_price(entry, side: str):
    if side.upper() == 'BUY':
        return entry * (1 + ONLY_FEE)
    if side.upper() == 'SELL':
        return entry * (1 - FEE_AND_TAX)


def take_and_stop(entry, percent_diff, risk_reward=2):
    tp = entry * (1 + percent_diff)
    sl = entry * (1 - percent_diff / risk_reward)
    return tp, sl


def profit_percent(entry_p, exit_p):
    return (exit_p - entry_p) / entry_p


def win_rate(num_of_gain, num_of_loss):
    return num_of_gain / (num_of_gain + num_of_loss)
