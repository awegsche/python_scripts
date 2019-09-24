from subprocess import Popen


class MadxCreator:
    def __init__(self):
        self.settings = {}
        self.tempfile = None
        self.targetfile = None
        self.errors = ""

    def new():
        return MadxCreator()

    def template(self, path: str):
        self.tempfile = path
        return self

    def target(self, path: str):
        self.targetfile = path
        return self

    def with_setting(self, key: str, value: object):
        self.settings[key] = str(value)
        return self

    def with_error(self, pattern, strengths, kind="EFCOMP"):
        strength_str = ", ".join([f"{x}*1.0e-4*TGAUSS(3)" for x in strengths])
        self.errors += f"""
SELECT, flag=error, clear;
SELECT, flag=error, pattern="{pattern}";
{kind}, order=1, radius=1, dknr:={{ {strength_str} }};
"""
        return self

    def create(self):
        print(self.settings)
        if self.targetfile is None:
            self.targetfile = "job." + self.tempfile
        self.settings["errors"] = self.errors
        self.settings["error"] = self.errors

        with open(self.targetfile, "w") as targ:
            with open(self.tempfile, "r") as temp:
                targ.write(temp.read().format(**self.settings))

        return self

    def run(self):
        return Popen([
            "madx",
            self.targetfile,
        ])

    def create_and_run(self):
        self.create()
        return self.run()
