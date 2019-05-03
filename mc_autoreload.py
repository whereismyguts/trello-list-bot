import subprocess

reload_command = 'touch /var/www/whereismyguts_pythonanywhere_com_wsgi.py'


def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output, error)
    return output, error


if __name__ == '__main__':
    run_command(reload_command)