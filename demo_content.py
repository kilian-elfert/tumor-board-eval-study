"""Content for the demo pages (one per rating step).

Each page is shown as click-through slides in a modal
(``/demo/<key>/folien``, ``templates/demo_slides.html``).

Each entry in ``DEMO_PAGES`` is keyed by the ``key`` of a step in
``RATING_STEPS`` (app.py). Chapter *i* drives scene *i* of the stage partial
``templates/demo/stage_<stage>.html``; keep chapter order and scene numbers in
sync when editing.

Chapter ``kind``:
    'ui'  – how to operate the interface ("Bedienung")
    'why' – rationale behind the rating ("Hintergrund")

Chapter texts are trusted HTML. ``{guideline_url}`` is replaced at render time.
"""


# The relevance rating is not part of RATING_STEPS (it happens on the patient
# dashboard), so its demo page gets a step-like descriptor of its own.
RELEVANCE_STEP = {
    'key': 'case_relevance',
    'section': 'Patientenakte',
    'subtitle': 'Relevanzbewertung',
    'has_tabs': False,
    'section_type': 'both',
    'alert': 'Welche Informationen der Patientenakte halten Sie für die '
             'Tumorboardanmeldung dieses Patienten für klinisch relevant?',
}

# Tour of the patient record itself (body map, imaging reports, original
# texts); opened from the "Demo: Patientenakte" button next to the record tabs.
RECORD_STEP = {
    'key': 'case_record',
    'section': 'Patientenakte',
    'subtitle': 'Aufbau und Originalbefunde',
    'has_tabs': False,
    'section_type': 'both',
    'alert': 'Wo finden Sie welche Informationen in der Patientenakte, und wie '
             'öffnen Sie die Originalbefunde?',
}


def _vas_page(criterion, definition_title, definition_text,
              icon, takeaways):
    return {
        'stage': 'vas',
        'icon': icon,
        'chapters': [
            {'kind': 'ui', 'title': 'Text lesen',
             'text': 'Lesen Sie die Zusammenfassung im linken Bereich. Rechts '
                     'finden Sie eine <strong>Skala von 0 bis 100</strong> – zu '
                     'Beginn ist noch kein Wert gesetzt.'},
            {'kind': 'why', 'title': definition_title, 'text': definition_text},
            {'kind': 'ui', 'title': 'Wert setzen',
             'text': 'Klicken Sie auf die Stelle der Skala, die Ihrem Urteil '
                     'entspricht. Eine Markierung zeigt Ihre Position. Einen '
                     'Zahlenwert sehen Sie bewusst nicht – maßgeblich ist Ihr '
                     'Gesamteindruck.'},
            {'kind': 'why', 'title': 'Bewusst ohne Abschnitte',
             'text': 'Beschriftet sind nur die beiden Endpunkte '
                     '<em>Sehr schlecht</em> und <em>Ausgezeichnet</em>. '
                     'Dazwischen gibt es bewusst <strong>keine Kategorien oder '
                     'Abschnitte</strong>: Setzen Sie die Markierung stufenlos '
                     'an die Stelle, die Ihrem Gesamteindruck entspricht.'},
            {'kind': 'ui', 'title': 'Korrigieren und weiter',
             'text': 'Ein erneuter Klick (oder Ziehen) verschiebt die Markierung. '
                     'Mit <strong>Weiter zu Version B</strong> wird Ihr Wert '
                     'gespeichert.'},
            {'kind': 'why', 'title': 'Jede Version für sich',
             'text': 'Version A und B bewerten Sie <strong>nacheinander und '
                     'unabhängig</strong>; für Version B startet die Skala wieder '
                     'leer. Den direkten Vergleich beider Versionen erfassen wir '
                     'erst im Schritt <em>Präferenz</em>.'},
        ],
        'takeaways': takeaways,
        'criterion': criterion,
    }


def _postedit_page(section_word, effort_text):
    return {
        'stage': 'postedit',
        'icon': 'clock',
        'chapters': [
            {'kind': 'ui', 'title': 'Text lesen',
             'text': f'Links steht die {section_word}, rechts zwei Karten: '
                     '<strong>Direkt verwenden</strong> oder '
                     '<strong>Überarbeitung nötig</strong>.'},
            {'kind': 'why', 'title': 'Praxistauglichkeit messen',
             'text': 'Ein Text kann gut klingen und trotzdem Nacharbeit '
                     'erfordern. Der geschätzte <strong>Überarbeitungsaufwand'
                     '</strong> zeigt, wie viel Zeit eine Unterstützung im '
                     'klinischen Alltag tatsächlich sparen würde.'},
            {'kind': 'ui', 'title': 'Ohne Änderungen nutzbar?',
             'text': 'Würden Sie den Text unverändert für die Tumorboardanmeldung '
                     'übernehmen, wählen Sie <strong>Direkt verwenden</strong>. '
                     'Eine Bestätigung erscheint darunter.'},
            {'kind': 'ui', 'title': 'Überarbeitung nötig',
             'text': 'Müssten Sie etwas ändern, wählen Sie <strong>Überarbeitung '
                     'nötig</strong>. Darunter öffnet sich eine zweite Ebene.'},
            {'kind': 'ui', 'title': 'Aufwand schätzen', 'text': effort_text},
            {'kind': 'why', 'title': 'Warum grobe Zeitkategorien?',
             'text': 'Exakte Minuten lassen sich kaum zuverlässig schätzen – '
                     'grobe Kategorien schon. Sie trennen klar zwischen '
                     '<em>kurz nachbessern</em> und <em>lohnt sich nicht, neu '
                     'schreiben</em>.'},
        ],
        'takeaways': [
            {'title': 'Erst entscheiden, dann schätzen', 'text': 'Zuerst wählen '
             'Sie, ob eine Überarbeitung nötig ist. Nur dann schätzen Sie den '
             'Aufwand.'},
            {'title': 'Ihr Maßstab', 'text': 'Entscheidend ist, ob Sie den Text '
             'so für die Tumorboardanmeldung verwenden würden.'},
            {'title': 'Zeit statt Note', 'text': 'Der geschätzte Aufwand zeigt '
             'den praktischen Nutzen und macht die Versionen vergleichbar.'},
        ],
    }


