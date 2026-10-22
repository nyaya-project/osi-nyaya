#!/usr/bin/env python3
# Campaign-local; does not emit coordinates or CIF text.
import argparse,json
# Retrieval is deliberately injected as logged excerpts; direct Valency calls occur only in the invoking harness.
def main():
 a=argparse.ArgumentParser();a.add_argument('candidate');a.add_argument('retrieval');a.add_argument('output');x=a.parse_args();c=json.load(open(x.candidate));r=json.load(open(x.retrieval)); ex=[z for z in r.get('excerpts',[]) if not z.get('reports_formula_B_structure')][:8]
 for i,z in enumerate(ex,1):z['evidence_id']=f"{c['candidate_id']}:L{i}"
 json.dump({'candidate_id':c['candidate_id'],'formula_B':c['formula_B'],'excerpts':ex},open(x.output,'w'),indent=2)
if __name__=='__main__':main()
