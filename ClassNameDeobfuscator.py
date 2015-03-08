import argparse
import os

__author__ = 'HamiltonianPath'


def parse_args():
    parser = argparse.ArgumentParser(description='Execute in the smali directory of a disassembled APK')
    parser.add_argument('namespace', type=str, help='base namespace to begin deobfuscating classes')
    parser.add_argument('-o', dest='outfile', default=None, metavar='output.txt', type=str, help='output filename to save deobfusacted class mapping')
    return parser.parse_args()


class SmaliFile:
    """A class to represent a Smali file."""

    raw_lines = []  # A list of all lines in the Smali file.

    def __init__(self, filepath=None):
        if filepath:
            self.readsmalifile(filepath)

    def readsmalifile(self, filepath):
        f = open(filepath, 'r')
        self.raw_lines = f.readlines()


class ClassNameDeobfuscator():
    def __init__(self, namespace, outfilepath):
        self.namespace = namespace
        self.outfilepath = outfilepath
        self.outfile = None
        if self.outfilepath:
            self.outfile = open(self.outfilepath, 'w')

    def out(self, message):
        if self.outfile:
            self.outfile.write(message + '\n')
        else:
            print(message)

    def namespace_to_path(self, namespace):
        return namespace.replace('.', os.path.sep)

    def path_to_namespace(self, path):
        return path.replace(os.path.sep, '.')

    def ensure_namespace_dir_exists(self, namespace_dir):
        return os.path.isdir(namespace_dir)

    def parse_classname_from_source_line(self, source_line):
        try:
            return source_line.split(' ')[1].strip().strip('"')
        except IndexError:
            return 'ERROR_WHILE_DEOBFUSCATING_CLASS_NAME'

    def deobfuscate_smali_file_class(self, namespace_path, filename):
        filepath = os.path.join(namespace_path, filename)
        smali_file = SmaliFile(filepath)
        for line in smali_file.raw_lines:
            if line.startswith('.source'):
                return self.parse_classname_from_source_line(line)

    def walk_namespace_dir(self, namespace_dir):
        self.out(' [*] Deobfuscating class names from namespace {0}...'.format(self.path_to_namespace(namespace_dir)))
        for dirpath, dirnames, filenames in os.walk(namespace_dir):
            namespace = self.path_to_namespace(dirpath)
            for file in filenames:
                if file.endswith('smali'):
                    obfuscated_full_namesapce = '{0}.{1}'.format(namespace, file)
                    deobfuscated_name = self.deobfuscate_smali_file_class(dirpath, file)
                    deobfuscated_full_namepsace = '{0}.{1}'.format(namespace, deobfuscated_name)
                    self.out('{0} => {1}'.format(obfuscated_full_namesapce, deobfuscated_full_namepsace))

    def execute(self):
        namespace_dir = self.namespace_to_path(self.namespace)
        if not self.ensure_namespace_dir_exists(namespace_dir):
            self.out(' [E] Could not find directory {0} for given namespace {1}'.format(namespace_dir, self.namespace))
            return

        self.walk_namespace_dir(namespace_dir)

        if self.outfile:
            self.outfile.close()


def main():
    args = parse_args()
    deobfuscator = ClassNameDeobfuscator(args.namespace, args.outfile)
    deobfuscator.execute()

if __name__ == '__main__':
    main()