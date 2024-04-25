from pathlib import Path

from warg import get_requirements_from_file

from piper import install_requirements_from_file, is_package_updatable

req_file_path = Path(__file__).parent / "requirements.txt"
reqs = get_requirements_from_file(req_file_path)

reqs = [req for req in reqs if is_package_updatable(req.name)]
print(reqs)

if True:
    if reqs:
        install_requirements_from_file(req_file_path)
