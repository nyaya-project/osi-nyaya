#!/usr/bin/env python3
# Campaign-local; does not emit coordinates or CIF text.
import argparse,json
# Candidates are retained only when precomputed ICSD and Valency checks are both false.
def main():
 a=argparse.ArgumentParser();a.add_argument('input');a.add_argument('output');x=a.parse_args();d=json.load(open(x.input)); kept=[];drops=[]
 for c in d['candidates']:
  n=c.get('novelty',{})
  if n.get('icsd_structure') or n.get('valency_structure'):
   drops.append({'candidate_id':c['candidate_id'],'reason':'icsd' if n.get('icsd_structure') else 'valency','source_id':n.get('source_id')})
  else: kept.append(c)
 json.dump({'kept':kept,'drops':drops},open(x.output,'w'),indent=2)
if __name__=='__main__':main()
