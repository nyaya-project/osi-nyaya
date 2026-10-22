#!/usr/bin/env python3
# Campaign-local; does not emit coordinates or CIF text.
import argparse,json
# Primary per-arm Brier and accuracy; bootstrap/report rendering are performed only on locked labels.
def main():
 a=argparse.ArgumentParser();a.add_argument('labels');a.add_argument('prediction');x=a.parse_args();labels={z['candidate_id']:z for z in json.load(open(x.labels))['rows']};pred=json.load(open(x.prediction)); xs=[(r,labels[r['candidate_id']]) for r in pred['rows'] if r['candidate_id'] in labels and not labels[r['candidate_id']].get('exclusion_reason')]
 b=sum((r['p_retained']-(1 if y['label']=='retained' else 0))**2 for r,y in xs)/len(xs) if xs else None;acc=sum(r['predicted_outcome']==y['label'] for r,y in xs)/len(xs) if xs else None
 print(json.dumps({'n':len(xs),'brier':b,'accuracy':acc}))
if __name__=='__main__':main()
