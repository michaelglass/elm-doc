from pathlib import Path

from elm_doc import elm_package


def test_glob_package_modules_includes_take_precedence_over_excludes(tmpdir, make_elm_project):
    elm_version = '0.19.0'
    make_elm_project(
        elm_version,
        tmpdir,
        copy_elm_stuff=True,
        modules=[
            'Main.elm',
            'MissingModuleComment.elm',
            'PublicFunctionNotInAtDocs.elm',
        ])
    package = elm_package.from_path(Path(str(tmpdir)))
    include_patterns = _resolve_paths(tmpdir, 'Main.elm', 'MissingModuleComment.elm')
    exclude_patterns = ['MissingModuleComment']
    modules = list(elm_package.glob_package_modules(
        package, include_patterns, exclude_patterns, force_exclusion=False))
    assert modules == ['Main', 'MissingModuleComment']


def test_glob_package_modules_excludes_take_precedence_over_includes_if_forced(tmpdir, make_elm_project):
    elm_version = '0.19.0'
    make_elm_project(
        elm_version,
        tmpdir,
        copy_elm_stuff=True,
        modules=[
            'Main.elm',
            'MissingModuleComment.elm',
            'PublicFunctionNotInAtDocs.elm',
        ])
    package = elm_package.from_path(Path(str(tmpdir)))
    include_patterns = _resolve_paths(tmpdir, 'Main.elm', 'MissingModuleComment.elm')
    exclude_patterns = ['MissingModuleComment']
    modules = list(elm_package.glob_package_modules(
        package, include_patterns, exclude_patterns, force_exclusion=True))
    assert modules == ['Main']


def test_glob_package_modules_includes_all_by_default(tmpdir, make_elm_project):
    elm_version = '0.19.0'
    make_elm_project(
        elm_version,
        tmpdir,
        copy_elm_stuff=False,
        modules=[
            'Main.elm',
            'MissingModuleComment.elm',
        ])
    package = elm_package.from_path(Path(str(tmpdir)))
    include_patterns = []
    exclude_patterns = []
    modules = list(elm_package.glob_package_modules(package, include_patterns, exclude_patterns))
    assert modules == ['Main', 'MissingModuleComment']


def test_glob_package_modules_can_include_path_in_non_dot_source_dir(tmpdir, make_elm_project):
    elm_version = '0.19.0'
    make_elm_project(
        elm_version,
        tmpdir,
        src_dir='src',
        copy_elm_stuff=False,
        modules=[
            'Main.elm',
            'MissingModuleComment.elm',
        ])
    package = elm_package.from_path(Path(str(tmpdir)))
    include_patterns = _resolve_paths(tmpdir, 'src/Main.elm')
    exclude_patterns = []
    modules = list(elm_package.glob_package_modules(package, include_patterns, exclude_patterns))
    assert modules == ['Main']


def _resolve_paths(tmpdir, *paths):
    return [str(tmpdir.join(path)) for path in paths]
