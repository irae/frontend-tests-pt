import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--target",
                  help="the file",
                  dest="target",
                  default=False,
                  metavar="TARGET")

(options, args) = parser.parse_args()

file = open(options.target, 'r')
index = file.read()
file.close()

patch = '''<script src="qunit/qunit/qunit.js"></script>
	<script src="qunit-tap/lib/qunit-tap.js"></script>
	<script>
		var tapResults = "";
		qunitTap(QUnit, function() { tapResults += Array.prototype.slice.call(arguments).join(" ") + "\\n"; }, {noPlan: true});
	</script>'''

search = '<script src="qunit/qunit/qunit.js"></script>'
file = open(options.target, 'w')
file.write(index.replace(search, patch))

# 		var tapResults = "";		qunitTap(QUnit, function() { tapResults += Array.prototype.slice.call(arguments).join(" ") + "\n"; }, {noPlan: true});	</script>