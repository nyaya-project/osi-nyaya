import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).parents[1]
def load(name):
 s=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_schemas_are_json_and_closed():
 for p in (ROOT/'schemas').glob('*.json'):
  d=json.loads(p.read_text()); assert d['additionalProperties'] is False

def test_pool_validator_detects_duplicate_id():
 m=load('validate_pool'); row={'candidate_id':'C01','source_collection_code':'x','source_formula':'AO','site_label':'a','element_out':'A','element_in':'B','formula_B':'BO','charge_preserving':True,'delta_r_over_r':.1,'anion':'O','framework_family':'f','batch':1}; assert any('duplicate candidate_id' in x for x in m.validate({'campaign_id':'icsd-substitution-mlip-20261022','candidates':[row,row]}))

def test_pramana_deduplicates_origin():
 m=load('pramana_score'); xs=[{'accepted_by_judge':True,'direction':'retained','pramana_class':'anumana/inference','support_strength':'strong','evidence_origin_id':'x'},{'accepted_by_judge':True,'direction':'reconstructed','pramana_class':'shabda/unexplained lit. claim','support_strength':'weak','evidence_origin_id':'x'}]; assert m.score(xs)['pramana_score_weighted']==3

def test_all_scripts_compile():
 import py_compile
 for p in (ROOT/'scripts').glob('*.py'): py_compile.compile(str(p),doraise=True)
