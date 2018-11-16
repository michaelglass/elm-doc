'''
'''
from typing import List, Optional
from pathlib import Path

from elm_doc import elm_package
from elm_doc import package_tasks
from elm_doc import asset_tasks
from elm_doc import catalog_tasks


def create_tasks(
        project_path: Path,
        output_path: Optional[Path] = None,
        elm: Optional[Path] = None,
        include_paths: List[Path] = [],
        exclude_modules: List[str] = [],
        force_exclusion: bool = False,
        mount_point: str = '',
        validate: bool = False):
    # todo: gracefully handle missing elm.json
    project_package = elm_package.from_path(project_path)

    for task in package_tasks.create_package_tasks(
            output_path,
            project_package,
            elm=elm,
            include_paths=include_paths,
            exclude_modules=exclude_modules,
            force_exclusion=force_exclusion,
            mount_point=mount_point,
            validate=validate):
        yield task

    if validate:
        return

    for package in deps:
        for task in package_tasks.create_package_tasks(
                output_path, package, elm=elm, mount_point=mount_point):
            yield task

    for task in catalog_tasks.create_catalog_tasks(all_packages, output_path, mount_point=mount_point):
        yield task

    yield {
        'basename': 'assets',
        'actions': [(asset_tasks.build_assets, (output_path, mount_point))],
        'targets': [output_path / 'assets', output_path / 'artifacts'],
        'uptodate': [True],
    }
