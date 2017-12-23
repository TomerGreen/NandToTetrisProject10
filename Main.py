import sys
import os
import CompilationEngine
import xml.etree.ElementTree as et
import xml.dom.minidom as dom


def compileFile(filename):
    engine = CompilationEngine.CompilationEngine(filename)
    engine.compileClass()
    xml_string = et.tostring(engine.root, encoding='UTF-8', method='html')
    #pretty_xml_string = dom.parseString(xml_string).toprettyxml()
    #if "?>" in pretty_xml_string:
    #    pretty_xml_string = pretty_xml_string[pretty_xml_string.find("?>")+3:]  # Removes the xml declaration.
    xml_string = xml_string.decode().replace("><",">\n<")
    xml_file = open(filename.replace('.jack', '.xml'), 'w')
    xml_file.write(xml_string)
    xml_file.close()

def compileAll(path):
    if path.endswith('.jack'):
        compileFile(path)
    else:
        for filename in os.listdir(path):
            if filename.endswith('.jack'):
                compileFile(path + '/' + filename)


if __name__ == "__main__":
    path = sys.argv[1]
    compileAll(path)