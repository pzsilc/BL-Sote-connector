from re import compile as cmpl
from json import loads

class OptionsExtractor:
    wrong_values = ['{"typ_ceny":"brutto"}', '{"typ_ceny":"netto"}']
    pattern = cmpl('{(.*)}')

    def extract(sote_product):
        ops = sote_product['product_options']
        if not ops or ops.replace(' ', '') not in OptionsExtractor.wrong_values:
            return []
        options = ['{'+i+'}' for i in OptionsExtractor.pattern.findall(ops)]
        return [loads(i) for i in options if 'kod' in loads(i)]
