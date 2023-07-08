#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import requests


def check_credential_exists(controller_url, controller_user, controller_password, name):
    url = f"{controller_url}/api/eda/v1/credentials/?name={name}"
    response = requests.get(url, auth=(controller_user, controller_password), verify=False)
    if response.status_code in (200, 201):
        credential_id = response.json().get('results', [{}])[0].get('id')
        return int(credential_id) if credential_id else None


def create_or_update_credential(module):
    # Extract input parameters from the module object
    controller_url = module.params['controller_url']
    controller_user = module.params['controller_user']
    controller_password = module.params['controller_password']
    credentials = module.params['eda_credentials']

    response_list = []

    for credential in credentials:
        name = credential['name']
        description = credential.get('description', '')
        username = credential['username']
        secret = credential['secret']
        credential_type = credential['credential_type']

        # Check if the credential exists
        credential_id = check_credential_exists(controller_url, controller_user, controller_password, name)

        # Build the payload
        payload = {
            'name': name,
            'description': description,
            'credential_type': credential_type,
            'username': username,
            'secret': secret
        }

        url = f"{controller_url}/api/eda/v1/credentials/"
        headers = {'Content-Type': 'application/json'}

        if credential_id:
            # Update the credential
            url += f"{credential_id}/"
            response = requests.patch(url, auth=(controller_user, controller_password), json=payload,
                                      headers=headers, verify=False)
        else:
            # Create the credential
            response = requests.post(url, auth=(controller_user, controller_password), json=payload,
                                     headers=headers, verify=False)

        if response.status_code in (200, 201):
            response_list.append(response.json())

    module.exit_json(changed=True, credentials=response_list)


def main():
    module_args = dict(
        controller_url=dict(type='str', required=True),
        controller_user=dict(type='str', required=True),
        controller_password=dict(type='str', required=True, no_log=True),
        eda_credentials=dict(type='list', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    try:
        create_or_update_credential(module)
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()