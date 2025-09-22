import json
import pathlib

CONTAINER_IMAGE = "ghcr.io/williamjacksn/graphviz"
DEFAULT_BRANCH = "master"
PUSH_OR_RELEASE = "github.event_name == 'push' || github.event_name == 'release'"
TAG_PLACEHOLDER = "${{ github.event.release.tag_name }}"
THIS_FILE = pathlib.PurePosixPath(
    pathlib.Path(__file__).relative_to(pathlib.Path.cwd())
)


def gen(content: dict, target: str) -> None:
    pathlib.Path(target).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target).write_text(
        json.dumps(content, indent=2, sort_keys=True), newline="\n"
    )


def gen_compose() -> None:
    target = "compose.yaml"
    content = {
        "services": {
            "graphviz": {
                "image": CONTAINER_IMAGE,
                "environment": {
                    "DESCRIPTION": f"This file ({target}) was generated from {THIS_FILE}"
                },
            }
        }
    }
    gen(content, target)


def gen_dependabot() -> None:
    target = ".github/dependabot.yaml"
    content = {
        "version": 2,
        "updates": [
            {
                "package-ecosystem": e,
                "allow": [{"dependency-type": "all"}],
                "directory": "/",
                "schedule": {"interval": "daily"},
            }
            for e in ["docker", "github-actions", "uv"]
        ],
    }
    gen(content, target)


def gen_workflow_build() -> None:
    target = ".github/workflows/build-container-image.yaml"
    content = {
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "name": "Build the container image",
        "on": {
            "pull_request": {"branches": [DEFAULT_BRANCH]},
            "push": {"branches": [DEFAULT_BRANCH]},
            "release": {"types": ["published"]},
            "workflow_dispatch": {},
        },
        "jobs": {
            "build": {
                "name": "Build the container image",
                "permissions": {"packages": "write"},
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Set up Docker Buildx",
                        "uses": "docker/setup-buildx-action@v3",
                    },
                    {
                        "name": "Build the container image",
                        "uses": "docker/build-push-action@v6",
                        "with": {
                            "cache-from": "type=gha",
                            "cache-to": "type=gha,mode=max",
                            "tags": CONTAINER_IMAGE,
                        },
                    },
                    {
                        "name": "Log in to GitHub container registry",
                        "if": PUSH_OR_RELEASE,
                        "uses": "docker/login-action@v3",
                        "with": {
                            "registry": "ghcr.io",
                            "password": "${{ github.token }}",
                            "username": "${{ github.actor }}",
                        },
                    },
                    {
                        "name": "Push latest image to registry",
                        "if": PUSH_OR_RELEASE,
                        "uses": "docker/build-push-action@v6",
                        "with": {
                            "cache-from": "type=gha",
                            "push": True,
                            "tags": f"{CONTAINER_IMAGE}:latest",
                        },
                    },
                    {
                        "name": "Push release image registry",
                        "if": "github.event_name == 'release'",
                        "uses": "docker/build-push-action@v6",
                        "with": {
                            "cache-from": "type=gha",
                            "push": True,
                            "tags": f"{CONTAINER_IMAGE}:{TAG_PLACEHOLDER}",
                        },
                    },
                ],
            }
        },
    }
    gen(content, target)


def main() -> None:
    gen_compose()
    gen_dependabot()
    gen_workflow_build()


if __name__ == "__main__":
    main()