def _origin_page(section_word):
    return {
        'stage': 'origin',
        'icon': 'origin',
        'chapters': [
            {'kind': 'ui', 'title': 'Text lesen',
             'text': f'Lesen Sie die {section_word} und geben Sie an, von wem '
                     'sie Ihrer Einschätzung nach verfasst wurde.'},
            {'kind': 'why', 'title': 'Grundlage Ihrer Einschätzung',
             'text': 'Maßgeblich ist der <strong>Eindruck, den der Text beim '
                     'Lesen</strong> auf Sie macht. Weitere Informationen sind '
                     'für diese Einschätzung nicht erforderlich.'},
            {'kind': 'ui', 'title': 'Einschätzung wählen',
             'text': 'Klicken Sie auf <strong>Mensch</strong>, '
                     '<strong>Unsicher</strong> oder <strong>KI</strong>. Die '
                     'gewählte Option wird hervorgehoben und lässt sich jederzeit '
                     'ändern.'},
            {'kind': 'why', 'title': '„Unsicher“ als Antwortoption',
             'text': 'Gefragt ist Ihre subjektive Einschätzung der Herkunft. '
                     'Lässt sich die Herkunft aus dem Text für Sie nicht '
                     'eindeutig ableiten, wählen Sie <strong>Unsicher</strong>. '
                     'Diese Antwort ist ausdrücklich vorgesehen.'},
            {'kind': 'ui', 'title': 'Jede Version einzeln',
             'text': 'Beurteilen Sie Version A und B jeweils für sich und '
                     'allein anhand des Textes.'},
        ],
        'takeaways': [
            {'title': 'Nur der Text zählt', 'text': 'Urteilen Sie allein aus '
             'Ihrem Leseeindruck.'},
            {'title': '„Unsicher“ vorgesehen', 'text': 'Ist die Herkunft für '
             'Sie nicht eindeutig, wählen Sie „Unsicher“.'},
            {'title': 'Jede Version einzeln', 'text': 'Beurteilen Sie Version A '
             'und B jeweils für sich.'},
        ],
    }


def _preference_page(section_word):
    return {
        'stage': 'preference',
        'icon': 'scale',
        'chapters': [
            {'kind': 'ui', 'title': 'Beide Versionen nebeneinander',
             'text': f'Erstmals sehen Sie beide Versionen der {section_word} '
                     '<strong>nebeneinander</strong>. Voreingestellt ist '
                     '<strong>Keine Präferenz</strong>.'},
            {'kind': 'why', 'title': 'Warum ein direkter Vergleich?',
             'text': 'Die vorherigen Schritte erfassen jeweils einen Aspekt. Der '
                     'direkte Vergleich bündelt alles zu einem '
                     '<strong>Gesamturteil</strong> – so, wie Sie im Alltag '
                     'zwischen zwei Entwürfen wählen würden.'},
            {'kind': 'ui', 'title': 'Version wählen',
             'text': 'Klicken Sie auf die Spalte der bevorzugten Version. Sie '
                     'wird blau umrandet und mit einem Waagen-Symbol markiert.'},
            {'kind': 'ui', 'title': 'Umentscheiden',
             'text': 'Ein Klick auf die andere Spalte ändert die Auswahl. Ein '
                     'erneuter Klick auf die bereits gewählte Version hebt die '
                     'Auswahl wieder auf – dann gilt <em>Keine Präferenz</em>.'},
            {'kind': 'ui', 'title': 'Gleichwertig?',
             'text': 'Halten Sie beide Versionen für gleichwertig, klicken Sie '
                     'auf <strong>Keine Präferenz</strong> in der Mitte.'},
            {'kind': 'why', 'title': 'Worauf es ankommt',
             'text': 'Entscheidend ist, welche Version Sie für den '
                     '<strong>klinischen Einsatz</strong> – die Anmeldung im '
                     'Tumorboard – bevorzugen würden. Wägen Sie alles ab, was '
                     'Ihnen wichtig ist: Richtigkeit, Vollständigkeit, Kürze und '
                     'Aufwand.'},
        ],
        'takeaways': [
            {'title': 'Seite an Seite', 'text': 'Nur hier sehen Sie beide '
             'Versionen gleichzeitig.'},
            {'title': 'Gesamturteil', 'text': 'Alle Aspekte zusammen – so wie '
             'bei einer echten Entscheidung.'},
            {'title': 'Neutral möglich', 'text': '„Keine Präferenz“ ist '
             'voreingestellt und eine gültige Wahl.'},
        ],
    }


