from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import data_required, optional

from app.utils.wtf_utils import InlineButtonWidget


class TradeForm(FlaskForm):
    symbol = StringField('Symbol', validators=[data_required()], render_kw={'placeholder': 'Symbol'})
    price = FloatField('Price', validators=[data_required()], render_kw={'placeholder': 'Price'})
    shares = FloatField('Shares', validators=[data_required()], render_kw={'placeholder': 'Shares'})
    profit_margin = FloatField('Profit Margin', validators=[optional()],
                               render_kw={'placeholder': 'Profit Margin'})

    bt_sell = SubmitField('SELL', widget=InlineButtonWidget(class_="btn btn-danger pull-right"),
                          render_kw={'name': 'action', 'style': 'margin-left : 8px;'})
    bt_buy = SubmitField('BUY', widget=InlineButtonWidget(class_="btn btn-success pull-right"),
                         render_kw={'name': 'action'})
