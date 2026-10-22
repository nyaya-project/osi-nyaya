#!/usr/bin/env python3
# Campaign-local; does not emit coordinates or CIF text.
import argparse,json,re,sys
def main():
 a=argparse.ArgumentParser();a.add_argument('prediction');a.add_argument('evidence_dir');x=a.parse_args();d=json.load(open(x.prediction));bad=[];total=0
 for row in d['rows']:
  p=f"{x.evidence_dir}/{row['candidate_id']}.json"
  if not __import__('os').path.exists(p):continue
  pack=json.load(open(p)); ids={z.get('evidence_id') for z in pack.get('excerpts',[])}; cited=set(re.findall(r'(?:C\d+:)?L\d+',row.get('rationale_ref','')))
  total+=len(cited); bad += [f"{row['candidate_id']}:{z}" for z in cited if z not in ids]
 print(json.dumps({'citations':total,'failures':len(bad),'invalid':bad,'failure_rate':len(bad)/total if total else 0}));sys.exit(bool(bad))
if __name__=='__main__':main()
