import os


class Global:
    resource_path = 'resources'
    saves_path = 'saves'
    gallery_path = 'gallery'

    with open(os.path.join(resource_path, 'info.txt'), 'r', encoding='utf-8') as f:
        info_text = f.read()
