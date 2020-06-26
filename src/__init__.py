# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# anki add-on  auto rate typed answer
# Copyright: ijgnd 2019
#            Ankitects Pty Ltd and contributors


import html.parser
import re

from anki.hooks import addHook, wrap
from anki.utils import stripHTML
from aqt.reviewer import Reviewer
from aqt.utils import showInfo, tooltip
from aqt import mw


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    else:
        return fail


def getUserSettingsAndMaybeWarn():
    errormsg = []
    try:
        hardThres = int(gc("hard if shorter than")*1000)
    except:
        hardThres = 12000
        errormsg.append("hard if shorter than")
    try:
        goodThres = int(gc("good if shorter than")*1000)
    except:
        goodThres = 5500
        errormsg.append("good if shorter than")
    try:
        easyThres = int(gc("easy if shorter than")*1000)
    except:
        easyThres = 2000
        errormsg.append("easy if shorter than")
    if errormsg:
        msg = ("""There's a problem in the config of your add-on "auto rate typed """
               """answer". The following settings are missing or have illegal """
               """values in your config:\n- %s\nInstead of your config default values are """
               """applied for this card. Please update your config.""" % "\n- ".join(errormsg))
        showInfo(msg)
    return hardThres, goodThres, easyThres


def getOriginal(self):
    # code is reused from typeAnsAnswerFilter,
    # https://github.com/dae/anki/blob/master/aqt/reviewer.py#L349
    parser = html.parser.HTMLParser()
    cor = self.mw.col.media.strip(self.typeCorrect)
    cor = re.sub("(\n|<br ?/?>|</?div>)+", " ", cor)
    cor = stripHTML(cor)
    # ensure we don't chomp multiple whitespace
    cor = cor.replace(" ", "&nbsp;")
    cor = parser.unescape(cor)
    cor = cor.replace("\xa0", " ")
    cor = cor.strip()
    return cor


def my_defaultEase(self, _old):
    if self.typedAnswer and gc("on mistake set focus on again", False):
        return 1
    else:
        return _old(self)
Reviewer._defaultEase = wrap(Reviewer._defaultEase, my_defaultEase, "around")


def myAutoAnswerCorrect(self):
    if self.typedAnswer:
        correctAns = getOriginal(self)
        given = self.typedAnswer
        if gc("ignore case when comparing", False):
            cond = True if given.lower() == correctAns.lower() else False
        else:
            cond = True if given == correctAns else False
        if cond:
            dur = self.card.timeTaken()
            hardThres, goodThres, easyThres = getUserSettingsAndMaybeWarn()
            cnt = self.mw.col.sched.answerButtons(mw.reviewer.card)  # Get button count
            def helper(ease):
                self._answerCard(ease)
                if gc("show tooltip for confirmation", True):
                    msg = """Last Card rated with "%i" in %.2f seconds.""" % (ease, dur/1000)
                    tooltip(msg)
            if dur < easyThres:
                if cnt == 2:
                    helper(2)
                elif cnt == 3:
                    helper(3)
                else:
                    helper(4)
            elif dur < goodThres:
                if cnt == 2:
                    helper(2)
                elif cnt == 3:
                    helper(2)
                else:
                    helper(3)
            elif dur < hardThres:
                hardIsAgain = gc("hard interval for cards with 2 or 3 buttons means again", True)
                if cnt == 2:
                    if hardIsAgain:
                        helper(1)
                    else:
                        helper(2)
                if cnt == 3:
                    if hardIsAgain:
                        helper(1)
                    else:
                        helper(2)
                else:  # 4 buttons
                    helper(2)
            else:
                helper(1)
Reviewer._showAnswer = wrap(Reviewer._showAnswer, myAutoAnswerCorrect)
