from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ultimatum_trial'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    ENDOWMENT = cu(10)
    #instructions_template = 'ultimatum_trial/Instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    proposal = models.CurrencyField(
        choices = currency_range(cu(0), C.ENDOWMENT, cu(1)),
        label = 'プレイヤー2にいくら渡しますか？',
        initial = cu(0)
    )
    accepted_or_not = models.BooleanField(
        label = 'あなたは提案を受け入れますか？',
        initial = False
    )
    Page2timeout = models.IntegerField()
    Page4timeout = models.IntegerField()


class Player(BasePlayer):
    pass


def compute(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.accepted_or_not == True:
        p1.payoff = C.ENDOWMENT - group.proposal
        p2.payoff = group.proposal
    else:
        p1.payoff = cu(0)
        p2.payoff = cu(0)


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
    def is_displayed(player):
        # 現在のラウンドが1の場合のみ True を返す
        return player.round_number == 1

class Page2(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['proposal']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.proposal = cu(0)
            player.group.Page2timeout = 1

class Page3(WaitPage):
    pass


class Page4(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['accepted_or_not']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.accepted_or_not = False
            player.group.Page4timeout = 1


class Page5(WaitPage):
    after_all_players_arrive = compute


class Page6(Page):
    pass


page_sequence = [Page1, Page2, Page3, Page4, Page5, Page6]