from typing import NamedTuple, Dict, List, Iterator
from pathlib import Path
import fnmatch
import json
import urllib.parse


ModuleName = str
DESCRIPTION_FILENAME = 'elm.json'
STUFF_DIRECTORY = 'elm-stuff'

ElmPackageBase = NamedTuple('ElmPackageBase', [
    ('path', Path),
    ('description', Dict),
    ('name', str),
    ('user', str),
    ('project', str),
    ('is_dep', bool),
])


class ElmPackage(ElmPackageBase):
    def __getattr__(self, name):
        return self.description[name.replace('_', '-')]


def from_path(path: Path, is_dep: bool = False) -> ElmPackage:
    description = load_description(path / DESCRIPTION_FILENAME)
    repo_path = Path(urllib.parse.urlparse(description['repository']).path)
    user = repo_path.parent.stem
    project = repo_path.stem
    return ElmPackage(
        path=path,
        description=description,
        name='{0}/{1}'.format(user, project),
        user=user,
        project=project,
        is_dep=is_dep,
    )


def description_path(package: ElmPackage) -> Path:
    return package.path / DESCRIPTION_FILENAME


def load_description(path: Path) -> Dict:
    with open(str(path)) as f:
        return json.load(f)


def glob_package_modules(
        package: ElmPackage,
        include_paths: List[Path] = [],
        exclude_patterns: List[str] = [],
        force_exclusion: bool = False) -> Iterator[ModuleName]:
    for source_dir_name in package.source_directories:
        source_dir = package.path / source_dir_name
        elm_files = source_dir.glob('**/*.elm')
        for elm_file in elm_files:
            if elm_file.relative_to(package.path).parts[0] == STUFF_DIRECTORY:
                continue

            if include_paths and not any(_matches_include_path(elm_file, include_path)
                                         for include_path in include_paths):
                continue

            rel_path = elm_file.relative_to(source_dir)
            module_name = '.'.join(rel_path.parent.parts + (rel_path.stem,))

            # check for excludes if there's no explicit includes, or if
            # there are explicit includes and exclusion is requested specifically.
            check_excludes = (not include_paths) or force_exclusion
            if check_excludes and any(fnmatch.fnmatch(module_name, module_pattern)
                                      for module_pattern in exclude_patterns):
                continue

            yield module_name


def _matches_include_path(source_path: Path, include_path: Path):
    try:
        source_path.relative_to(include_path)
    except ValueError:
        return False
    else:
        return True
