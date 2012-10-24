'''
Handle the version information here; you should only have to
change the version tuple.
'''


class Version(object):

    def __init__(self, package, major, minor, micro):
        '''

        :param package: Name of the package that this is a version of.
        :param major: The major version number.
        :param minor: The minor version number.
        :param micro: The micro version number.
        '''
        self.package = package
        self.major = major
        self.minor = minor
        self.micro = micro

    def short(self):
        ''' Return a string in canonical short version format
        <major>.<minor>.<micro>
        '''
        return '%d.%d.%d' % (self.major, self.minor, self.micro)

    def __str__(self):
        ''' Returns a string representation of the object

        :returns: A string representation of this object
        '''
        return '[%s, version %s]' % (self.package, self.short())

version = Version('cakery', 0, 1, 0)
version.__name__ = 'cakery'  # fix epydoc error

#---------------------------------------------------------------------------#
# Exported symbols
#---------------------------------------------------------------------------#
__all__ = ["version"]
