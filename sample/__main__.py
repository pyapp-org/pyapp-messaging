from pyapp.app import CliApplication, CommandOptions
from pyapp.injection import inject_into, Args

import sample


app = CliApplication(sample)


def main(args=None):
    app.dispatch(args)


if __name__ == "__main__":
    main()
