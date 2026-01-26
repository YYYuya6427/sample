from otree.api import *


doc = """
公共財ゲーム
"""


class C(BaseConstants):
    NAME_IN_URL = 'publicgoods_trial'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 2
    ENDOWMENT = cu(20)
    MULTIPLIER = 1.6


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()



class Player(BasePlayer):
    contribution = models.CurrencyField(
        choices = currency_range(cu(0), cu(C.ENDOWMENT), cu(1)),
        max=C.ENDOWMENT,
        doc="あなたはいくら貢献しますか？",
    )


def compute(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


def creating_session(subsession: Subsession):
    """
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)
    """
    subsession.group_randomly()


# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = ['contribution']


class Page2(WaitPage):
    after_all_players_arrive = compute


class Page3(Page):
    pass


page_sequence = [Page1, Page2, Page3]