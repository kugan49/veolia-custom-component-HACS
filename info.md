# Notice

## How to commit new version :

- change version in `custom_components/veolia/manifest.json`
- Add infos about new version in `CHANGELOG.md`
- To auto release commit whith name : `Release: vx.x.x ....`

## What?

[integration_blueprint][integration_blueprint]

This repository contains multiple files, here is a overview:

| File                                        | Purpose                                                                                                                                                                                                                                         |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.devcontainer/*`                           | Used for development/testing with VSCODE, more info in the readme file in that dir.                                                                                                                                                             |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Template for Feature Requests                                                                                                                                                                                                                   |
| `.github/ISSUE_TEMPLATE/issue.md`           | Template for issues                                                                                                                                                                                                                             |
| `.vscode/tasks.json`                        | Tasks for the devcontainer.                                                                                                                                                                                                                     |
| `custom_components/veolia/translations/*`   | [Translation files.](https://developers.home-assistant.io/docs/internationalization/custom_integration)                                                                                                                                         |
| `custom_components/veolia/__init__.py`      | The component file for the integration.                                                                                                                                                                                                         |
| `custom_components/veolia/api.py`           | This is a sample API client.                                                                                                                                                                                                                    |
| `custom_components/veolia/binary_sensor.py` | Binary sensor platform for the integration.                                                                                                                                                                                                     |
| `custom_components/veolia/config_flow.py`   | Config flow file, this adds the UI configuration possibilities.                                                                                                                                                                                 |
| `custom_components/veolia/const.py`         | A file to hold shared variables/constants for the entire integration.                                                                                                                                                                           |
| `custom_components/veolia/manifest.json`    | A [manifest file](https://developers.home-assistant.io/docs/en/creating_integration_manifest.html) for Home Assistant.                                                                                                                          |
| `custom_components/veolia/sensor.py`        | Sensor platform for the integration.                                                                                                                                                                                                            |
| `custom_components/veolia/switch.py`        | Switch sensor platform for the integration.                                                                                                                                                                                                     |
| `tests/__init__.py`                         | Makes the `tests` folder a module.                                                                                                                                                                                                              |
| `tests/conftest.py`                         | Global [fixtures](https://docs.pytest.org/en/stable/fixture.html) used in tests to [patch](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch) functions.                                                                 |
| `tests/test_api.py`                         | Tests for `custom_components/veolia/api.py`.                                                                                                                                                                                                    |
| `tests/test_config_flow.py`                 | Tests for `custom_components/veolia/config_flow.py`.                                                                                                                                                                                            |
| `tests/test_init.py`                        | Tests for `custom_components/veolia/__init__.py`.                                                                                                                                                                                               |
| `tests/test_switch.py`                      | Tests for `custom_components/veolia/switch.py`.                                                                                                                                                                                                 |
| `CONTRIBUTING.md`                           | Guidelines on how to contribute.                                                                                                                                                                                                                |
| `example.png`                               | Screenshot that demonstrate how it might look in the UI.                                                                                                                                                                                        |
| `info.md`                                   | An example on a info file (used by [hacs][hacs]).                                                                                                                                                                                               |
| `LICENSE`                                   | The license file for the project.                                                                                                                                                                                                               |
| `README.md`                                 | The file you are reading now, should contain info about the integration, installation and configuration instructions.                                                                                                                           |
| `requirements.txt`                          | Python packages used by this integration.                                                                                                                                                                                                       |
| `requirements_dev.txt`                      | Python packages used to provide [IntelliSense](https://code.visualstudio.com/docs/editor/intellisense)/code hints during development of this integration, typically includes packages in `requirements.txt` but may include additional packages |
| `requirements_test.txt`                     | Python packages required to run the tests for this integration, typically includes packages in `requirements_dev.txt` but may include additional packages                                                                                       |

## How?

If you want to use all the potential and features of this blueprint template you
should use Visual Studio Code to develop in a container. In this container you
will have all the tools to ease your python development and a dedicated Home
Assistant core instance to run your integration. See `.devcontainer/README.md` for more information.

If you need to work on the python library in parallel of this integration
(`sampleclient` in this example) there are different options. The following one seems
easy to implement:

- Create a dedicated branch for your python library on a public git repository (example: branch
  `dev` on `https://github.com/ludeeus/sampleclient`)
- Update in the `manifest.json` file the `requirements` key to point on your development branch
  ( example: `"requirements": ["git+https://github.com/ludeeus/sampleclient.git@dev#devp==0.0.1beta1"]`)
- Each time you need to make a modification to your python library, push it to your
  development branch and increase the number of the python library version in `manifest.json` file
  to ensure Home Assistant update the code of the python library. (example `"requirements": ["git+https://...==0.0.1beta2"]`).

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://github.com/custom-components/hacs
