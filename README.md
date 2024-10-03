# Role Name

The role's purpose is to provide an helper for configuring EDA Controller via API

## Requirements

N/A

## Role Variables

## Configure Projects

| Name                                 | Description                                                  | Mandatory | Defaults |
| ------------------------------------ | ------------------------------------------------------------ | --------- | -------- |
| `eda_controller_url`                 | The URL of the EDA Controller API.                           | ✔️        |          |
| `eda_controller_username`                | The username for authenticating with the EDA Controller API. | ✔️        |          |
| `eda_controller_password`            | The password for authenticating with the EDA Controller API. | ✔️        |          |
| `eda_project`                        | Configuration for the EDA Project.                           | ✔️        |          |

### Structure of `eda_project`:

| Name          | Description                                |
| ------------- | ------------------------------------------ |
| `name`        | The name of the EDA Project.               |
| `git_url`     | The Git URL of the EDA Project repository. |
| `description` | A description of the EDA Project.          |

## Configure Decision environments

| Name                              | Description                                                  | Mandatory | Defaults |
| --------------------------------- | ------------------------------------------------------------ | --------- | -------- |
| `eda_controller_url`              | The URL of the EDA Controller API.                           | ✔️        |          |
| `eda_controller_username`             | The username for authenticating with the EDA Controller API. | ✔️        |          |
| `eda_controller_password`         | The password for authenticating with the EDA Controller API. | ✔️        |          |
| `eda_decision_env`                | Configuration for the Decision Environment.                  | ✔️        |          |

### Structure of `eda_decision_env`:

| Name        | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| `name`      | The name of the Decision Environment.                        |
| `image_url` | The URL of the image for the Decision Environment container. |

## Configure activations

| Name                        | Description                                                  | Mandatory | Defaults |
| --------------------------- | ------------------------------------------------------------ | --------- | -------- |
| `eda_controller_url`        | The URL of the EDA Controller API.                           | ✔️        |          |
| `eda_controller_username`       | The username for authenticating with the EDA Controller API. | ✔️        |          |
| `eda_controller_password`   | The password for authenticating with the EDA Controller API. | ✔️        |          |
| `eda_activations`           | List of activations to create for the given project.         | ✔️        |          |


### Structure of `eda_activations`:

| Name         | Description                               |
| ------------ | ----------------------------------------- |
| `name`       | The name of the activation.               |
| `project name` | Project name for the activation   |
| `rulebook`   | The YAML file of the associated rulebook. |
| `decision_env` | Decision environment name   |
| `controller_token` | Token name for the user   |
| `extra_vars` | Extra variables to add to the rulebook.   |
| `restart_policy` (optional) | The restart policy for the activations (default: always).    | ❌        | `always` |
| `enabled` (optional)        | Flag to enable/disable the activations (default: true).      | ❌        | `true`   |

## Dependencies

N/A

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    ---
    - name: Sample EDA Controller Setup
      hosts: localhost
      gather_facts: false

      roles:
        - role: role_eda_controller_setup
          vars:
            eda_controller_url: "https://your-eda-controller-api.com"
            eda_controller_username: "your_eda_user"
            eda_controller_password: "your_eda_password"
            eda_projects:
              - name: "EDA Demo Project"
                git_url: "https://github.com/kubealex/event-driven-automation"
                description: "Demo project to show EDA in action"
            eda_decision_env:
              - name: "kubealex-eda"
                image_url: "quay.io/kubealex/eda-decision-env"
            eda_activations:
              - name: "eda-alertmanager"
                rulebook: "eda-rulebook-alertmanager.yml"
                project_name: EDA Demo Project
                decision_env: Automation Hub Default Decision Environment
                controller_token: "Automation Controller Token"

## License

Apache 2.0

## Author Information

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
