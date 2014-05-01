import argparse
import mako.lookup
import mako.template
import os
import os.path
import re
import SimpleHTTPServer
import SocketServer
import shutil
import tempfile
import yaml

parser = argparse.ArgumentParser(description='generate a static site')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--input', default=os.getcwd())
parser.add_argument('--output', default=tempfile.mkdtemp())
args = parser.parse_args()

config = {
    'ignore_regexes': []
}
try:
    config = dict(config.items() + yaml.load(open('_config.yaml').read()).items())
except IOError:
    pass

assert not os.listdir(args.output), 'output directory not empty'

templates_dir = tempfile.mkdtemp()
if args.debug:
    print 'intermediate templates dir is %s' % templates_dir

def read_and_strip_front_matter(fn):
    f = open(fn)
    y = {}
    if f.readline() == '---\n':
        s = ''
        while True:
            line = f.readline()
            if line == '---\n':
                break
            s += line
        y = yaml.load(s)
    return y, f.read()

# The info we glean from all the files, and the list of (generator, source
# path, input, target path) to generate after scanning everything.
global_tree = {}
to_generate = []

# Paths relative to `args.input`, with the cumulative base YAML.
dirs = [([''], {})]

while dirs:
    direc_list, base_y = dirs.pop(0)
    direc = os.path.join(*direc_list)
    source_dir = os.path.join(args.input, direc)

    # Find `_inherit.yaml` first and apply it to the base YAML, since it
    # applies to everything in and under this directory.
    ps = os.listdir(source_dir)
    if '_inherit.yaml' in ps:
        y = yaml.load(open('_inherit.yaml').read())
        base_y = dict(base_y.items() + y.items())

    for p in ps:
        source_path = os.path.join(source_dir, p)
        target_path = os.path.join(args.output, direc, p)

        # Ignore anything starting with '_'.
        if p.startswith('_'):
            if args.debug:
                print '%s is an internal file, ignoring' % source_path

        # If configured, ignore things.
        elif any(re.search(r, p) for r in config['ignore_regexes']):
            if args.debug:
                print "%s is matched by config['ignore_regexes'] , ignoring" % source_path

        # Make a directory.
        elif os.path.isdir(source_path):
            if args.debug:
                print 'mkdir %s' % target_path
            os.mkdir(target_path)
            dirs.append((direc_list + [p], base_y))

        elif os.path.isfile(source_path):
            y = {}
            if p.endswith('.mako') or p.endswith('.mako_layout'):
                _, ext = os.path.splitext(p)

                # Strip the front matter and maybe insert <%inherit/> tag.
                page_y, source = read_and_strip_front_matter(source_path)
                y = dict(base_y.items() + page_y.items())
                if 'layout' in y:
                    source = '<%%inherit file="/%s"/>\n%s' % (y['layout'], source)
                try:
                    os.makedirs(os.path.join(templates_dir, direc))
                except OSError:
                    pass
                f = open(os.path.join(templates_dir, direc, p), 'w')
                f.write(source)
                f.close()

                # If a .mako: add a 'url' attribute, and defer rendering until later.
                if p.endswith('.mako'):
                    y['url'] = os.path.join(direc, p[:-len(ext)])
                    target_path = target_path[:-len(ext)]
                    to_generate.append((os.path.join(direc, p), y, target_path))
            else:
                if args.debug:
                    print 'copying %s to %s' % (source_path, target_path)
                shutil.copyfile(source_path, target_path)

            # Any concrete file gets added to the 'tree', which is a nested dict.
            t = global_tree
            for part in filter(None, os.path.normpath(target_path[len(args.output):]).split(os.sep)):
                if part not in t:
                    t[part] = {}
                t = t[part]

            # The leaf (file) gets the yaml,
            t.clear()
            for k, v in y.items():
                t[k] = v
        else:
            assert False, 'what is this: %s' % source_path

# Template rendering deferred until now so that each template:
#   . gets the full file `tree` in the render-data,
#   . has been rewritten with <%inherit/> tags,
#   . has had its front matter stripped.
for path, inp, target_path in to_generate:
    if args.debug:
        print 'generating %s from %s, yaml=%s' % (target_path, os.path.join(templates_dir, path), y)

    lookup = mako.lookup.TemplateLookup(directories=[templates_dir], input_encoding='utf-8', output_encoding='utf-8')
    data = {
        'tree': global_tree,
        'page': inp,
    }
    f = open(target_path, 'w')
    f.write(lookup.get_template(path).render(**data))
    f.close()

print 'serving at at http://localhost:8000'
os.chdir(args.output)
SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(('', 8000), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.serve_forever()
