import asyncio
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import imageio
from yapapi.log import (enable_default_logger, log_event_repr,
    log_summary)
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext

import utils


data_file = '/golem/owid-covid-data.csv'
country_codes_file = '/golem/country_codes.csv'
plot_file = '/golem/plot.py'


def dates(from_, to):
    start = date.fromisoformat(from_)
    end = date.fromisoformat(to)
    current_date = start
    while current_date <= end:
        yield current_date.isoformat()
        current_date += timedelta(days=1)


def generate_gif(output):
    png_dir = './outputs/'
    images = []
    for file_name in sorted(os.listdir(png_dir)):
        if file_name.endswith('.png'):
            file_path = os.path.join(png_dir, file_name)
            images.append(imageio.imread(file_path))

    imageio.mimsave(output, images, fps=5)


async def main(args):

    package = await vm.repo(
        image_hash='8af41741dc1a15fb85d519dce2b42e994ba2494acd4c71a96c5029d2',
        min_mem_gib=1,
        min_storage_gib=2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        async for task in tasks:
            output_file_name = f'{task.data}.png'
            output_file_path = f'/golem/work/{output_file_name}'
            ctx.send_file('plot.sh', '/golem/work/plot.sh')
            command = (
                '/bin/sh',
                '/golem/work/plot.sh',
                task.data,
                data_file,
                country_codes_file,
                output_file_path,
                args.parameter,
            )
            print(*command)
            ctx.run(*command)
            yield ctx.commit()
            ctx.download_file(output_file_path, f'outputs/{output_file_name}')
            task.accept_task(result=output_file_name)

    async with Engine(
        package=package,
        max_workers=args.workers,
        budget=10.0,
        timeout=timedelta(minutes=10),
        subnet_tag=args.subnet_tag,
        event_emitter=log_summary(log_event_repr),
    ) as engine:

        days = dates(args.start, args.end)
        async for task in engine.map(worker, [Task(data=date) for date in days]):
            print(f'\033[36;1mTask computed: {task}, result: {task.output}\033[0m')

    gif_name = './covid.gif'
    generate_gif(gif_name)

    print(
        f'{utils.TEXT_COLOR_GREEN}'
        f'gif generated: {gif_name}'
        f'{utils.TEXT_COLOR_DEFAULT}'
    )


if __name__ == '__main__':
    parser = utils.build_parser('covid')
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--parameter', type=str, default='new_deaths')
    parser.add_argument('--start', type=str, default='2020-10-01')
    parser.add_argument('--end', type=str, default='2020-10-20')

    args = parser.parse_args()

    enable_default_logger(log_file=args.log_file)

    sys.stderr.write(
        f'Using subnet: {utils.TEXT_COLOR_YELLOW}{args.subnet_tag}{utils.TEXT_COLOR_DEFAULT}\n'
    )

    Path('outputs').mkdir(parents=True, exist_ok=True)

    loop = asyncio.get_event_loop()
    task = loop.create_task(main(args))

    try:
        loop.run_until_complete(task)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        task.cancel()
        loop.run_until_complete(task)
