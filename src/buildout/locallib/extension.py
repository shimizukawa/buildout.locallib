from zc.buildout import easy_install
from distutils.sysconfig import get_python_lib

SP_PATH = get_python_lib()

class Installer(easy_install.Installer):
    """ hook easy_install.Installer() for egg search path modification """

    base = None

    def __init__(self, *args, **kw):
        # if exist args[5] (is path parameter) or 'path' keyword argument,
        # update path list for including 'site-packages' path.

        #print '### easy_install.Installer hooking ...'
        if len(args) > 5:
            path = args[5]
        elif kw.get('path') is not None:
            path = kw['path']
        else:
            path = kw['path'] = []

        if SP_PATH not in path:
            path.append(SP_PATH)

        self.base.__init__(self, *args, **kw)

    __init__.func_doc = easy_install.Installer.__init__.func_doc


def patch_to_Installer():
    #print '### easy_install.Installer patching ...'
    if easy_install.Installer != Installer:
        Installer.base = easy_install.Installer
        easy_install.Installer = Installer


def load(buildout):
    patch_to_Installer()

