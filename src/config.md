for a description see [on ankiweb](https://ankiweb.net/shared/info/1836029849).

About `accept_multiple_answers_for_these_notetypes`. This might be useful if you have vocabulary 
words with multiple similar definitions. E.g. you have a note type named 
"Basic, modified" to which you added additional fields. The add-on by default compares
the text you typed in with the field that's in your front template where you have e.g.
`{{type::Back}}`. If you want to additionally compare against fields named like 
"alternative 1" and "another alternative" you would have to put this into your config:

    "accept_multiple_answers_for_these_notetypes": {
        "Basic, modified": ["alternative 1", "another alternative"]
    }
