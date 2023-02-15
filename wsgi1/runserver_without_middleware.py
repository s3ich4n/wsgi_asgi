#
# 클래스 내부에 callable을 전달해주는 케이스
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2023/02/14 22:55 created.
# @modified    2023/02/14 22:55 modified.
# @license     Please refer to the LICENSE file on a root directory of project.
#


import argparse

from pep_example.server import run_with_cgi


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=f"{__file__.split('/')[-1]}",
        description="Middleware checker",
        epilog="2023, made by s3ich4n.",
    )
    parser.add_argument(
        'run',
        choices=['function', 'class'],
    )
    args = parser.parse_args()

    if args.run == "function":
        from pep_example.without_middleware.app_base import easy_application
        run_with_cgi(easy_application)

    else:
        from pep_example.without_middleware.app_base_class import AppClass
        run_with_cgi(AppClass)
