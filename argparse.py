import argparse


class ArgumentParser(argparse.ArgumentParser):
    """ перекрыл error, для того, чтобы можно было получать Exception без SystemExit """

    def error(self, message):
        raise Exception(message)
