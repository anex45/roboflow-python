import argparse
from typing import List, Optional

from roboflow.core.project import Project
from roboflow.core.workspace import Workspace


def add_model_commands(subparsers):
    """
    Add model-related commands to the CLI parser.
    """
    # List models command
    list_models_parser = subparsers.add_parser(
        "list-models",
        help="List all models in a workspace",
    )
    list_models_parser.add_argument(
        "-w",
        dest="workspace",
        help="Specify a workspace URL or ID (will use default workspace if not specified)",
    )
    list_models_parser.add_argument(
        "-p",
        dest="project",
        help="Filter models by project name",
    )
    list_models_parser.set_defaults(func=list_models_command)


def list_models_command(args, workspace: Optional[Workspace] = None):
    """
    List all models in a workspace.
    """
    if workspace is None:
        from roboflow import Roboflow
        rf = Roboflow()
        workspace = rf.workspace(args.workspace)

    projects = workspace.projects()
    
    print(f"\nModels in workspace '{workspace.name}':\n")
    
    if not projects:
        print("No models found.")
        return
    
    for project_id in projects:
        # If project filter is specified, skip other projects
        project_name = project_id.split('/')[-1]
        if args.project and args.project != project_name:
            continue
            
        project = workspace.project(project_name)
        versions = project.versions()
        
        # Only show projects with trained models
        models_found = False
        for version in versions:
            if version.model is not None:
                models_found = True
                break
                
        if not models_found:
            continue
            
        print(f"{project.name}")
        print(f"  ID: {project.id}")
        print(f"  Type: {project.type}")
        
        for version in versions:
            if version.model is not None:
                print(f"  Model version {version.version}:")
                print(f"    Created: {version.created}")
                print(f"    Type: {project.type}")
                print(f"    ID: {version.id}")
        print()