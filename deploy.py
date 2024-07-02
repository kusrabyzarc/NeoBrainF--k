import os
import shutil
import subprocess


def clean_previous_builds():
    """Очистка предыдущих сборок."""
    dirs_to_remove = ['build', 'dist', 'neobrainfuck.egg-info']
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"Removed {dir_path}")


def build_distributions():
    """Построение новых дистрибутивов."""
    subprocess.run(['py', 'setup.py', 'sdist', 'bdist_wheel'], check=True)
    print("Built new distributions.")


def upload_to_pypi():
    """Загрузка новых дистрибутивов на PyPI."""
    subprocess.run(['twine', 'upload', '--repository', 'pypi', 'dist/*'], check=True)
    print("Uploaded distributions to PyPI.")


if __name__ == "__main__":
    clean_previous_builds()
    build_distributions()
    upload_to_pypi()
