import os
import click
import logging
from dotenv import load_dotenv
from run import run_locust

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cli')

load_dotenv()

file = {
    'main': 'main_locustfiles.py',
    'vendors': 'vendors_locust.py',
    'users': 'users_locust.py',
    'super_admin': 'super_admin_locust.py',
    'shopping_list': 'shopping_list_locust.py',
    'report': 'report_locust.py',
    'bin_family': 'bin_family_locust.py',
    'bin': 'bin_locust.py',
    'product': 'product_locust.py',
    'location': 'location_locust.py',
    'licenseplates': 'licenseplates_locust.py',
    'production_order': 'production_order_locust.py',
    'stack': 'stack_locust.py',
    'printer': 'printer_locust.py',
    'learning_video_map': 'learning_video_map_locust.py',
    'pick_lineitem': 'pick_lineitem_locust.py',
    'pick': 'pick_locust.py'
}


@click.command()
@click.option('--test', type=click.Choice(file.keys()))
@click.option(
    '--host',
    default=os.getenv("HOST"),
    required=True,
    help='host')
@click.option(
    '-u', '--users',
    default=os.getenv("USERS"),
    required=True,
    help='number of concurrent users'
    )
@click.option(
    '-r', '--rate',
    default=os.getenv("RATE"),
    required=True,
    help='user per sec'
    )
@click.option(
    '-t', '--time',
    default=os.getenv("TIME"),
    required=True,
    help='duration'
    )
@click.option('--report', is_flag=True, help='is a flag')
def cli(test, host, users, rate, time, report):
    logger.info("LoadTesting CLI Tool")
    logger.info(
        f'''LoadTest: momenttrack {test} api,
            host: {host},
            users: {users},
            rate: {rate},
            time: {time},
            report: {report}'''
        )
    locustfile = file[test]
    run_locust(locustfile, host, users, rate, time, report)


if __name__ == "__main__":
    cli()
