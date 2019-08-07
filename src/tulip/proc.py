import subprocess


def run(*cmdstr, **kwargs):
    """
    run shell command
    """
    for c in cmdstr:
        subprocess.run(c, shell=True, **kwargs)


def output(cmdstr):
    """
    run shell command and return output
    """
    proc = subprocess.Popen(cmdstr, shell=True, stdout=subprocess.PIPE)
    return proc.stdout.read().decode("utf-8").strip()


def d(*cmdstr, **kwargs):
    """
    command shortcut: docker
    """
    run(*[f"docker {c}" for c in cmdstr], **kwargs)


def dc(*cmdstr, **kwargs):
    """
    command shortcut: docker-compose
    """
    run(*[f"docker-compose {c}" for c in cmdstr], **kwargs)


def k(*cmdstr, **kwargs):
    """
    command shortcut: kubectl
    """
    run(*[f"kubectl {c}" for c in cmdstr], **kwargs)


def mk(*cmdstr, **kwargs):
    """
    command shortcut: minikube
    """
    run(*[f"minikube {c}" for c in cmdstr], **kwargs)