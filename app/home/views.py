import datetime

from flask import render_template, jsonify, json, request, redirect, url_for, session
from sqlalchemy import desc

from app import db
from app.home.forms import TradeForm
from app.models import Stock, Trade
from app.utils import stockcal
from app.utils.datadump import TradeStats
from . import home

FEES = {'ssi': 0.0025, 'tax': 0.001}
RISK_REWARD = 3


@home.route('/', methods=['GET', 'POST'])
def index():
    models = Stock.query.all()
    dump_stocks = [m.dump() for m in models]

    sold_trades = Trade.query.filter_by(order=0).all()    
    stats = TradeStats(sold_trades).to_dict()

    for s in dump_stocks:
        if s.get('freeroll'):
            s['stop'] = s.get('price') * 1.02
        else:
            s['target'], s['stop'] = stockcal.take_and_stop(s.get('price'), s.get('ratio'), RISK_REWARD)

    form = TradeForm()
    if form.validate_on_submit():
        exist = Stock.query.filter_by(symbol=form.symbol.data.upper()).first()  # type:Stock

        if request.form['action'] == 'BUY':
            # Action: BUY

            # New a trade with buy action
            trade = Trade(
                symbol=form.symbol.data.upper(),
                matched_price=form.price.data,
                net_price=stockcal.net_price(form.price.data, 'buy'),
                shares=form.shares.data,
                order=1,
            ).create()

            if not exist:
                # Create stock if not exists
                Stock(
                    symbol=form.symbol.data.upper(),
                    price=trade.net_price,
                    shares=form.shares.data,
                    ratio=form.profit_margin.data
                ).create()

            else:
                exist.shares = exist.shares + form.shares.data
                # AP = SUM(Pn*Qn)/SUM(Qn)
                exist.price = stockcal.avg_price(exist.price, exist.shares, trade.net_price, trade.shares)
                if form.profit_margin.data:
                    exist.ratio = form.profit_margin.data
                exist.create()
            session['toast'] = '{} has purchased'.format(trade.symbol)
            return redirect(url_for('home.index'))
        elif request.form['action'] == 'SELL':
            # Action: SELL
            # Assert that stock exists and total shares for sale is less than or equal the holding shares
            if not exist:
                form.symbol.errors.append('{} is not holding '.format(form.symbol.data.upper()))

            elif form.shares.data <= exist.shares:
                # New a trade with sell action
                Trade(
                    symbol=form.symbol.data.upper(),
                    matched_price=form.price.data,
                    average_price=exist.price,
                    net_price=stockcal.net_price(form.price.data, 'sell'),
                    shares=form.shares.data,
                    order=0,
                ).create()

                exist.shares = exist.shares - form.shares.data
                if exist.shares > 0:
                    exist.create()
                else:
                    # Delete if holding shares is equal to 0
                    db.session.delete(exist)
                    db.session.commit()
                session['toast'] = '{} has sold'.format(exist.symbol)
                return redirect(url_for('home.index'))
            else:
                form.shares.errors.append('Shares for sale is less than or equal to {}'.format(exist.shares))

    elif request.form.get('name') == 'freeroll':
        # handle Checkbox
        id = request.form.get('value')
        s = Stock.query.get(id)  # type:Stock
        s.freeroll = int(request.form.get('checked')) > 0
        s.create()
        tp, sl = stockcal.take_and_stop(s.price, s.ratio, RISK_REWARD)
        obj = {
            'target-' + id: 'FREE' if s.freeroll else tp,
            'stop-' + id: s.price * 1.02 if s.freeroll else sl
        }
        return jsonify(json.dumps(obj, ensure_ascii=False))
    elif form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)

    return render_template('home/index.html', stocks=dump_stocks, form=form, stats=stats)


@home.route('/history', methods=['GET'])
def history():
    trades = Trade.query.order_by(desc(Trade.date)).all()
    dump_data = [t.dump() for t in trades]
    for t in dump_data:
        t['gross_amount'] = t.get('shares') * t.get('matched_price')
        t['amount'] = t.get('shares') * t.get('net_price')
        t['date'] = datetime.datetime.strptime(t.get('date'), '%Y-%m-%dT%H:%M:%S')
        if t.get('order') == 0:
            t['percent'] = stockcal.profit_percent(t.get('average_price'), t.get('net_price'))
            t['gain_loss'] = t.get('percent') * t.get('average_price') * t.get('shares')
            t['fees'] = t.get('gross_amount') * (FEES['ssi'] + FEES['tax'])
        else:
            t['fees'] = t.get('gross_amount') * FEES['ssi']

    return render_template('home/history.html', trades=dump_data)
