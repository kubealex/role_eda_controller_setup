#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import requests


def create_activations(module):
    # Extract input parameters from the module object
    eda_controller_url = module.params['eda_controller_url']
    eda_project_id = module.params['eda_project_id']
    eda_controller_user = module.params['eda_controller_user']
    eda_controller_password = module.params['eda_controller_password']
    restart_policy = module.params['restart_policy']
    enabled = module.params['enabled']
    eda_denv_id = module.params['eda_denv_id']
    eda_activations = module.params['eda_activations']

    rulebook_list = []
    extra_vars_list = []

    # Retrieve rulebooks
    url = f"{eda_controller_url}/api/eda/v1/rulebooks/?project_id={eda_project_id}"
    response = requests.get(url, auth=(eda_controller_user, eda_controller_password), verify=False)
    if response.status_code in (200, 201):
        rulebooks = response.json().get('results', [])
        for activation in eda_activations:
            for rulebook in rulebooks:
                if rulebook['name'] == activation['rulebook']:
                    rulebook_list.append({'name': activation['name'], 'id': int(rulebook['id'])})
                    break

    # Create extra vars for activations
    for activation in eda_activations:
        if 'extra_vars' in activation and activation['extra_vars']:
            url = f"{eda_controller_url}/api/eda/v1/extra-vars/"
            body = {"extra_var": activation['extra_vars']}
            response = requests.post(url, auth=(eda_controller_user, eda_controller_password),
                                     json=body, verify=False)
            if response.status_code in (200, 201):
                extra_vars_list.append({'name': activation['name'], 'var_id': int(response.json().get('id'))})

    # Join rulebook_list and extra_vars_list
    activations_list = []
    for rulebook in rulebook_list:
        activation = {
            'name': rulebook['name'],
            'project_id': int(eda_project_id),
            'decision_environment_id': int(eda_denv_id),
            'rulebook_id': rulebook['id'],
            'restart_policy': restart_policy,
            'is_enabled': enabled
        }
        for extra_vars in extra_vars_list:
            if extra_vars['name'] == rulebook['name']:
                activation['extra_var_id'] = extra_vars['var_id']
                break
        activations_list.append(activation)

    # Create activations for given project
    url = f"{eda_controller_url}/api/eda/v1/activations/"
    response_list = []
    for activation in activations_list:
        body = {
            'restart_policy': activation['restart_policy'],
            'is_enabled': activation['is_enabled'],
            'name': activation['name'],
            'project_id': activation['project_id'],
            'decision_environment_id': activation['decision_environment_id'],
            'rulebook_id': activation['rulebook_id'],
        }
        if 'extra_var_id' in activation:
            body['extra_var_id'] = activation['extra_var_id']
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, auth=(eda_controller_user, eda_controller_password),
                                 json=body, headers=headers, verify=False)
        if response.status_code in (200, 201):
            response_list.append(response.json())

    module.exit_json(changed=True, activations=response_list)


def main():
    module_args = dict(
        eda_controller_url=dict(type='str', required=True),
        eda_project_id=dict(type='str', required=True),
        eda_controller_user=dict(type='str', required=True),
        eda_controller_password=dict(type='str', required=True, no_log=True),
        restart_policy=dict(type='str', default='always'),
        enabled=dict(type='bool', default=True),
        eda_denv_id=dict(type='str', required=True),
        eda_activations=dict(type='list', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    try:
        create_activations(module)
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()