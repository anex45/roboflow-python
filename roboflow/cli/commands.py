import argparse
from typing import List, Optional

from roboflow.core.project import Project
from roboflow.core.workspace import Workspace


def add_dataset_commands(subparsers):
    """
    Add dataset-related commands to the CLI parser.
    """
    # Upload dataset command
    upload_parser = subparsers.add_parser(
        "upload-dataset",
        help="Upload a dataset from a local folder to a Roboflow project",
    )
    upload_parser.add_argument(
        "folder",
        help="Filesystem path to a folder that contains your dataset",
    )
    upload_parser.add_argument(
        "-w",
        dest="workspace",
        help="Specify a workspace URL or ID (will use default workspace if not specified)",
    )
    upload_parser.add_argument(
        "-p",
        dest="project",
        required=True,
        help="Project name (will be created if it does not exist)",
    )
    upload_parser.add_argument(
        "-c",
        dest="concurrency",
        type=int,
        default=10,
        help="How many image uploads to perform concurrently (default: 10)",
    )
    upload_parser.add_argument(
        "-n",
        dest="batch_name",
        help="Name of batch to upload to within project",
    )
    upload_parser.add_argument(
        "-r",
        dest="num_retries",
        type=int,
        default=0,
        help="Retry failed uploads this many times (default: 0)",
    )
    upload_parser.add_argument(
        "-l",
        dest="license",
        default="MIT",
        help="License for the project (default: MIT)",
    )
    upload_parser.add_argument(
        "-t",
        dest="project_type",
        default="object-detection",
        choices=[
            "object-detection",
            "classification",
            "instance-segmentation",
            "semantic-segmentation",
            "keypoint-detection",
        ],
        help="Type of the project (default: object-detection)",
    )
    upload_parser.set_defaults(func=upload_dataset_command)

    # Download dataset command
    # Note: This is already implemented in the main CLI as 'download'

    # List datasets command
    list_datasets_parser = subparsers.add_parser(
        "list-datasets",
        help="List all datasets in a workspace",
    )
    list_datasets_parser.add_argument(
        "-w",
        dest="workspace",
        help="Specify a workspace URL or ID (will use default workspace if not specified)",
    )
    list_datasets_parser.set_defaults(func=list_datasets_command)


def upload_dataset_command(args, workspace: Optional[Workspace] = None):
    """
    Upload a dataset to Roboflow.
    """
    if workspace is None:
        from roboflow import Roboflow
        rf = Roboflow()
        workspace = rf.workspace(args.workspace)

    workspace.upload_dataset(
        dataset_path=args.folder,
        project_name=args.project,
        num_workers=args.concurrency,
        project_license=args.license,
        project_type=args.project_type,
        batch_name=args.batch_name,
        num_retries=args.num_retries,
    )


def list_datasets_command(args, workspace: Optional[Workspace] = None):
    """
    List all datasets in a workspace.
    """
    if workspace is None:
        from roboflow import Roboflow
        rf = Roboflow()
        workspace = rf.workspace(args.workspace)

    projects = workspace.projects()
    
    print(f"\nDatasets in workspace '{workspace.name}':\n")
    
    if not projects:
        print("No datasets found.")
        return
    
    for project_id in projects:
        project = workspace.project(project_id.split('/')[-1])
        versions = project.versions()
        version_count = len(versions)
        
        print(f"{project.name}")
        print(f"  ID: {project.id}")
        print(f"  Type: {project.type}")
        print(f"  Images: {project.images}")
        print(f"  Versions: {version_count}")
        if versions:
            print(f"  Latest version: {versions[-1].version}")
        print(f"  Classes: {list(project.classes.keys())}")
        print()