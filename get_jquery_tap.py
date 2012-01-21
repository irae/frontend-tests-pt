from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

def console_output(report):
    print report

def get_report(target_url, command_executor=None, desired_capabilities=None):
    print "Running Selenium..."
    driver = None
    if command_executor is None:
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Remote(command_executor, desired_capabilities)

    driver.get(target_url)
    WebDriverWait(driver, 30).until(lambda x : is_text_present(driver,"Tests completed"))
    report =  driver.execute_script("return tapResults;")
    driver.quit()

    return report


parser = OptionParser()
parser.add_option("-t", "--target",
                  help="url that jscoverage is running in (default http://localhost:8585/jscoverage.html?/)",
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
    report = get_report( options.target )
else:
    report = get_report(
        options.target,
        options.server,
        webdriver.DesiredCapabilities.FIREFOX,
        )

console_output(report)

