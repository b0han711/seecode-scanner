# coding:utf-8

import argparse

from seecode_scanner.lib.core.service import TestService
from seecode_scanner.lib.core.settings import VERSION_STRING
from seecode_scanner.lib.core.data import paths


def cmd_line():
    """

    return:
    """
    parser = argparse.ArgumentParser("seecode-scanner")

    parser.add_argument(
        '-v',
        dest='verbose',
        default='info',
        choices=['warn', 'debug', 'info', 'error'],
        help='Verbosity level, default: info.'
    )
    parser.add_argument(
        '--test',
        '-t',
        dest='enable_test_services',
        action="store_true",
        help='Test the status of all system services, default: False.'
    )
    parser.add_argument(
        '--no-banner',
        dest='no_banner',
        action="store_true",
        help='Do not display banner information, default: False.'
    )

    parser.add_argument(
        '--version',
        dest='version',
        action="store_true",
        help='Show current software version.'
    )

    parser.add_argument(
        '--upgrade',
        dest='enable_upgrade',
        action='store_true',
        help='Connect to the server for scanning configuration upgrade, default: False.'
    )

    parser.add_argument(
        '--monitor',
        dest='enable_monitor',
        action='store_true',
        help='SeeCode Scanner client heartbeat monitoring service, default: False.'
    )

    # Scan
    scan = parser.add_argument_group('scan arguments')
    scan.add_argument(
        '-c',
        dest='config',
        help='Project scan configuration file based on yaml format.'
    )
    scan.add_argument(
        '--scan-template',
        default='normal',
        dest='template',
        help='Scan the name of the template, default: normal'
    )
    scan.add_argument(
        '--scan-threads',
        dest='threads',
        default=20,
        type=int,
        help='The number of threads when the engine scans, default: 20.'
    )
    scan.add_argument(
        '--scan-path',
        '-p',
        dest='project_path',
        help='The absolute path of the item to be scanned.'
    )
    scan.add_argument(
        '--name',
        '-n',
        dest='project_name',
        help='The name of the project to scan.'
    )
    scan.add_argument(
        '--result-file',
        '-o',
        dest='result_file',
        help='Scan the path saved by the report.'
    )

    # Task
    task = parser.add_argument_group('task arguments')
    task.add_argument(
        '--celery',
        dest='enable_celery',
        action='store_true',
        help="Start celery's work tasks."
    )

    task.add_argument(
        '--celery-concurrency',
        dest='celery_concurrency',
        default=4,
        help='Number of child processes processing the queue, default: 4'
    )

    task.add_argument(
        '--celery-name',
        dest='celery_name',
        default='sca-1',
        help='Set custom hostname, default: sca-1'
    )

    args = parser.parse_args()

    if not args.no_banner:
        print("""---------------------------------------------------------------------------------------------------
          ____     U _____ u U _____ u    ____     U  ___ u   ____    U _____ u              
         / __"| u  \| ___"|/ \| ___"|/ U /"___|     \/"_ \/  |  _"\   \| ___"|/              
        <\___ \/    |  _|"    |  _|"   \| | u       | | | | /| | | |   |  _|"                
         u___) |    | |___    | |___    | |/__  .-,_| |_| | U| |_| |\  | |___                
         |____/>>   |_____|   |_____|    \____|  \_)-\___/   |____/ u  |_____|               
          )(  (__)  <<   >>   <<   >>   _// \\\\        \\\\      |||_     <<   >>               
         (__)      (__) (__) (__) (__) (__)(__)      (__)    (__)_)   (__) (__)              
                  ____        ____      _        _   _       _   _     U _____ u    ____     
                 / __"| u  U /"___| U  /"\  u   | \ |"|     | \ |"|    \| ___"|/ U |  _"\ u  
                <\___ \/   \| | u    \/ _ \/   <|  \| |>   <|  \| |>    |  _|"    \| |_) |/  
                 u___) |    | |/__   / ___ \   U| |\  |u   U| |\  |u    | |___     |  _ <    
                 |____/>>    \____| /_/   \_\   |_| \_|     |_| \_|     |_____|    |_| \_\   
                  )(  (__)  _// \\\\   \\\\    >>   ||   \\\\,-.  ||   \\\\,-.  <<   >>    //   \\\\_  
                 (__)      (__)(__) (__)  (__)  (_")  (_/   (_")  (_/  (__) (__)  (__)  (__) 
    
                {0} xsseroot#gmail.com\n
---------------------------------------------------------------------------------------------------
        """.format(VERSION_STRING))

    if args.enable_test_services:
        ts = TestService()
        ts.start()
        exit(0)

    if args.version:
        scan_template_version = '0.0.0'
        try:
            with open(paths.PROFILE_VERSION_PATH, 'rb') as fp:
                scan_template_version = fp.read().decode('utf-8')
        except Exception as ex:
            pass

        print('{0}, template v{1}'.format(VERSION_STRING, scan_template_version))
        exit(0)

    if not any((args.config, args.enable_monitor, args.enable_upgrade, args.project_path, args.project_name, args.enable_celery)):
        parser.print_help()
        exit(0)


    return args
