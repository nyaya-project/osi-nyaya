#!/usr/bin/env python3
# Campaign-local; does not emit coordinates or CIF text.
import argparse,json,math
P={'pratyaksha/direct':4,'anumana/inference':3,'upamana/analogy':2,'shabda/unexplained lit. claim':1,'unassessed':0};S={'strong':1,'moderate':.6,'weak':.3,'unassessed':0}
def score(items):
 best={}
 for x in items:
  if not x.get('accepted_by_judge'):continue
  sign=1 if x['direction']=='retained' else -1; w=P[x['pramana_class']]*S[x['support_strength']]*sign; q=S[x['support_strength']]*sign
  k=x['evidence_origin_id']
  if k not in best or abs(w)>abs(best[k][0]):best[k]=(w,q)
 w=sum(x[0] for x in best.values());q=sum(x[1] for x in best.values());den=sum(abs(x[0]) for x in best.values())+1
 p=.5+.5*w/den
 return {'pramana_score_weighted':w,'pramana_score_strength_only':q,'p_retained':p,'uncertainty':1-abs(2*p-1),'predicted_outcome':'retained' if p>=.5 else 'reconstructed','evidence_magnitude':den-1}
def main():
 a=argparse.ArgumentParser();a.add_argument('ledger');a.add_argument('output');x=a.parse_args();d=json.load(open(x.ledger));out={}
 for c in {i['candidate_id'] for i in d['items']}:out[c]=score([i for i in d['items'] if i['candidate_id']==c])
 json.dump(out,open(x.output,'w'),indent=2)
if __name__=='__main__':main()
