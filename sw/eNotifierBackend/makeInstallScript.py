
def create_install_script(component_name, component_description, wheel_name):
    install_script = textFile('dist/install.sh')
    install_script.addLine('echo " -> Check and Stop service"')
    install_script.addLine('sudo systemctl stop ' + component_name + '.service')
    install_script.addLine('echo " -> Check and Remove old version"')
    install_script.addLine('sudo rm -rf /usr/share/iz2k/' + component_name)
    install_script.addLine('sudo mkdir /usr/share/iz2k/' + component_name)
    install_script.addLine('echo " -> Create virtual environment"')
    install_script.addLine('sudo python3 -m venv /usr/share/iz2k/' + component_name + '/venv')
    install_script.addLine('sudo cp version.txt /usr/share/iz2k/' + component_name + '/')
    install_script.addLine('echo " -> Install component"')
    install_script.addLine('sudo /usr/share/iz2k/' + component_name + '/venv/bin/pip install ' + wheel_name)
    install_script.addLine('echo " -> Create executable script"')
    install_script.addLine('sudo touch /usr/share/iz2k/' + component_name + '/' + component_name + '.sh')
    install_script.addLine('echo "/usr/share/iz2k/' + component_name + '/venv/bin/python -m ' + component_name + ' \\"\$@\\"" | sudo tee -a /usr/share/iz2k/' + component_name + '/' + component_name + '.sh | grep donotshowanythinginbash')
    install_script.addLine('sudo chmod +x /usr/share/iz2k/' + component_name + '/' + component_name + '.sh')
    install_script.addLine('echo " -> Create symbolic link"')
    install_script.addLine('sudo ln -f -s /usr/share/iz2k/' + component_name + '/' + component_name + '.sh /usr/bin/' + component_name)

    install_script.addLine('echo " -> Create ' + component_name + ' Service"')
    install_script.addLine('cat << EOF | sudo tee /etc/systemd/system/' + component_name + '.service | grep donotshowanythinginbash')
    install_script.addLine('[Unit]')
    install_script.addLine('Description = ' + component_description)
    install_script.addLine('After = network.target')
    install_script.addLine('')
    install_script.addLine('[Service]')
    install_script.addLine('ExecStart = /usr/share/iz2k/' + component_name + '/venv/bin/python -m ' + component_name)
    install_script.addLine('WorkingDirectory = /usr/share/iz2k/' + component_name)
    install_script.addLine('StandardOutput = inherit')
    install_script.addLine('StandardError = inherit')
    install_script.addLine('Restart = always')
    install_script.addLine('User = root')
    install_script.addLine('')
    install_script.addLine('[Install]')
    install_script.addLine('WantedBy = multi-user.target')
    install_script.addLine('EOF')

    install_script.addLine('echo " -> Enable ' + component_name + ' Service"')
    install_script.addLine('sudo systemctl daemon-reload')
    install_script.addLine('sudo systemctl enable ' + component_name + '.service')
    install_script.addLine('sudo systemctl start ' + component_name + '.service')
    install_script.addLine('echo "Done!"')

    install_script.close()

class textFile:

    def __init__(self, filename, endl = '\n'):
        self.file = open(filename, 'w+', newline=endl)
        self.endl = endl

    def addLine(self, line):
        self.file.write(line + self.endl)

    def close(self):
        self.file.close()
