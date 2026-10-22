#!/usr/bin/env python3
# Campaign-local; does not emit coordinates or CIF text.
import argparse,json
# Converts scored candidate mappings into a schema-shaped Nyaya prediction set.
def main():
 a=argparse.ArgumentParser();a.add_argument('scores');a.add_argument('output');x=a.parse_args();s=json.load(open(x.scores)); rows=[]
 for rank,(cid,v) in enumerate(sorted(s.items(),key=lambda z:-abs(2*z[1]['p_retained']-1)),1):rows.append({'candidate_id':cid,'rank':rank,'in_top10':rank<=10,'predicted_outcome':v['predicted_outcome'],'p_retained':v['p_retained'],'rationale_ref':'ledger','tier':2,**{k:v[k] for k in ('pramana_score_weighted','pramana_score_strength_only','uncertainty')}})
 json.dump({'campaign_id':'icsd-substitution-mlip-20261022','arm':'nyaya','model':'gpt-5.6-sol','rows':rows},open(x.output,'w'),indent=2)
if __name__=='__main__':main()
