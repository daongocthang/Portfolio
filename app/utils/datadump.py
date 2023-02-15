from datetime import datetime

from app.utils import stockcal
from app.utils.stockcal import ListUtils


class Tracker:
    class GainLoss:
        def __init__(self, dt: datetime):
            self.sortable = dt.strftime('%Y%m')
            self.month = dt.strftime('%b %Y')
            self.gain = list()
            self.loss = list()

        def add(self, percent):
            if percent > 0:
                self.gain.append(percent)
            else:
                self.loss.append(percent)

        def total_trades(self):
            return len(self.gain) + len(self.loss)

        def win_rate(self):
            return len(self.gain) / self.total_trades()

        def to_dict(self):
            return {
                'sortable': self.sortable,
                'month': self.month,
                'avg_gain': ListUtils.average(self.gain) if len(self.gain) > 0 else 0,
                'avg_loss': abs(ListUtils.average(self.loss)) if len(self.loss) > 0 else 0,
                'win_rate': self.win_rate() if self.total_trades() > 0 else 0,
                'total_trades': self.total_trades(),
                'lg_gain': ListUtils.max(self.gain) if len(self.gain) > 0 else 0,
                'lg_loss': abs(ListUtils.max(self.loss)) if len(self.loss) > 0 else 0
            }

    def __init__(self, trades):
        self.pool = dict()

        for t in trades:
            if t.average_price is None:
                continue
            idx = t.date.strftime('%Y%m')
            gain_loss = self.pool.get(idx) if idx in self.pool.keys() else self.GainLoss(t.date)
            gain_loss.add(stockcal.profit_percent(t.average_price, t.net_price))

            self.pool[idx] = gain_loss

    def to_list(self):
        new_list = [x.to_dict() for x in self.pool.values()]
        return sorted(new_list, key=lambda item: item['sortable'])


class TradeStats:
    class Holder:
        count = 0
        gross_entry = 0
        gross_exit = 0
        largest = 0

        def append(self, g_entry, g_exit):
            self.gross_entry += g_entry
            self.gross_exit += g_exit
            self.count += 1
            profit = abs(g_exit - g_entry)
            if profit > self.largest:
                self.largest = profit

        def to_dict(self):
            return {
                'profit': abs(self.gross_exit - self.gross_entry),
                'largest': self.largest,
                'rate': abs(stockcal.profit_percent(self.gross_entry, self.gross_exit)) if self.count > 0 else 0,
                'count': self.count
            }       

    def __init__(self, trades):
        self.gain = self.Holder()
        self.loss = self.Holder()
        self.win_rate = 0

        for t in trades:
            if t.average_price is None:
                continue
            rate = stockcal.profit_percent(t.average_price, t.net_price)
            if rate > 0:
                self.gain.append(t.average_price * t.shares, t.net_price * t.shares)
            else:
                self.loss.append(t.average_price * t.shares, t.net_price * t.shares)
        
        if any([self.gain.count > 0, self.loss.count > 0]):
            self.win_rate = stockcal.win_rate(self.gain.count, self.loss.count)
            

    def to_dict(self):
        return {
            'gain': self.gain.to_dict(),
            'loss': self.loss.to_dict(),
            'win_rate': self.win_rate,
            'num_of_trades': self.gain.count + self.loss.count
        }
