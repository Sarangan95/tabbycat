"""Checks for feedbacks with more than one version."""

import header
import debate.models as m

import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.parse_args()

for adj in m.Adjudicator.objects.all():
    seen = list()
    for feedback in m.AdjudicatorFeedback.objects.filter(adjudicator=adj):
        if feedback.source in seen:
            continue
        seen.append(feedback.source)
        others = m.AdjudicatorFeedback.objects.filter(adjudicator=adj,
            source_adjudicator=feedback.source_adjudicator,
            source_team=feedback.source_team).order_by('version')
        num = others.count()
        if num > 1:
            print " *** Adjudicator: {0}, from: {1}, {2:d} versions".format(adj, feedback.source, num)
            for other in others:
                #print other.timestamp.isoformat()
                print "   {6:>3} {5:<12} {4} {7} {3} {0:.1f} {1} {2}".format(other.score, {None: "-", True: "y", False: "n"}[other.agree_with_decision], other.comments, other.version, other.round, other.user, other.id, other.confirmed and "c" or "-")
