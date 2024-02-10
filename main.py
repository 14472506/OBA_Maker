""" 
===================================================================================================
Details
===================================================================================================
"""
# imports =========================================================================================
# base and third party packages
import argparse
import yaml

# local packages
from generators import BasicOBAMaker

# class ===========================================================================================
class OBAMaker():
    """ OBAMaker class handles process at high level """
    def __init__(self, cfg):
        """ detials """
        self._init_attributes(cfg)
        self._augmentor_select()

    def _init_attributes(self, cfg):
        """ detials """
        self.cfg = cfg
        self.augmentor_type = cfg["augmentor_type"]
    
    def _augmentor_select(self):
        """ detials """
        if self.augmentor_type == "Basic":
            self.augmentor = BasicOBAMaker(self.cfg)
        
    def run(self):
        """ Detials """
        self.augmentor.run()

# functions =======================================================================================
def main(args):
    """ executes program """
    cfg = load_config(args.config)
    oba_maker = OBAMaker(cfg)
    oba_maker.run()

def load_config(cfg_root):
    """ Detials """
    with open(cfg_root, "r") as file:
        return yaml.safe_load(file)

def init_parser():
    """ initialises parser """
    # initialise parser
    parser = argparse.ArgumentParser(description="Retrieves key parameters during execution")
    # add to paerser
    parser.add_argument("-config", type=str, required=True, help="Provide the path to the experiment config")
    # return
    return parser

# execute =========================================================================================
if __name__ == "__main__":
    """
    Entry point of script:
        The following code defines the args parser, gathers the provided arguments, 
        them passes them to the main function
    """
    # get parser and execute main
    parser = init_parser()
    args = parser.parse_args()
    main(args)
