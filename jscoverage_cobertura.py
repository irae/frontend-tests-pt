import json
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import DOMImplementation

def generate_cobertura_xml(report):
    imp = DOMImplementation()
    doctype = imp.createDocumentType(
        qualifiedName='coverage',
        publicId='',
        systemId='http://cobertura.sourceforge.net/xml/coverage-04.dtd',
    )
    doc = imp.createDocument(None, 'coverage', doctype)

    #print doc.toxml()
    #exit()

    #coverage_element = doc.createElementNS(None, "coverage")
    #doc.appendChild(coverage_element)

    coverage_element = doc.getElementsByTagName("coverage")[0]
    sources_element = doc.createElementNS(None, "sources")

    coverage_element.appendChild(sources_element)

    source_element = doc.createElementNS(None, "source")
    sources_element.appendChild(source_element)
    text = doc.createTextNode('app/static/js')
    source_element.appendChild(text)

    packages_element = doc.createElementNS(None, "packages")
    coverage_element.appendChild(packages_element)
    package_element = doc.createElementNS(None, "package")
    package_element.setAttributeNS(None, "name", "Project")
    package_element.setAttributeNS(None, "branch-rate", "0")
    package_element.setAttributeNS(None, "complexity", "0.0")
    packages_element.appendChild(package_element)

    classes_element = doc.createElementNS(None, "classes")
    package_element.appendChild(classes_element)

    total_statements = 0
    total_hits = 0
    for script in report:
        statement_lines = 0
        covered_lines = 0
        line_number = 0
        class_element = doc.createElementNS(None, "class")
        class_element.setAttributeNS(None, "filename", script)
        class_element.setAttributeNS(None, "name", script)
        methods_element = doc.createElementNS(None, "methods")
        class_element.appendChild(methods_element)
        lines_element = doc.createElementNS(None, "lines")
        class_element.appendChild(lines_element)
        for line in report[script]["coverage"]:
            if line is not None:
                statement_lines = statement_lines + 1
                total_statements = total_statements + 1
            if line > 0:
                covered_lines = covered_lines + 1
                total_hits = total_hits + 1
            if line >= 0:
                line_element = doc.createElementNS(None, "line")

                lines_element.appendChild(line_element)
                line_element.setAttributeNS(None, "number", str(line_number))
                line_element.setAttributeNS(None, "branch", "false")
                line_element.setAttributeNS(None, "hits", str(line))

            line_number = line_number + 1

        class_element.setAttributeNS(None, "branch-rate", "0")
        class_element.setAttributeNS(None, "complexity", "0.0")
        class_element.setAttributeNS(None, "line-rate", str(round((float(covered_lines)/float(statement_lines)),2)))

        classes_element.appendChild(class_element)
        # print "Total lines: " + str(len(report[script]["coverage"]))
        # print "    statements:" + str(statement_lines)
        # print "    covered: " + str(covered_lines)
        # print "    percentage: " + str(float(covered_lines)/float(statement_lines)*100.0)

    package_element.setAttributeNS(None, "line-rate", str(round((float(total_hits)/float(total_statements)),2)))

    return doc.toprettyxml()