DEMO_PAGES = {
    # ── Patientenakte (once per case, before the rating steps) ───────────────
    'case_relevance': {
        'stage': 'relevance',
        'icon': 'record',
        'chapters': [
            {'kind': 'ui', 'title': 'Die Patientenakte',
             'text': 'Beim ersten Öffnen eines Falls erscheint die '
                     '<strong>Patientenakte</strong> mit allen Falldaten – '
                     'Übersicht, Verlauf, Laborwerte und Bildgebung – und eine '
                     'kurze Einführung zur Relevanzbewertung.'},
            {'kind': 'ui', 'title': 'Sidebar öffnen',
             'text': 'Mit <strong>Verstanden. Zur Relevanzbewertung →</strong> '
                     'fährt rechts die Sidebar heraus. Später öffnen und '
                     'schließen Sie sie über den blauen Reiter '
                     '<strong>„Relevanz“</strong>.'},
            {'kind': 'ui', 'title': 'Pro Information entscheiden',
             'text': 'Markieren Sie jede Information als <span class="rel-intro-pill '
                     'rel-intro-pill--yes">✓ relevant</span> oder <span '
                     'class="rel-intro-pill rel-intro-pill--no">✗ nicht relevant'
                     '</span> für die '
                     'Tumorboardanmeldung dieses Patienten. Markieren Sie nur, '
                     'was Sie für die Anmeldung <strong>'
                     'tatsächlich benötigen</strong>. Der Zähler oben '
                     'läuft mit; gespeichert wird automatisch.'},
            {'kind': 'ui', 'title': 'Ganze Kategorien bewerten',
             'text': 'Mit <span class="rel-intro-pill rel-intro-pill--yes">'
                     'alle&nbsp;✓</span> bzw. <span class="rel-intro-pill '
                     'rel-intro-pill--no">alle&nbsp;✗</span> neben einer '
                     'Kategorie markieren Sie alle Punkte dieser Kategorie in '
                     'einem Schritt.'},
            {'kind': 'ui', 'title': 'Ausnahmen anpassen',
             'text': 'Danach korrigieren Sie einzelne Ausnahmen direkt in der '
                     'Zeile – hier etwa eine Angabe, die für diesen Fall keine '
                     'Rolle spielt.'},
            {'kind': 'ui', 'title': 'Sidebar jederzeit schließen',
             'text': 'Sie müssen nicht alles in einem Zug bewerten. Über '
                     '<strong>✕</strong> oder den Reiter <strong>„Relevanz“'
                     '</strong> schließen Sie die Sidebar jederzeit – etwa um '
                     'die Patientenakte in Ruhe zu lesen oder in Verlauf, '
                     'Laborwerten und Bildgebung nachzusehen. Der Reiter zeigt '
                     'weiterhin Ihren Fortschritt.'},
            {'kind': 'ui', 'title': 'Später fortsetzen',
             'text': 'Ihre Angaben werden laufend gespeichert. Öffnen Sie die '
                     'Sidebar über den Reiter <strong>„Relevanz“</strong> '
                     'wieder, sind alle bisherigen Markierungen erhalten und Sie '
                     'machen dort weiter, wo Sie aufgehört haben.'},
            {'kind': 'why', 'title': 'Sie legen die Referenz fest',
             'text': 'Was für eine Tumorboardanmeldung relevant ist, hängt vom jeweiligen '
                     'Fall und von Ihrer ärztlichen Einschätzung ab. Ihre Auswahl '
                     'bestimmt, welche Informationen bei der Auswertung berücksichtigt werden.'},
            {'kind': 'why', 'title': 'Maßgeblich ist die Patientenakte',
             'text': 'Die Patientenakte – Übersicht sowie Verlauf, Laborwerte '
                     'und Bildgebung – enthält <strong>alle</strong> '
                     'Informationen aus den Originalunterlagen. Ist etwa keine '
                     'Therapie aufgeführt, ist keine erfolgt bzw. keine '
                     'dokumentiert. Bewerten Sie allein anhand der Patientenakte. Die zu '
                     'bewertenden Texte sehen Sie erst danach – so bleibt Ihre '
                     'Relevanzeinschätzung unabhängig von den zu bewertenden Textversionen.'},
            {'kind': 'ui', 'title': 'Weiter zur Textbewertung',
             'text': 'Erst wenn <strong>alle</strong> Informationen bewertet '
                     'sind, wird <strong>Weiter zur Textbewertung</strong> '
                     'direkt unter dem Fortschrittsbalken in der Sidebar '
                     'freigeschaltet. Bis dahin zeigt ein Hinweis, wie viele '
                     'Informationen noch offen sind. Die Relevanzbewertung erfolgt einmal pro '
                     'Fall. Die Patientenakte kann später jederzeit wieder eingesehen werden.'},
        ],
        'takeaways': [
            {'title': 'Einmal pro Fall', 'text': 'Vor der Textbewertung, in der '
             'Sidebar „Relevanz“. Sie können jederzeit pausieren und später '
             'weitermachen.'},
            {'title': 'Ihre Auswahl ist der Maßstab', 'text': 'Was Sie als '
             'relevant markieren, bestimmt, woran die Texte später gemessen '
             'werden.'},
            {'title': 'Grundlage ist die Akte', 'text': 'Sie enthält alle '
             'Informationen. Bewerten Sie unabhängig von den Texten.'},
        ],
    },

    # ── Patientenakte: Aufbau und Originalbefunde ───────────────────────────
    'case_record': {
        'stage': 'record',
        'icon': 'record',
        'chapters': [
            {'kind': 'ui', 'title': 'Aufbau der Patientenakte',
             'text': 'Die Patientenakte ist in vier Reiter gegliedert: '
                     '<strong>Übersicht</strong>, <strong>Verlauf</strong>, '
                     '<strong>Laborwerte</strong> und <strong>Bildgebung</strong>. '
                     'Während der Textbewertung öffnen Sie sie jederzeit über die '
                     'Schaltfläche <strong>Patientenakte</strong>.'},
            {'kind': 'ui', 'title': 'Die Körperkarte',
             'text': 'Fahren Sie mit der Maus über einen Punkt der Körperkarte: '
                     'Die zugehörigen Einträge in den Listen werden hervorgehoben, '
                     'und ein Hinweisfeld fasst die Befunde zu dieser Region '
                     'zusammen. Die Legende rechts erklärt die Farben.'},
            {'kind': 'ui', 'title': 'Originalbefunde in der „Übersicht“',
             'text': 'Unter <strong>Bildgebung</strong> öffnet <strong>TXT</strong> '
                     'neben einem Eintrag den Originalbefund als Text, '
                     '<strong>PDF</strong> – sofern vorhanden – das '
                     'Originaldokument.'},
            {'kind': 'ui', 'title': 'Originaltext im Kurzverlauf',
             'text': 'Die Einträge im Kurzverlauf sind Zusammenfassungen. Mit '
                     '<strong>Originaltext anzeigen</strong> sehen Sie den '
                     'zugrunde liegenden Eintrag aus den Originalunterlagen.'},
            {'kind': 'ui', 'title': 'Der Reiter „Verlauf“',
             'text': 'Der Reiter <strong>Verlauf</strong> enthält die vollständige '
                     'Verlaufsdokumentation: jeden Eintrag im Wortlaut der '
                     'Originalunterlagen, chronologisch geordnet. Sie können nach '
                     'Jahr, Stichwort und Kategorie filtern.'},
            {'kind': 'ui', 'title': 'Der Reiter „Laborwerte“',
             'text': 'Der Reiter <strong>Laborwerte</strong> zeigt jeden Marker als '
                     'Verlaufsdiagramm mit Referenzbereich. Die Kategorien darüber '
                     'filtern die Anzeige; <strong>⚠</strong> kennzeichnet '
                     'Kategorien mit auffälligen Werten.'},
            {'kind': 'ui', 'title': '„Laborwerte“ als Tabelle',
             'text': 'Über <strong>Tabelle</strong> sehen Sie alle Werte mit '
                     'Einheit und Referenzbereich; auffällige Werte sind markiert. '
                     'Mit <strong>Nur auffällige Werte anzeigen</strong> blenden '
                     'Sie unauffällige Werte aus.'},
            {'kind': 'ui', 'title': 'Der Reiter „Bildgebung“',
             'text': 'Der Reiter <strong>Bildgebung</strong> zeigt alle '
                     'bildgebenden Befunde nach Körperregion und Datum, jeweils mit '
                     'Zusammenfassung und Beurteilung.'},
            {'kind': 'ui', 'title': 'Originalbefunde im Reiter „Bildgebung“',
             'text': 'Auch hier öffnet <strong>TXT</strong> bzw. <strong>PDF'
                     '</strong> den vollständigen Originalbefund.'},
            {'kind': 'why', 'title': 'Die Akte ist vollständig',
             'text': 'Die Patientenakte enthält <strong>alle</strong> '
                     'Informationen aus den Originalunterlagen. Ist eine Angabe '
                     'nicht aufgeführt oder als <em>Nicht dokumentiert</em> '
                     'gekennzeichnet, ist sie in den Unterlagen nicht enthalten.'},
        ],
        'takeaways': [
            {'title': 'Vier Reiter', 'text': 'Übersicht, Verlauf, Laborwerte und '
             'Bildgebung enthalten alle Informationen des Falls.'},
            {'title': 'Originale abrufbar', 'text': 'Über TXT, PDF und '
             '„Originaltext anzeigen“ sehen Sie die Originalunterlagen.'},
            {'title': 'Vollständig', 'text': 'Was nicht aufgeführt ist, ist in den '
             'Unterlagen nicht dokumentiert.'},
        ],
    },

    # ── Zusammenfassung ──────────────────────────────────────────────────────
    'summary_falseinfo': {
        'stage': 'falseinfo',
        'icon': 'alert',
        'chapters': [
            {'kind': 'ui', 'title': 'Die Ausgangslage',
             'text': 'Links sehen Sie die Zusammenfassung, rechts die Angaben, die '
                     'das Studienteam als <strong>inhaltlich falsch oder '
                     'irreführend</strong> markiert hat. Die betroffenen '
                     'Textstellen sind <strong>rot hervorgehoben</strong>.'},
            {'kind': 'why', 'title': 'Keine Fehlersuche',
             'text': 'Die Fehler wurden vom Studienteam bereits annotiert. '
                     'Ihre Aufgabe ist es, ihre '
                     'möglichen <strong>klinischen Folgen</strong> einzuschätzen. '
                     'So kommt Ihre Expertise genau dort zum Tragen, wo sie am meisten zählt.'},
            {'kind': 'ui', 'title': 'Mit den Falldaten abgleichen',
             'text': 'Fahren Sie mit der Maus über eine markierte Textstelle: Der '
                     'zugehörige Eintrag rechts wird hervorgehoben. Das '
                     'funktioniert auch umgekehrt über den aufklappbaren Eintrag '
                     'rechts. Enthält die Patientenakte Angaben dazu, erscheint '
                     'neben dem Mauszeiger ein Hinweisfeld mit diesen <strong>'
                     'Angaben aus der Patientenakte</strong>. Erscheint kein '
                     'Hinweisfeld, gibt es dazu in den Quelldokumenten keine '
                     'Angabe.'},
            {'kind': 'ui', 'title': 'Eintrag öffnen',
             'text': 'Ein Klick klappt den Eintrag auf. Oben steht die '
                     '<strong>Begründung des Studienteams</strong> mit der '
                     'zugeordneten Fehlerkategorie, z. B. <em>Inhaltlich</em> oder '
                     '<em>Logisch/medizinisch</em>.'},
            {'kind': 'ui', 'title': 'Schwere des Schadens',
             'text': 'Wählen Sie über die Ampel, welche <strong>Folgen</strong> ein Fehler für <strong>Patientenwohl und Patientensicherheit</strong> haben könnte, wenn der Fehler unbemerkt bliebe und das Tumorboard auf Basis dieser Angabe entscheiden würde. '
                     'Ist mit <strong>keinem Schaden</strong>, einem <strong>leichten Schaden</strong> '
                     'oder einem <strong>schweren Schaden</strong> zu rechnen?'},
            {'kind': 'ui', 'title': 'Eintrittswahrscheinlichkeit',
             'text': 'Schätzen Sie, wie <strong>wahrscheinlich</strong> es ist, dass dieser '
                     'Fehler in der Praxis unbemerkt bleibt und der Schaden tatsächlich eintritt: '
                     'Ist die Wahrscheinlichkeit eher <strong>gering</strong>, <strong>moderat</strong> oder <strong>hoch</strong>?'},
            {'kind': 'why', 'title': 'Warum zwei Ampeln?',
             'text': 'Schwere und Wahrscheinlichkeit ergeben zusammen das '
                     '<strong>klinische Risiko</strong>. Ein schwerwiegender Fehler, der selten unbemerkt bleibt, wiegt anders als ein leichter Fehler, der häufig unbemerkt bleibt. '
                     'Nur wenn diese Dimensionen kombiniert werden, lässt sich das klinische Risiko präzise bewerten.'},
        ],
        'takeaways': [
            {'title': 'Vorab markiert', 'text': 'Das Studienteam hat die Fehler '
             'annotiert – Sie bewerten ausschließlich deren Folgen.'},
            {'title': 'Zwei Dimensionen', 'text': 'Schwere und '
             'Eintrittswahrscheinlichkeit getrennt einschätzen.'},
            {'title': 'Patientenakte als Referenz', 'text': 'Beim Überfahren mit dem Mauszeiger '
             'werden die zugehörigen Falldaten eingeblendet.'},
        ],
    },

    'summary_missinginfo': {
        'stage': 'missinginfo',
        'icon': 'gap',
        'chapters': [
            {'kind': 'ui', 'title': 'Die Ausgangslage',
             'text': 'Rechts sehen Sie die Informationen, die in dieser Version '
                     '<strong>fehlen</strong>, obwohl sie für den Fall relevant '
                     'sind. Der erste Eintrag ist bereits aufgeklappt.'},
            {'kind': 'why', 'title': 'Ihre Relevanzbewertung zählt',
             'text': 'Was als relevant gilt, haben <strong>Sie selbst</strong> zu '
                     'Beginn des Falls in der Relevanzbewertung der Patientenakte '
                     'festgelegt. Was Sie dort als <span class="rel-intro-pill '
                     'rel-intro-pill--no">✗ nicht relevant</span> markiert '
                     'haben, wird hier nicht abgefragt.'},
            {'kind': 'ui', 'title': 'Nur relevante Informationen',
             'text': 'Die Liste enthält daher nur Informationen, die das '
                     'Studienteam als <em>nicht enthalten</em> annotiert hat '
                     '<strong>und</strong> die Sie als <span class="rel-intro-pill '
                     'rel-intro-pill--yes">✓ relevant</span> bewertet '
                     'haben.'},
            {'kind': 'ui', 'title': 'Schwere des Schadens',
             'text': 'Wählen Sie über die Ampel, welche <strong>Folgen</strong> '
                     'das Fehlen der Information für <strong>Patientenwohl und '
                     'Patientensicherheit</strong> haben könnte, wenn es unbemerkt '
                     'bliebe und das Tumorboard ohne diese Information entscheiden '
                     'würde. Ist mit <strong>keinem Schaden</strong>, einem '
                     '<strong>leichten Schaden</strong> oder einem <strong>schweren '
                     'Schaden</strong> zu rechnen?'},
            {'kind': 'ui', 'title': 'Eintrittswahrscheinlichkeit',
             'text': 'Schätzen Sie, wie <strong>wahrscheinlich</strong> es ist, dass '
                     'das Fehlen der Information in der Praxis unbemerkt bleibt und '
                     'der Schaden tatsächlich eintritt: Ist die Wahrscheinlichkeit '
                     'eher <strong>gering</strong>, <strong>moderat</strong> oder '
                     '<strong>hoch</strong>? Sind beide Ampeln gesetzt, wird der '
                     'Eintrag als <em>Fertig</em> markiert, und der nächste öffnet sich.'},
            {'kind': 'why', 'title': 'Gleicher Maßstab wie bei Fehlern',
             'text': 'Fehlende und falsche Angaben werden mit <strong>derselben '
                     'Skala</strong> bewertet. So lassen sich beide Fehlerarten '
                     'direkt vergleichen – und es wird sichtbar, ob eine Version '
                     'eher durch fehlende oder durch falsche Informationen auffällt.'},
        ],
        'takeaways': [
            {'title': 'Ihre Relevanzbewertung zählt', 'text': 'Abgefragt wird '
             'nur, was Sie als relevant markiert haben.'},
            {'title': 'Folgen statt Anzahl', 'text': 'Entscheidend ist das '
             'Risiko, nicht die Zahl der fehlenden Informationen.'},
            {'title': 'Gleicher Maßstab', 'text': 'Sie bewerten mit denselben '
             'Ampeln wie bei Falschinformationen.'},
        ],
    },

    'summary_correctness': _vas_page(
        criterion='correctness',
        definition_title='Was bedeutet Korrektheit?',
        definition_text='Bewertet wird, ob die <strong>enthaltenen</strong> '
                        'Informationen medizinisch korrekt und frei von '
                        'Ungenauigkeiten sind. Unter der Skala sehen Sie zur '
                        'Orientierung die vom Studienteam markierten '
                        '<strong>Falschinformationen</strong> samt Begründung – '
                        'Ihr Urteil bleibt aber eine Gesamteinschätzung.',
        icon='check',
        takeaways=[
            {'title': 'Nur Enthaltenes', 'text': 'Fehlende Informationen zählen '
             'bei der Vollständigkeit, nicht hier.'},
            {'title': 'Orientierungshilfe', 'text': 'Die markierten '
             'Falschinformationen stehen unter der Skala.'},
            {'title': 'Stufenlos', 'text': 'Nur die Endpunkte sind beschriftet. '
             'Dazwischen setzen Sie Ihren Wert frei.'},
        ],
    ),
    'summary_completeness': _vas_page(
        criterion='completeness',
        definition_title='Was bedeutet Vollständigkeit?',
        definition_text='Bewertet wird, wie vollständig die Zusammenfassung '
                        'alle <strong>klinisch relevanten</strong> Informationen '
                        'abbildet. Zur Orientierung sehen Sie die '
                        '<strong>fehlenden Informationen</strong>, die '
                        'Sie in der Relevanzbewertung als <span class="rel-intro-pill '
                        'rel-intro-pill--yes">✓ relevant</span> eingestuft '
                        'haben.',
        icon='layers',
        takeaways=[
            {'title': 'Relevanz als Maßstab', 'text': 'Es zählt, was für diesen '
             'Fall relevant ist – nicht jedes Detail.'},
            {'title': 'Orientierungshilfe', 'text': 'Die fehlenden Informationen '
             'stehen unter der Skala.'},
            {'title': 'Stufenlos', 'text': 'Nur die Endpunkte sind beschriftet. '
             'Dazwischen setzen Sie Ihren Wert frei.'},
        ],
    ),
    'summary_conciseness': _vas_page(
        criterion='conciseness',
        definition_title='Was bedeutet Prägnanz?',
        definition_text='Bewertet wird, ob die Zusammenfassung angemessen kurz '
                        'und fokussiert ist – <strong>weder zu knapp noch '
                        'überladen</strong>. Zur Orientierung sehen Sie enthaltene '
                        'Informationen, die Sie in der Relevanzbewertung als '
                        '<span class="rel-intro-pill rel-intro-pill--no">✗ nicht '
                        'relevant</span> eingestuft haben.',
        icon='compress',
        takeaways=[
            {'title': 'Fokus', 'text': 'Überflüssiges lenkt im Tumorboard von '
             'den Kernpunkten ab.'},
            {'title': 'Orientierungshilfe', 'text': 'Als nicht relevant '
             'eingestufte Inhalte stehen unter der Skala.'},
            {'title': 'Stufenlos', 'text': 'Nur die Endpunkte sind beschriftet. '
             'Dazwischen setzen Sie Ihren Wert frei.'},
        ],
    ),
    'summary_postedit': _postedit_page(
        'Zusammenfassung',
        'Schätzen Sie, wie lange die Überarbeitung dauern würde: '
        '<strong>Kleine Korrekturen</strong> (max. 1 min), <strong>Größere '
        'Überarbeitungen</strong> (1–5 min) oder <strong>Vollständig neu '
        'verfassen</strong> (&gt; 5 min).',
    ),
    'summary_origin_guess': _origin_page(
        'Zusammenfassung',
    ),
    'summary_preference': _preference_page(
        'Zusammenfassung',
    ),

    # ── Fragestellung ────────────────────────────────────────────────────────
    'problem_focus': {
        'stage': 'focus',
        'icon': 'target',
        'chapters': [
            {'kind': 'ui', 'title': 'Fragestellung lesen',
             'text': 'Links steht die Fragestellung für das Tumorboard, rechts '
                     'ein Baum möglicher <strong>Diskussionsschwerpunkte</strong>.'},
            {'kind': 'why', 'title': 'Beschreiben statt bewerten',
             'text': 'In diesem Schritt halten Sie fest, '
                     '<strong>worauf die Fragestellung abzielt</strong>. So lässt '
                     'sich vergleichen, ob beide Versionen dieselben Themen '
                     'ansprechen und wie präzise sie formuliert sind.'},
            {'kind': 'ui', 'title': 'Schwerpunkt anklicken',
             'text': 'Klicken Sie auf einen Knoten, z. B. <strong>Weitere '
                     'Diagnostik</strong>. Er wird markiert, und eine '
                     'Detailauswahl öffnet sich.'},
            {'kind': 'ui', 'title': 'Details ergänzen',
             'text': 'Kreuzen Sie an, welche Art von Diagnostik die '
                     'Fragestellung vorschlägt. Mehrfachauswahl ist möglich.'},
            {'kind': 'ui', 'title': 'Mehrere Schwerpunkte',
             'text': 'Spricht die Fragestellung mehrere Themen an, wählen Sie alle '
                     'zutreffenden Knoten – etwa zusätzlich '
                     '<strong>Therapie</strong> mit der vorgeschlagenen '
                     'Therapieform.'},
            {'kind': 'why', 'title': 'Und wenn nichts konkret ist?',
             'text': 'Nennt die Fragestellung keinen erkennbaren Schwerpunkt '
                     '(z. B. nur „Bitte um Vorstellung“), wählen Sie '
                     '<strong>Keine Spezifizierung</strong>. Diese Option schließt '
                     'alle anderen aus. Auch das sagt etwas über die Präzision '
                     'der Fragestellung aus.'},
        ],
        'takeaways': [
            {'title': 'Beschreibend', 'text': 'Kein Urteil – Sie halten fest, '
             'worum es geht.'},
            {'title': 'Mehrfachauswahl', 'text': 'Alle angesprochenen Themen '
             'und Unterpunkte auswählen.'},
            {'title': 'Keine Spezifizierung', 'text': 'Für Fragestellungen ohne '
             'erkennbaren Schwerpunkt.'},
        ],
    },

    'problem_correctness': {
        'stage': 'correctness_tl',
        'icon': 'traffic',
        'chapters': [
            {'kind': 'ui', 'title': 'Fragestellung lesen',
             'text': 'Rechts sehen Sie vier Antwortoptionen zur '
                     '<strong>Nachvollziehbarkeit des vorgeschlagenen '
                     'Vorgehens</strong>.'},
            {'kind': 'why', 'title': 'Drei Abstufungen',
             'text': 'Die Skala unterscheidet <strong>Therapiestandard</strong> '
                     '(best practice), eine <strong>begründbare Abweichung</strong> '
                     'und ein <strong>nicht nachvollziehbares</strong> Vorgehen. '
                     'Im Tumorboard wird oft bewusst vom Standard abgewichen, '
                     'etwa wegen Komorbiditäten oder Patientenwunsch – das soll '
                     'nicht als Fehler zählen.'},
            {'kind': 'ui', 'title': 'Option wählen',
             'text': 'Klicken Sie auf die zutreffende Option; die Ampel leuchtet '
                     'auf.'},
            {'kind': 'ui', 'title': 'Auswahl ändern',
             'text': 'Ein Klick auf eine andere Option ändert die Auswahl '
                     'jederzeit.'},
            {'kind': 'why', 'title': 'Wenn es nichts zu beurteilen gibt',
             'text': 'Enthält die Fragestellung kein konkretes Vorgehen, wählen '
                     'Sie <strong>Nicht spezifisch genug für eine '
                     'Beurteilung</strong> (grau). So werden vage Fragestellungen '
                     'nicht fälschlich als falsch gewertet.'},
            {'kind': 'why', 'title': 'Ihr Maßstab',
             'text': 'Maßgeblich sind der aktuelle Standard – z. B. die '
                     '<a href="{guideline_url}" target="_blank" rel="noopener">'
                     'S3-Leitlinie Melanom</a> – und Ihre klinische Erfahrung, '
                     'bezogen auf die Falldaten in der Patientenakte. Ob die '
                     'Fragestellung alle Aspekte des Falls abdeckt, bewerten Sie '
                     'separat im nächsten Schritt <em>Fallspezifität</em>.'},
        ],
        'takeaways': [
            {'title': 'Abweichung ≠ Fehler', 'text': 'Begründbare Abweichungen '
             'haben eine eigene Stufe.'},
            {'title': 'Grau für vage', 'text': 'Ohne konkretes Vorgehen: „Nicht '
             'spezifisch genug“.'},
            {'title': 'Leitlinie + Erfahrung', 'text': 'Standard und klinisches '
             'Urteil, bezogen auf den Fall.'},
        ],
    },

    'problem_specificity': {
        'stage': 'specificity',
        'icon': 'person',
        'chapters': [
            {'kind': 'ui', 'title': 'Fragestellung lesen',
             'text': 'Rechts steht die Aussage <em>„Alle relevanten Aspekte des '
                     'Falls werden berücksichtigt.“</em> – darunter drei '
                     'Antwortoptionen.'},
            {'kind': 'why', 'title': 'Was bedeutet Fallspezifität?',
             'text': 'Bewertet wird, inwieweit die Fragestellung die '
                     '<strong>für diesen Patienten relevanten Aspekte</strong> '
                     'berücksichtigt, etwa Vortherapien, den aktuellen Befund und '
                     'relevante Begleitumstände.'},
            {'kind': 'ui', 'title': 'Bezüge prüfen',
             'text': 'Gleichen Sie die Fragestellung mit der Patientenakte ab: '
                     'Welche relevanten Aspekte werden aufgegriffen, welche '
                     'fehlen?'},
            {'kind': 'ui', 'title': 'Zustimmung wählen',
             'text': 'Wählen Sie <strong>Trifft zu</strong> (alle relevanten '
                     'Aspekte berücksichtigt), <strong>Trifft teilweise zu</strong> '
                     '(einige relevante Aspekte fehlen oder sind unvollständig) '
                     'oder <strong>Trifft nicht zu</strong> (wesentliche Aspekte '
                     'des Falls fehlen).'},
            {'kind': 'why', 'title': 'Abgrenzung zu den anderen Kriterien',
             'text': '<strong>Fokus</strong> beschreibt, welche Themen angesprochen '
                     'werden; <strong>Nachvollziehbarkeit</strong> die '
                     'medizinische Begründbarkeit. <strong>Fallspezifität</strong> '
                     'fragt, ob die Fragestellung auf diesen Fall zugeschnitten '
                     'ist.'},
        ],
        'takeaways': [
            {'title': 'Fallbezug', 'text': 'Bewertet wird, ob die relevanten '
             'Aspekte des Falls berücksichtigt sind.'},
            {'title': 'Patientenakte', 'text': 'Abgleich mit den dokumentierten '
             'Falldaten.'},
            {'title': 'Eigenständig', 'text': 'Unabhängig von Fokus und '
             'Nachvollziehbarkeit bewerten.'},
        ],
    },

    'problem_postedit': _postedit_page(
        'Fragestellung',
        'Schätzen Sie, wie lange die Überarbeitung dauern würde: '
        '<strong>Kleine Korrekturen</strong> (max. 1 min) oder '
        '<strong>Vollständig neu verfassen</strong> (&gt; 1 min).',
    ),
    'problem_origin_guess': _origin_page(
        'Fragestellung',
    ),
    'problem_preference': _preference_page(
        'Fragestellung',
    ),

    # ── Abschluss ────────────────────────────────────────────────────────────
    'final_overall': {
        'stage': 'complexity',
        'icon': 'gauge',
        'chapters': [
            {'kind': 'ui', 'title': 'Abschluss des Falls',
             'text': 'Nach beiden Bewertungsblöcken schätzen Sie die '
                     '<strong>klinische Komplexität</strong> des gesamten Falls '
                     'ein.'},
            {'kind': 'why', 'title': 'Warum Komplexität?',
             'text': 'Die Fallkomplexität ist eine wichtige '
                     '<strong>Einflussgröße</strong>: Mit ihr lässt sich '
                     'auswerten, ob sich die Qualität der Texte zwischen '
                     'einfachen und komplexen Fällen unterscheidet.'},
            {'kind': 'ui', 'title': 'Wert setzen',
             'text': 'Klicken Sie auf die Skala: <strong>0</strong> steht für '
                     'einen sehr einfachen Routinefall, <strong>100</strong> für '
                     'einen hochkomplexen Fall.'},
            {'kind': 'why', 'title': 'Ihre Gesamteinschätzung',
             'text': 'Maßgeblich ist Ihre <strong>klinische '
                     'Gesamteinschätzung</strong> des Falls auf Grundlage der '
                     'Patientenakte.'},
            {'kind': 'ui', 'title': 'Kommentar und Abschluss',
             'text': 'Optional können Sie einen Kommentar zum Fall hinterlassen. '
                     '<strong>Fall abschließen ✓</strong> ist erst aktiv, wenn '
                     'alle vorherigen Schritte bewertet sind.'},
        ],
        'takeaways': [
            {'title': 'Ganzer Fall', 'text': 'Bewertet wird der Fall, nicht die '
             'Texte.'},
            {'title': 'Einflussgröße', 'text': 'Hilft, Ergebnisse nach '
             'Fallschwere zu differenzieren.'},
            {'title': 'Ihr Gesamteindruck', 'text': 'Von Routinefall (0) bis '
             'hochkomplex (100).'},
        ],
    },
}
