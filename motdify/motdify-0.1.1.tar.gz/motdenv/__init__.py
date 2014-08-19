import os, glob

motdenv_files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in motdenv_files if os.path.basename(f) != "__init__.py"]