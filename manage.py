"""Manager to run commands linked to the application."""
import subprocess
from flask_script import Manager

from app import app


manager = Manager(app)


def taskrc_handler(variable, variable_details):
    """Specific handler for TASKRC config.

    :param str variable: variable name to edit.
    :param dict variable_details: dictionnary containing details of the config
    variable.
    """
    # Unix specific try:
    try:
        possible_existing_taskrc = subprocess.check_output(
            ['locate', 'taskrc']).decode("utf-8")
        for taskrc in possible_existing_taskrc.split("\n"):
            if taskrc.endswith("taskrc"):
                variable_details["value"] = taskrc
                break
    except Exception:
        # It will fail on windows.
        pass
    variable_details["value"] = input("{} [{}]:".format(
        variable, variable_details["value"])) or variable_details["value"]


@manager.command
def new_config():
    """Generate local config file."""
    # List of variables that can be specified.
    # value key is set to default value.
    config_variables = {"SQLALCHEMY_DATABASE_URI": {"description": "",
                                                    "value": "sqlite:///test.db"},
                        "SQLALCHEMY_TRACK_MODIFICATIONS": {"description": "",
                                                           "value": False},
                        "UPLOAD_FOLDER": {"description": "",
                                          "value": "./app/static/uploads/"},
                        "SECRET_KEY": {"description": "",
                                       "value": "redpr0d"},
                        "ENV": {"description": "",
                                "value": "PROD"},
                        "TASKRC": {"description": "",
                                   "value": "./app/config/taskrc",
                                   "handler": taskrc_handler},
                        "ADMIN_EMAIL": {"description": "",
                                        "value": "encima@gmail.com"},
                        "ADMIN_PW": {"description": "",
                                     "value": "Tumultuous4Sunscreen"},
                        "THEME": {"description": "",
                                  "value": "Base"}}

    # Write the file in the config folder.
    for variable in config_variables:
        variable_details = config_variables[variable]
        if "handler" not in variable_details:
            # Default case.
            variable_details["value"] = input("{} [{}]:".format(
                variable, variable_details["value"])) or variable_details["value"]

        else:
            # Case we have a specific handler for a specific variable
            variable_details["handler"](variable, variable_details)

    # Write the local config file
    with open("app/config/local.cfg", "w+") as config_file:
        for variable in config_variables:
            config_file.write("{}='{}'\n".format(
                variable, config_variables[variable]["value"]))


if __name__ == "__main__":
    manager.run()
