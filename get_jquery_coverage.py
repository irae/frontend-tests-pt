from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from xml.dom.minidom import getDOMImplementation
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from jscoverage_cobertura import generate_cobertura_xml
from optparse import OptionParser

def is_text_present (driver, string):
   if str(string) in driver.page_source: return True
   else:
       return False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

colors = bcolors()

def color_by_percentage(percent):
    color = colors.FAIL
    if float(percent) > 91.0:
        color = colors.WARNING
    if float(percent) >= 97.0:
        color = colors.OKGREEN
    return color

def console_output(report):
    output_lines = []
    for script in report:
        output = "\t" + script + " - "
        total_lines = len(report[script]["coverage"])
        statement_lines = 0
        covered_lines = 0
        uncovered_lines = []
        for idx, line in enumerate(report[script]["coverage"]):
            #print line
            if line is not None:
                statement_lines = statement_lines + 1
            if line > 0:
                covered_lines = covered_lines +1
            if line == 0:
                uncovered_lines.append(idx)
        percent_covered = float(covered_lines)/float(statement_lines)*100.0

        output += "(" + str(covered_lines) + "/" + str(statement_lines) + ") "
        output += color_by_percentage(percent_covered) + str(round(percent_covered,2)) + "% "

        output += colors.ENDC

        if percent_covered < 100.0:
            output += "\n\t\tuncovered:"
            output += str(uncovered_lines)

        output_lines.append(output)

    output_lines.sort()
    print ""
    print "\n".join(output_lines)
    print ""

def get_report(target_url, command_executor=None, desired_capabilities=None):
    print "Running Selenium..."
    driver = None
    if command_executor is None:
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Remote(command_executor, desired_capabilities)

    driver.get(target_url)

    driver.switch_to_frame(0)
    WebDriverWait(driver, 5*60).until(lambda x : is_text_present(driver,"Tests completed"))
    driver.switch_to_default_content()
    report =  driver.execute_script("var coverage = jscoverage_serializeCoverageToJSON(); return coverage;")
    driver.quit()

    try:
       report = json.loads(report)
    except TypeError:
       pass



    return report


parser = OptionParser()
parser.add_option("-t", "--target",
                  help="url that jscoverage is running in",
                  dest="target",
                  default=False,
                  metavar="TARGET")
parser.add_option("-s", "--server",
                  help="url that selenium is running e.g. http://localhost:4444/wd/hub",
                  dest="server",
                  default=False,
                  metavar="SERVER")
parser.add_option("-n", "--no-color",
                  help="disable color output",
                  action="store_false", dest="color", default=True)

(options, args) = parser.parse_args()

if options.server == False:
    report = get_report(options.target)
else:
    report = get_report(
        options.target,
        options.server,
        webdriver.DesiredCapabilities.FIREFOX,
        )

xml_string =  generate_cobertura_xml(report, 'jquery', 'src')

xml_file = open('jscoverage_cobertura.xml', 'w')
xml_file.write(xml_string)
xml_file.close()

if not options.color:
    colors.disable()

console_output(report)





