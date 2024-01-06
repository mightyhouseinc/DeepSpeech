import requests
import progressbar

from os import path, makedirs
from .io import open_remote, path_exists_remote, is_remote_path

SIMPLE_BAR = ['Progress ', progressbar.Bar(), ' ', progressbar.Percentage(), ' completed']

def maybe_download(archive_name, target_dir, archive_url):
    # If archive file does not exist, download it...
    archive_path = path.join(target_dir, archive_name)

    if not is_remote_path(target_dir) and not path.exists(target_dir):
        print(f'No path "{target_dir}" - creating ...')
        makedirs(target_dir)

    if not path_exists_remote(archive_path):
        print(f'No archive "{archive_path}" - downloading...')
        req = requests.get(archive_url, stream=True)
        total_size = int(req.headers.get('content-length', 0))
        done = 0
        with open_remote(archive_path, 'wb') as f:
            bar = progressbar.ProgressBar(max_value=total_size if total_size > 0 else progressbar.UnknownLength, widgets=SIMPLE_BAR)

            for data in req.iter_content(1024*1024):
                done += len(data)
                f.write(data)
                bar.update(done)
    else:
        print(f'Found archive "{archive_path}" - not downloading.')
    return archive_path
