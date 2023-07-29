import argparse
import subprocess
import tempfile
from arcgis.gis import GIS, Item
import json
from zipfile import ZipFile
from distutils.sysconfig import get_python_lib


class StoreDictKeyPair(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreDictKeyPair, self).__init__(
            option_strings, dest, nargs=nargs, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        my_dict = {}
        for kv in values:
            k, v = kv.split("=")
            my_dict[k] = v
        setattr(namespace, self.dest, my_dict)


def main():
    site_packages_dir = get_python_lib()

    parser = argparse.ArgumentParser(
        description="ArcGIS Online or Portal as a Python package manager!"
    )

    parser.add_argument(
        dest="operation",
        type=str,
        help="Operation that you wish to perform.",
    )

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="The URL of the package to download and install.",
        required=False,
    )

    parser.add_argument(
        "-o",
        "--org",
        type=str,
        help="The URL of the AGOL or AGE Org.",
        required=False,
    )

    parser.add_argument(
        "-i",
        "--item",
        type=str,
        help="The ID of the package to download and install.",
        required=False,
    )

    parser.add_argument(
        "-p",
        "--profile",
        type=str,
        help="Name of the ArcGIS API profile to use.",
        required=False,
    )

    parser.add_argument("--conn", type=GIS, required=False)

    parser.add_argument(
        "-un",
        "--username",
        type=str,
        help="Username for the AGOL or AGE Org.",
        required=False,
    )

    parser.add_argument(
        "-pw",
        "--password",
        type=str,
        help="Password for the AGOL or AGE Org.",
        required=False,
    )

    parser.add_argument(
        "-r",
        "--replace",
        type=bool,
        help="Replace existing package if it exists.",
        required=False,
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        help=f"Location to install the package. Default is {site_packages_dir}",
        required=False,
        default=site_packages_dir,
    )

    parser.add_argument(
        "-g",
        "-gis",
        type=json.loads,
        required=False,
        help='Arguments to pass through to the ArcGIS API gis.GIS() class for authentication. Pass in as a dictionary {"url" = "https://portal.portal.com/portal"} See https://developers.arcgis.com/python/api-reference/arcgis.gis.toc.html#gis',
        default="{}",
    )

    args = parser.parse_args()

    temp_dir = tempfile.mkdtemp()

    explicit_gis_args = {
        "url": args.org,
        "username": args.username,
        "password": args.password,
        "profile": args.profile,
        "verify_cert": False,
    }

    gis_args = explicit_gis_args | args.g

    if args.operation == "install":
        print("Installing package from ArcGIS Online or Portal...")
        if args.url is not None:
            if "/home/item.html?id=" not in args.url:
                print("Invalid URL. Must be a URL to an item.")
                exit(1)

            if args.item is None:
                # Get the item ID from the URL
                args.item = args.url.split("/home/item.html?id=")[1]

        if args.profile is not None:
            if args.org is None:
                # Get the org URL from the profile
                org = args.profile["url"]

        if args.org is None:
            args.org = "https://www.arcgis.com"

        if args.conn is None:
            args.conn = GIS(**gis_args)

            if args.username is None:
                print("Username is required.")
                exit(1)
            if args.password is None:
                print("Password is required.")
                exit(1)
            if args.org is None:
                print("Org URL is required.")
                exit(1)

        if args.item is None:
            print("Item ID or URL is required.")
            exit(1)

        item = Item(args.conn, args.item)

        if item.type != "Code Sample":
            print("Item must be a Code Attachment.")
            exit(1)

        print(f"Downloading {item.title}...")
        download_path = item.download(temp_dir)
        folder_name = download_path.split("\\")[-1].split(".")[0]
        extract_path = f"{site_packages_dir}\\{folder_name}"

        if download_path.endswith(".zip"):
            with ZipFile(download_path, "r") as zip_file:
                zip_file.extractall(path=extract_path)
        else:
            print("Invalid file type. Must be a .zip file.")
            exit(1)

        print("Installing package...")
        subprocess.check_call(["pip", "install", extract_path])

        print("Package installed successfully.")

        exit(0)

    else:
        print("Invalid operation.")
        exit(1)


if __name__ == "__main__":
    main()
