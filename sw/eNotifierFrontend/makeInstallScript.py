
def create_install_script(component_name):
    install_script = textFile('dist/install.sh')
    install_script.addLine('echo " -> Check and Stop service"')
    install_script.addLine('sudo service apache2 stop')
    install_script.addLine('sudo rm -rf /usr/share/iz2k/' + component_name)
    install_script.addLine('echo " -> Install component"')
    install_script.addLine('sudo mkdir /usr/share/iz2k/' + component_name)
    install_script.addLine('sudo cp version.txt /usr/share/iz2k/' + component_name + '/')
    install_script.addLine('sudo cp -r public /usr/share/iz2k/' + component_name + '/')
    install_script.addLine('echo " -> Start Service"')
    install_script.addLine('sudo service apache2 start')
    install_script.addLine('echo "Done"')
    install_script.close()

class textFile:

    def __init__(self, filename, endl = '\n'):
        self.file = open(filename, 'w+', newline=endl)
        self.endl = endl

    def addLine(self, line):
        self.file.write(line + self.endl)

    def close(self):
        self.file.close()
