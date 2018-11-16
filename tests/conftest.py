import os
import os.path
import json
import tarfile

import pytest
import py

import elm_doc


@pytest.fixture(scope='session')
def overlayer():
    elm_doc.__path__.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))


@pytest.fixture
def elm_stuff_fixture_path():
    def for_version(elm_version):
        filename = '{}-core-elm-stuff.tar.gz'.format(elm_version)
        return py.path.local(__file__).dirpath('fixtures', filename)
    return for_version


@pytest.fixture
def module_fixture_path():
    def for_version(elm_version):
        return py.path.local(__file__).dirpath('fixtures', elm_version)
    return for_version


@pytest.fixture
def make_elm_project(elm_stuff_fixture_path, module_fixture_path):
    def for_version(elm_version, root_dir, src_dir='.', package_overrides={}, copy_elm_stuff=False, modules=[]):
        elm_json = dict(default_elm_json, **{'source-directories': [src_dir]})
        elm_json.update(package_overrides)
        elm_json['elm-version'] = '{v} <= v <= {v}'.format(v=elm_version)
        root_dir.join('elm.json').write(json.dumps(elm_json))
        if copy_elm_stuff:
            with root_dir.as_cwd():
                with tarfile.open(str(elm_stuff_fixture_path(elm_version))) as tar:
                    tar.extractall()

        root_dir.ensure(src_dir, dir=True)
        module_root = module_fixture_path(elm_version)
        for module in modules:
            root_dir.join(src_dir, module).write(module_root.join(module).read())

    return for_version


default_elm_json= {
    "type": "application",
    "source-directories": [
        "src"
    ],
    "elm-version": "0.19.0",
    "dependencies": {
        "direct": {
            "elm/browser": "1.0.1",
            "elm/core": "1.0.2",
            "elm/html": "1.0.0"
        },
        "indirect": {
            "elm/json": "1.1.1",
            "elm/time": "1.0.0",
            "elm/url": "1.0.0",
            "elm/virtual-dom": "1.0.2"
        }
    },
    "test-dependencies": {
        "direct": {},
        "indirect": {}
    }
}
