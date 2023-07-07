#!/usr/bin/python

class FilterModule(object):
    def filters(self):
        return {
            'join_vars': self.join_vars
        }

    def join_vars(self, rulebook_list, extra_vars_list):
        result = []
        for rulebook in rulebook_list:
            for extra_vars in extra_vars_list:
                if rulebook['name'] == extra_vars['name']:
                    rulebook['var_id'] = extra_vars['var_id']
                    break
            result.append(rulebook)
        return result
