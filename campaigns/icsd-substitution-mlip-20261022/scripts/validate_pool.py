#!/usr/bin/env python3
# Campaign-local; does not emit coordinates or CIF text.
import argparse,json,re,sys
REQ={'candidate_id','source_collection_code','source_formula','site_label','element_out','element_in','formula_B','charge_preserving','delta_r_over_r','anion','framework_family','batch'}
def validate(d, expected=None):
 e=[]; cs=d.get('candidates',[])
 if d.get('campaign_id')!='icsd-substitution-mlip-20261022': e.append('bad campaign_id')
 if expected is not None and len(cs)!=expected:e.append(f'expected {expected} candidates, got {len(cs)}')
 ids=set(); formulas=set()
 for i,c in enumerate(cs):
  miss=REQ-set(c); extra=set(c)-REQ
  if miss or extra:e.append(f'row {i}: missing={sorted(miss)} extra={sorted(extra)}')
  cid=c.get('candidate_id');
  if cid in ids:e.append(f'duplicate candidate_id {cid}')
  ids.add(cid)
  if c.get('element_in')==c.get('element_out'):e.append(f'{cid}: identical elements')
  f=''.join(re.findall(r'[A-Z][a-z]?\d*',c.get('formula_B','')))
  if not f:e.append(f'{cid}: invalid formula_B')
  if f in formulas:e.append(f'duplicate formula_B {f}')
  formulas.add(f)
 return e
def main():
 p=argparse.ArgumentParser();p.add_argument('pool');p.add_argument('--expected',type=int);a=p.parse_args(); e=validate(json.load(open(a.pool)),a.expected); print(json.dumps({'valid':not e,'errors':e}));sys.exit(bool(e))
if __name__=='__main__':main()
