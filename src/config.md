for a description see [on ankiweb](https://ankiweb.net/shared/info/1836029849).

Anki and this add-on compare the text you typed in with the field that's in your front template 
where you have e.g. `{{type::Back}}`. But for some questions two answers are equally good, e.g.
if you have vocabulary words with multiple similar definitions. In this case the setting 
`accept_multiple_answers_for_these_notetypes` might be useful.

The best way to show this is with an example.

The following section is only understandable if you know about the difference between "notes" and 
"cards" in Anki. If not, check the manual or see e.g. 
[here](https://www.reddit.com/r/Anki/comments/9elfd8/what_is_the_different_between_bury_a_card_and_a/e5pqgqv/) 
or [here](https://www.reddit.com/r/Anki/comments/8w2b5e/the_fundamental_principle_of_anki_card_creation/).

E.g. you have a note type named "Basic (type in the answer)" to which you added an addtional field
named "my alternative answer". This note type generates only one card based on the card template 
named "Card 1". For this you want that Anki accepts also the content of "my alternative answer" 
as a correct answer. So you would set the config as follows:

    "accept_multiple_answers_for_these_notetypes": {
        "Basic (type in the answer)": {
            "Card 1": ["my alternative answer"]
        }
    },

P.S.: To find out the name of a card template go to the Card Layout window and in the upper right
click the button "Options", then select "Rename Card Type ..". Then a new window opens where you
see the card type name.
