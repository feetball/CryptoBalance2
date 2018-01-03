from google.appengine.ext import vendor

import tempfile
tempfile.SpooledTemporaryFile = tempfile.TemporaryFile
# Add any libraries installed in the "lib" folder.
vendor.add('lib')
