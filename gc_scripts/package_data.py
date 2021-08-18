

def data_root_dir():
    import pkg_resources

    dataroot = pkg_resources.resource_filename(
        'gc_scripts',
        'data')
    return dataroot
