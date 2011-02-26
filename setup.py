from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('epr', ['src/epr.pyx'], libraries=['epr_api'])]

setup(
  name = 'Python EPR API',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
