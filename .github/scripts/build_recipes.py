#!/usr/bin/env python3
import os
import json
from pathlib import Path
import subprocess
import yaml
from collections import defaultdict

BASE_PATH = Path(__file__).parent


def get_updated_recipes():
    updated_paths = os.getenv("BUILD_RECIPES", "").split(" ")
    recipe_files = defaultdict(set)
    for path in updated_paths:
        parts = Path(path).parts
        if len(parts) >= 2 and parts[0] == "recipes":
            recipe_name = parts[1]
            file = "/".join(parts[2:])
            recipe_files[recipe_name].add(file)
    return set(recipe_files.keys())


def load_versions(recipe_dir: Path) -> dict:
    cfg = recipe_dir / "config.yml"
    if not cfg.is_file():
        return {}
    return yaml.safe_load(cfg.read_text() or "").get("versions", {})


for recipe_name in get_updated_recipes():
    recipe_dir = Path("recipes") / recipe_name
    versions = load_versions(recipe_dir)

    for version, info in versions.items():
        recipe_path = recipe_dir / info.get("folder", ".")

        inspect_json = subprocess.check_output(
            ["conan", "inspect", str(recipe_path / "conanfile.py"), "--format=json"],
            text=True,
        )
        recipe_name = json.loads(inspect_json)["name"]

        cmd = [
            "conan",
            "create",
            str(recipe_path),
            "--version",
            version,
            "--build",
            "missing",
            "-pr:a",
            str(BASE_PATH / ".ci_base_profile"),
        ]

        with open(BASE_PATH / "profiles.json", "r") as f:
            profile_list = json.load(f).get(recipe_name)

        print(f"::group::{recipe_name}/{version}", flush=True)

        try:
            print("executing:", " ".join(cmd), flush=True)
            subprocess.run(cmd, check=True)
            for profile in profile_list.get(version, {}).get("profiles", []):
                example_cmd = [
                    "conan",
                    "test",
                    str(recipe_path / "test_example"),
                    f"{recipe_name}/{version}",
                    "--profile",
                    profile,
                ]
                print("executing:", " ".join(example_cmd), flush=True)
                subprocess.run(example_cmd, check=True)
        finally:
            print("::endgroup::", flush=True)
